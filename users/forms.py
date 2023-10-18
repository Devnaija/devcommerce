from django import forms

from . models import Customer

class UserProfile(forms.ModelForm):
    password1 = forms.CharField(label=('Password'),widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=('Confirm Password'),widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Customer
        fields = ['fullname','username','email','password1','password2','sex','profile_pix']

        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'profile_pix': forms.FileInput(attrs={'class': 'form-control'}),
        }
