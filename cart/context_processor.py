def total_cart(request):
    total = 0.0
    #if request.user.is_authenticated:
    if 'cart' in request.session:
        for key,value in request.session['cart'].items():
            total = total +(float(value['price'])   )
    return {"total_cart":total}

