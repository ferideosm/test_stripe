from django.db import models


class Item(models.Model):

    class CURRENCIES(models.TextChoices):
        eur = 'EUR'
        usd = 'USD'

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.TextField()
    currency = models.CharField(choices=CURRENCIES.choices, max_length=5, blank=True, default=CURRENCIES.usd.value)


    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    order_number = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.order_number = str(self.pk).zfill(10)
        super().save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True)
    tax = models.ForeignKey('Tax', on_delete=models.CASCADE, blank=True, null=True)


class Discount(models.Model):
    percent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.percent}'

class Tax(models.Model):
    amount = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return f'{self.amount}'

