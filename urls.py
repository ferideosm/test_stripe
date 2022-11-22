"""stripe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from payments import views

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/<int:pk>/', views.ItemDetail.as_view(), name='item'),
    path('buy/<int:pk>/', views.buy, name='buy'),
    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order'),
    path('buy_order/<int:pk>/', views.buy_order, name='buy_order'),
    path('', include('payments.urls')),
] + router.urls
