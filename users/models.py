from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    SEX_CHOICE = (
        ('M','Male'),
        ('F','Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    dob = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=8,choices=SEX_CHOICE)
    profile_pix = models.ImageField(upload_to='profile' , blank=True)

    def __str__(self):
        return f'{self.username}'
        