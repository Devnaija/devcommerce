from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib  import messages

from . models import *
from . forms import CheckoutForm

# Create your views here.
def index(request):
    # slider
    sliders = Slider.objects.all()
    # category
    categorys = Category.objects.all()[:4]

    # products
    products = Product.objects.filter(available=True)[:3]
    
    context={
        'sliders':sliders,
        'categorys':categorys,
        'products':products
    }
    return render(request, 'stores/index.html',context)

def stores(request):
    products = Product.objects.all()
    paginator = Paginator(products,3)
    page_number = request.GET.get("page")
    page_list= paginator.get_page(page_number)    
    context ={
        'products': products,
        'paginator':page_list
    }
    return render(request, 'stores/stores.html',context)

def store(request,id):
    product = Product.objects.get(id=id)
    
    context ={
        'product': product
    }
    return render(request, 'stores/detail.html',context)

def search(request):
    if request.method == 'GET':
        kword = request.GET.get('search')
        output = Product.objects.filter(Q(title__icontains = kword) | Q(description__icontains = kword) )

        context ={
            'output':output
        }
    return render(request, 'stores/search.html',context)

        

def category(request,id):
    get_category = Product.objects.all().filter(category=id)

    context ={
        'output':get_category
    }
    return render(request, 'stores/category.html',context)

def addtocart(request,id):
    # get the product
    cart_product = Product.objects.get(id=id)   
    # check if cart exit
    cart_id = request.session.get('cart_id', None)
    
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)

        # assign a cart to a user
        if request.user.is_authenticated and request.user.customer():
            cart_item.customer = request.user.customer
            cart_item.save()

        # check if item in cart
        item_in_cart = cart_item.cartproduct_set.filter(product=cart_product)
        
        if item_in_cart.exists():
           cartproduct = item_in_cart.last()
           cartproduct.quantity +=1
           cartproduct.subtotal += cart_product.price
           cartproduct.save()
           cart_item.total += cart_product.price
           cart_item.save()
           messages.success(request, 'Item increased in cart successfully !')

        else: 
            cartproduct = CartProduct.objects.create(cart = cart_item,product=cart_product,quantity=1,subtotal=cart_product.price)
            cart_item.total += cart_product.price
            cart_item.save()
            messages.success(request, 'Item added to cart successfully !')

    else:
        cart_item = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_item.id
        cartproduct = CartProduct.objects.create(cart = cart_item,product=cart_product,quantity=1,subtotal=cart_product.price)
        cart_item.total += cart_product.price
        cart_item.save()
        messages.success(request, 'New Item added to cart successfully !')
        
    return redirect('stores')


def myCart(request):
    cart_id = request.session.get('cart_id', None)

    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)

         # assign a cart to a user
        if request.user.is_authenticated and request.user.customer:
            cart_item.customer = request.user.customer
            cart_item.save()
            
    else:
        cart_item = None

    context={
        'cart':cart_item
    }
    return render(request,'stores/mycart.html',context)

def manage(request, id):
    action = request.GET.get('action')
    cart_obj = CartProduct.objects.get(id=id)
    cart = cart_obj.cart

    if action == 'inc':
        cart_obj.quantity +=1
        cart_obj.subtotal +=cart_obj.product.price
        cart_obj.save()
        cart.total +=cart_obj.product.price
        cart.save()
        messages.success(request,'quantity increase')
        
    if action == 'dcr':
        cart_obj.quantity -=1
        cart_obj.subtotal -=cart_obj.product.price
        cart_obj.save()
        cart.total -=cart_obj.product.price
        cart.save()
        messages.success(request,'quantity decreased')
        if cart_obj.quantity ==0:
            cart_obj.delete()

    if action == 'rmv':
        cart.total -= cart_obj.subtotal
        cart.save()
        cart_obj.delete()
    
    return redirect('mycart')

def checkout(request):
    cart_id = request.session.get('cart_id', None)
    cart_obj = Cart.objects.get(id = cart_id)
    form = CheckoutForm()

    # checking authentication
    if request.user.is_authenticated and request.user.customer:
        pass
    else:
        return redirect('/user/login/?next=/checkout/')

    if request.method == "POST":
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit = False)
            form.cart = cart_obj
            form.amount = cart_obj.total
            form.subtotal = cart_obj.total
            form.discount = 0
            form.order_status = 'pending'
            paymethod = form.payment_method
            del request.session['cart_id']
            paymethod = form.payment_method
            form.save()

            order = form.id
            if paymethod == 'paystack':
                return redirect('payment', id =order)
            
    context = {
        'cart':cart_obj,
        'form':form
    }
    return render(request, 'stores/checkout.html',context)


def paymentPage(request,id):
    orders = Order.objects.get(id=id)
    context = {
        'order':orders,
        'paystack_public_key' : settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'stores/payment.html',context)


def verify_payment(request:HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Order, ref =ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('dashboard')
