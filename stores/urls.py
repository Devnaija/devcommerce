from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stores/', views.stores, name='stores'),
    path('store/<str:id>/', views.store, name='store'),
    path('search/', views.search, name='search'),
    path('category/<str:id>/', views.category, name='category'),
    path('addtocart/<str:id>/', views.addtocart, name='addtocart'),
    path('mycart/', views.myCart, name='mycart'),
    path('manage/<str:id>/', views.manage, name='manage'),
    path('checkout',views.checkout,name='checkout'),
    
    path('payment/<str:id>/',views.paymentPage, name='payment'),
    path('<str:ref>/',views.verify_payment, name='verify-payment'),
]