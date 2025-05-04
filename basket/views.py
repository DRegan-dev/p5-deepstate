from django.shortcuts import render, redirect

# Create your views here.
def view_basket(request):
    """ Aview that renders basket contents page """

    return render(request, "basket/basket.html")

def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the basket """
    print("add_to_basket view called")
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

   

    if item_id in basket:
        basket[item_id] += quantity
    else:
        basket[item_id] = quantity

    request.session['basket'] = basket 
    print(request.session['basket'])

    print(f'Added/updated product {item_id}, quantity: {quantity}. Basket now contains: {basket}')

    return redirect(redirect_url)