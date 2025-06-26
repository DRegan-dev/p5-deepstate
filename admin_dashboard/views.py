from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from products.models import Product, Category
from checkout.models import OrderLineItem
# Create your views here.

@login_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_sales = OrderLineItem.objects.aggregate(Sum(lineitem_total))['lineitem_total__sum'] or 0