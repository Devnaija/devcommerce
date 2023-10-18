from django import forms
from .models import Order
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['cart','discount','subtotal','amount','ref','order_status','payment_complete']
        widgets= {
            'order_by': forms.TextInput(attrs={'class': 'form-control','placeholder':'e.g John Doe'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }