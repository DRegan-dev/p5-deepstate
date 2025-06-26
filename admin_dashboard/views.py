from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from products.models import Product, Category
from checkout.models import OrderLineItem
# Create your views here.

@login_required
def admin_dashboard(request):
    # Get statistics
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_sales = OrderLineItem.objects.aggregate(Sum(lineitem_total))['lineitem_total__sum'] or 0

    #Get recent products
    recent_products = Product.objects.orderby('-date_added')[:5]

    # Get best-selling products
    best_selling = OrderLineItem.objects.values('products__name').annotate(
        total_sold=Sum('quantity')
    ).orderby('-total_sold')[:5]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_sales': total_sales,
        'recent_products': recent_products,
        'best_selling': best_selling
    }

    return render(request, 'admin_dashboard/dashboard.html', context)