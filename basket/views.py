from django.shortcuts import render, redirect, reverse, HttpResponse
# Create your views here.
def view_basket(request):
    """ Aview that renders basket contents page """

    return render(request, "basket/basket.html")

def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the basket """
    print("add_to_basket view called")
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    basket = request.session.get('basket', {})

    if item_id in basket:
        basket[item_id] += quantity
    else:
        basket[item_id] = quantity

    # if size:
    #     if item_id in basket:
    #         if size in basket[item_id]['items_by_size'].keys():
    #             basket[item_id]['items_by_size'][size] += quantity
    #         else:
    #             basket[item_id]['items_by_size'][size] = quantity
    #     else:
    #         basket[item_id] = {'items_by_size': {size: quantity}}
    # else:
    #     if item_id in basket:
    #         if 'default' in basket[item_id]['items_by_size']:
    #             basket[item_id]['items_by_size']['default'] += quantity
    #         else:
    #             basket[item_id]['items_by_size']['default'] = quantity
    #     else:
    #         basket[item_id] = {'items_by_size': {'default': quantity}}

    request.session['basket'] = basket 
    print(request.session['basket'])

    print(f'Added/updated product {item_id}, quantity: {quantity}. Basket now contains: {basket}')

    return redirect('basket:view_basket')

def adjust_basket(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    quantity_str = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity_str) if quantity_str else 1
    except (ValueError, TypeError):
        return redirect(reverse('basket:view_basket'))
    
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
    else:
        if item_id in basket:
            del basket[item_id]


    request.session['basket'] = basket
    return redirect(reverse('basket:view_basket'))

def remove_from_basket(request, item_id):
    """ Remove the tem from the shopping basket """
    try:
        basket = request.session.get('basket', {})

        if item_id in basket:
            del basket[item_id]
            request.session['basket'] = basket
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

    except Exception as e:
        print(f"Error in remove_from_basket: {str(e)}")
        return HttpResponse(status=500)                             
        