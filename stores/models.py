from django.db import models
from users.models import Customer
import secrets
# Create your models here.
from . paystack import Paystack
class Slider(models.Model):
    image = models.ImageField(upload_to='slider')
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.created_at)}'


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='category')
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Category :-{self.name}'
    class Meta:
        ordering: ['-name']

        
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product')
    available = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product: -{self.title}'
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True,blank=True)
    total = models.PositiveIntegerField()
    created_at= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{str(self.total)}'

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created_at= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.product.price} - {self.quantity}'
    

ORDER_STATUS =(
    ('pending','pending'),
    ('payment received','payment received'),
    ('order in progress','order in progress'),
    ('order canceled','order canceled'),
    ('order shipped','order shipped'),
    ('order completed','order completed'),
)
PAYMENT_METHOD =(
    ('paystack','paystack'),
    ('transefer','transefer'),
    
)
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    shipping_address = models.TextField()
    discount = models.PositiveIntegerField(null=True,blank=True)
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS, null=True)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD, default='paystack',null=True,blank=True)
    payment_complete = models.BooleanField(default=False)
    ref = models.CharField(max_length=255, null=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.payment_complete} <==> {self.cart}'
    
    # ref generate and save
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref = ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)

    # amount conversion from cent to dollar/naira
    def amount_value(self)-> int:
        return self.amount * 100

    def verify_payment(self):
            paystack = Paystack()
            status, result = paystack.verify_payment(self.ref, self.amount)
            if status:
                if result['amount'] / 100 == self.amount:
                    self.payment_complete = True
                self.save()
            if self.payment_complete:
                return True
            return False

