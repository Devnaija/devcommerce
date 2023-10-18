from . models import Category,CartProduct,Cart

def category(request):
    category = Category.objects.all()
    context = {
        'categorys':category
    }
    return context

def cartproduct(request):
    # cart_id = request.session.get('cart_id', None)

    # if cart_id:
    #     cart_item = Cart.objects.get(id=cart_id)
    #     items = cart_item.cartproduct_set.all()
    #     numbers_of_items = len(items)
    
    context={
        # 'count': numbers_of_items
    }
    return context