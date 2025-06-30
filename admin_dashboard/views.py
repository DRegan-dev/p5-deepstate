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
    total_sales = OrderLineItem.objects.aggregate(Sum('lineitem_total' ))['lineitem_total__sum'] or 0

    #Get recent products with their categories
    recent_products = Product.objects.select_related('category').order_by('-date_added')[:5]

    # Get all categories form dropdown
    categories = Category.objects.all()

    # Handle category update
    if request.method == 'POST' and request.POST.get('action') == 'update_categories':
        product_id = request.POST.get('product_id')
        selected_categories = request.POST.getlist('category_ids[]')

        try:
            product = Product.objects.get(pk=product_id)
            product.categories.set(selected_categories)
            messages.success(request, f'Successfully updated categories for {product.name}')
        except product.DoesNotExist:
            messages.error(request, 'Product not found')
        except Exception as e:
            messages.error(request, f'Error updating categories: {str(e)}') 



    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_sales': total_sales,
        'recent_products': recent_products,
        'categories': categories
    }

    return render(request, 'admin_dashboard/dashboard.html', context)