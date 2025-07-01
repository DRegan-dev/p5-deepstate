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
        size = request.POST[product_size]
    basket = request.session.get('basket', {})

   
    if size:
        if item_id in basket:
            if size in basket[item_id]['items_by_size'].keys():
                basket[item_id]['items_by_size'][size] += quantity
            else:
                basket[item_id]['items_by_size'][size] = quantity
        else:
            basket[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in basket:
            basket[item_id] += quantity
        else:
            basket[item_id] = quantity

    request.session['basket'] = basket 
    print(request.session['basket'])

    print(f'Added/updated product {item_id}, quantity: {quantity}. Basket now contains: {basket}')

    return redirect(redirect_url)

def adjust_basket(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    basket = request.session.get('basket', {})

    if size:
        if quantity > 0:
            basket[item_id]['items_by_size'][size] = quantity
        else:
            del basket[item_id][item_id][size]
            if not basket[item_id]['items_by_size']:
                basket.pop(item_id)
    else:
        if quantity > 0:
            basket[item_id] = quantity
        else:
            basket.pop(item_id)

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))

def remove_from_basket(request, item_id):
    """ Remove the tem from the shopping basket """
    try:
        basket = request.session.get('basket', {})

        if item_id in basket:
            if isinstance(basket[item_id],dict):
                size = request.POST.get('size')
                if size:
                    if size in basket[item_id]['items_by_size']:
                        del basket[item_id][size]
                        if not basket[item_id]['items_by_size']:
                            del basket[item_id]
                else:
                    del basket[item_id]
            else:
                del basket[item_id]

            request.session['basket'] = basket
            return HttpResponse(status=200)

        return HttpResponse(status=404)

    except Exception as e:
        print(f"Error in remove_from_basket: {str(e)}")
        return HttpResponse(status=500)                             
        