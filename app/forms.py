from .models import Customer,Product,Order_placed,Cart
from django import forms

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['name','city','zip_code','state']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "city":forms.TextInput(attrs={"class":"form-control"}),
            "district":forms.TextInput(attrs={"class":"form-control"}),
            "zip_code":forms.NumberInput(attrs={"class":"form-control"}),
            "state":forms.TextInput(attrs={"class":"form-control"}),
        }

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name','selling_price','discounted_price','description','brand','category','image']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "selling_price":forms.NumberInput(attrs={"class":"form-control"}),
            "discounted_price":forms.NumberInput(attrs={"class":"form-control"}),
            "description":forms.TextInput(attrs={"class":"form-control"}),
            "brand":forms.TextInput(attrs={"class":"form-control"}),
            "category":forms.TextInput(attrs={"class":"form-control"}),
            "image":forms.TextInput(attrs={"class":"form-control"}),
        }

class CartForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ['user','product','quantity']
        widgets={
            "user":forms.TextInput(attrs={"class":"form-control"}),
            "product":forms.TextInput(attrs={"class":"form-control"}),
            "quantity":forms.NumberInput(attrs={"class":"form-control"}),
        }