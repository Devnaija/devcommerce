from django.shortcuts import redirect, render
from . models import Customer
from . forms import UserProfile
from stores.models import Order,Cart

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


# login
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'User login successfully')
            return redirect('dashboard')
        
        if 'next' in request.GET:
            next_url = request.GET.get('next')
            return redirect(next_url)
        
    return render(request, 'users/login.html')

    
# register
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    forms = UserProfile
    if request.method == 'POST':
        forms = UserProfile(request.POST, request.FILES)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            email = forms.cleaned_data.get('email')
            password = forms.cleaned_data.get('password1')
            password2 = forms.cleaned_data.get('password2')

            if password != password2:
                messages.warning(request, "Password not match")
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
                return redirect('register')
            user = User.objects.create_user(username,email,password)
            forms = forms.save(commit=False)
            forms.user = user
            forms.save()
            messages.success(request, "Registration successful")
            return redirect('login')

    if 'next' in request.GET:
        next_url = request.GET.get('next')
        return redirect(next_url)

    context={
        'forms':forms
    }
    return render(request, 'users/register.html',context)


# logout
def logoutuser(request):
    logout(request)
    return redirect('login')

# dashboard
def dashboard(request):
    user = request.user.customer
    cart =  Cart.objects.filter(customer = user)

    order = Order.objects.filter(cart__id__in= cart)

    context = {
        'user':user,
        'order':order
    }
    return render(request, 'users/dashboard.html', context)