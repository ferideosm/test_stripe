from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.views.generic import ListView
from .models import Item, Order, OrderItem
from rest_framework import viewsets, generics
from .serializers import ItemSerializer, OrderItemSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
import settings
import stripe


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'data': self.object}, template_name='items.html')


class OrderDetail(ListView):
    model = OrderItem
    queryset = OrderItem.objects.all()
    template_name = 'orders.html'

    def get_context_data(self, **kwargs):
        obj_ = super().get_queryset().filter(order_id=self.kwargs['pk'])
        category = get_object_or_404(OrderItem, title=self.kwargs['pk'])
        print('category_ ', category)
        if not obj_:
            print(' not obj_ ', obj_)
            return {'error': 'gfgfgfgf'}
        serializer = OrderItemSerializer(obj_, many=True)
        return get_data(self.kwargs['pk'], serializer)


def get_data(pk, serializer):
    import json
    data = dict()
    data['data'] = list()
    tax_due = 0
    discount = 0
    tax = 0
    for d in serializer.data:
        item = json.loads(json.dumps(d))
        price = float(item['item']['price'])
        quantity = item['quantity']
        item['amount'] = float(price * quantity)
        item['unit_amount'] = price
        if item.get('discount'):
            unit_amount = price * float(item['discount']['percent']) / 100
            discount_ = unit_amount * quantity
            item['amount'] -= discount_
            item['unit_amount'] -= unit_amount
            discount += discount_
        if item.get('tax'):
            tax_ = float(item['tax']['amount'])
            item['amount'] += tax_
            item['unit_amount'] += tax_
            tax += tax_
        tax_due += item['amount']
        data['data'].append(item)

    data['id'] = pk
    data['order_id'] = str(pk).zfill(10)
    data['currency'] = data['data'][0]['item']['currency']
    data['tax_due'] = tax_due
    data['discount'] = discount
    data['tax'] = tax
    return data


def buy(request, pk):
    item = Item.objects.get(pk=pk)
    url = 'https://www.google.com/'
    stripe.api_key = settings.API_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
              'currency': item.currency.lower(),
              'unit_amount': int(item.price * 100),
              'product_data': {
                'name': item.name,
                'description': item.description,
              },
            },
            'quantity': 1,
          }],
        mode='payment',
        customer=settings.customer_id,
        success_url=url,
        cancel_url=url,
    )
    return redirect(session['url'])


def buy_order(request, pk):
    obj_ = OrderItem.objects.filter(order_id=pk)
    serializer = OrderItemSerializer(obj_, many=True)
    items = get_data(pk, serializer)
    url = 'https://www.google.com/'
    stripe.api_key = settings.API_KEY
    line_items = list()
    for item in items['data']:
        line_items.append({
            'price_data': {
                'currency': item['item']['currency'].lower(),
                'unit_amount': int(item['unit_amount'] * 100),
                'product_data': {
                    'name': item['item']['name'],
                    'description': item['item']['description'],
                },
            },
            'quantity': item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        customer=settings.customer_id,
        success_url=url,
        cancel_url=url,
    )
    return redirect(session['url'])


def home(request):
    return render(request, 'home.html', {})
