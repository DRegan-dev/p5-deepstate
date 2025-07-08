from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
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
    all_products = Product.objects.all().select_related('category').order_by('-date_added')

    # Get all categories form dropdown
    categories = Category.objects.all().order_by('name')

    # Handle category update
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.POST.get('action')
        if action == 'update_categories':
            return handle_category_update_ajax(request)
    
    if request.method == 'POST' and request.POst.get('action') == 'update_categories':
        return handle_category_update(request)
         



    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_sales': total_sales,
        'all_products': all_products,
        'categories': categories
    }

    return render(request, 'admin_dashboard/dashboard.html', context)

def handle_category_update(request):
    """
    Handle Category update logic separated for better readability.
    """
    product_id = request.POST.get('product_id')
    category_id = request.POST.getlist('category_id')

    if not product_id:
        messages.error(request, 'Product ID is required')
        return redirect('admin_dashboard')
    try:
        product = get_object_or_404(Product, pk=product_id)

        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            product.category = category
        else:
            product.category = None

        product.save()
        messages.success(request, 'Successfully updated category for {product.name}')

    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found')
    except Exception as e:
        messages.error(request, f'Error updating categories: {str(e)}')

    return redirect('admin_dashboard')

@login_required
@require_POST
def handle_category_update_ajax(request):

    product_id = request.POST.get('product_id')
    category_id = request.POST.get('category_id')

    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID is required'})
    
    try:
        product = get_object_or_404(Product, pk=product_id)

        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            product.category = category
        else:
            product.category = None

        product.save()

        return JsonResponse({
            'success': True,
            'message': f'Successfully updated categories for {product.name}'
        })
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Product not found'
        })
    
    except Category.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Category not found'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        })
    
@login_required
def get_product_stats(request):

    stats = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_sales': OrderLineItem.objects.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or 0,
        'recent_products_count': Product.objects.filter(
            date_added__gte=timezone.now() - timedelta(days=7)
        ).count()
    }
    return JsonResponse(stats)
