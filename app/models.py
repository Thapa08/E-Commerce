from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    state_choice=[
        ('Pradesh-1','Pradesh-1'),
        ('Pradesh-2','Pradesh-2'),
        ('Pradesh-3','Pradesh-3'),
        ('Pradesh-4','Pradesh-4'),
        ('Pradesh-5','Pradesh-5'),
        ('Pradesh-6','Pradesh-6'),
        ('Pradesh-7','Pradesh-7'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    zip_code = models.IntegerField(null=True,blank=True)
    state = models.CharField(max_length=100,choices=state_choice)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_choices = [
        ('Smartphone','Smartphone'),
        ('Laptop','Laptop'),
        ('Topwear','Topwear'),
        ('Bottomwear','Bottomwear'),
    ]
    name = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.CharField(max_length=300)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100,choices=product_choices)
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.name
    
class Order_placed(models.Model):
    status_choice=[
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On the way','On the way'),
        ('Delivered','Delivered'),
        ('Canceled','Canceled'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=status_choice,default='Pending')

    def __str__(self):
        return f"{str(self.id)}"

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price