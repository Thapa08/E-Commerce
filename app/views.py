from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import CustomerForm,CartForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer,Product,Order_placed,Cart
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
   electronics = Product.objects.filter(category='Smartphone') | Product.objects.filter(category='Laptop')
   fashion = Product.objects.filter(category='Topwear') | Product.objects.filter(category='Bottomwear')
   context={
        'electronics':electronics,
        'fashion':fashion,
    }
   return render(request,'home.html',context)

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.is_staff = True
            user.save()
    else:
        form = UserCreationForm() 
    return render(request,'register.html',{"form":form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                uname =form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return redirect("home")
        else:
            form = AuthenticationForm()
        return render(request,'login.html',{'form':form})
    else:
        return redirect("home")               

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("home")        

@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('profile')
    else:
        form = CustomerForm()
    return render(request,'profile.html',{'form':form})

@login_required(login_url='/login/')
def address(request):
    user = request.user
    user_address = Customer.objects.filter(user=user)
    return render(request,'address.html',{'addresses':user_address})

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request,'changepassword.html',{'form':form})

def product_detail(request,id):
    product = Product.objects.get(id=id)
    return render(request,'productdetail.html',{'product':product})

def smartphones(request,data=None):
    if data == None:
        phone = Product.objects.filter(category='Smartphone')
    elif data == 'Google' or data == 'Samsung':
        phone = Product.objects.filter(category='Smartphone').filter(brand=data)
    elif data == 'below':
        phone = Product.objects.filter(category='Smartphone').filter(discounted_price__lt=1000)
    elif data == 'above':
        phone = Product.objects.filter(category='Smartphone').filter(discounted_price__gt=1000)
    return render(request,'phone.html',{'phones':phone})

def Laptops(request,data=None):
    if data == None:
        laptop = Product.objects.filter(category='Laptop')
    elif data == 'Lenovo' or data == 'Apple':
        laptop = Product.objects.filter(category='Laptop').filter(brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(category='Laptop').filter(discounted_price__lt=1000)
    elif data == 'above':
        laptop = Product.objects.filter(category='Laptop').filter(discounted_price__gt=1000)
    return render(request,'laptop.html',{'laptops':laptop})

def Topwears(request,data=None):
    if data == None:
        topwear = Product.objects.filter(category='Topwear')
    elif data == 'Polo' or data == 'Prada':
        topwear = Product.objects.filter(category='Topwear').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='Topwear').filter(discounted_price__lt=10)
    elif data == 'above':
        topwear = Product.objects.filter(category='Topwear').filter(discounted_price__gt=10)
    return render(request,'topwear.html',{'topwears':topwear})

def Bottomwears(request,data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='Bottomwear')
    elif data == 'Levis' or data == 'Prada':
        bottomwear = Product.objects.filter(category='Bottomwear').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='Bottomwear').filter(discounted_price__lt=10)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='Bottomwear').filter(discounted_price__gt=10)
    return render(request,'bottomwear.html',{'bottomwears':bottomwear})

@login_required(login_url='/login/')
def orders(request):
    user = request.user
    order = Order_placed.objects.filter(user=user)
    return render(request,'orders.html',{'orders':order})

@login_required(login_url='/login/')
def Carts(request):
    user = request.user
    amount = 0.0
    shipping = 5
    total = 0.0
    cart = Cart.objects.filter(user=user)
    product_list = [p for p in Cart.objects.all() if p.user == user]
    if product_list:
        for p in product_list:
            tempamt = p.product.discounted_price * p.quantity
            amount += tempamt
        total = amount + shipping
        context ={
        'carts':cart,
        'amount':amount,
        'total':total,
        }
        return render(request,'cart.html',context)
    else:
        
        return render(request,'emptycart.html')

@login_required(login_url='/login/')
def add_cart(request,id=None):
    user = request.user
    if id == None:
        return redirect('cart')
    else:
        product_set = Product.objects.get(id=id)
        instance_exists = Cart.objects.filter(user=user,product=product_set).exists()
        if instance_exists:
            return redirect('cart')
        else:
            form = CartForm()
            cart_instance = form.save(commit=False)
            cart_instance.user = user
            cart_instance.product = product_set
            cart_instance.save()
    cart = Cart.objects.filter(user=user)
    return redirect('cart')

def minus(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity -= 1
        cart.save()
        amount = 0.0
        shipping = 5.0
        total = 0.0
        product_list = [p for p in Cart.objects.all() if p.user == request.user]
        for p in product_list:
            tempamt = p.product.discounted_price * p.quantity
            amount += tempamt
        total =  amount+shipping
        context ={
            'quantity':cart.quantity,
            'amount':amount,
            'total':total
        }
        return JsonResponse({'status':1,'cart_data':context})
    
def plus(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        amount = 0.0
        shipping = 5.0
        total = 0.0
        product_list = [p for p in Cart.objects.all() if p.user == request.user]
        for p in product_list:
            tempamt = p.product.discounted_price * p.quantity
            amount += tempamt
        total =  amount+shipping

        context ={
            'quantity':cart.quantity,
            'amount':amount,
            'total':total
        }
        return JsonResponse({'status':1,'cart_data':context})
    
def remove(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.delete()
        items = Cart.objects.filter(user = request.user)
        amount = 0.0
        shipping = 5.0
        total = 0.0
        product_list = [p for p in Cart.objects.all() if p.user == request.user]
        for p in product_list:
            tempamt = p.product.discounted_price * p.quantity
            amount += tempamt
        total = shipping+amount
        context={
            'amount':amount,
            'total':total,
        }
        return JsonResponse({'status':1,'cart_data':context})
    
@login_required(login_url='/login/')   
def checkout(request):
    products = Cart.objects.filter(user=request.user)
    addersses = Customer.objects.filter(user=request.user)
    amount = 0.0
    shipping = 5.0
    total = 0.0
    product_list = [p for p in Cart.objects.all() if p.user == request.user]
    for p in product_list:
        tempamt = p.product.discounted_price * p.quantity
        amount += tempamt
    total = shipping+amount
    context={
        'products':products,
        'addresses':addersses,
        'total':total,
    }
    return render(request,'checkout.html',context)

@login_required(login_url='/login/')
def buy(request,id):
    product = Product.objects.filter(id=id).first()
    Cart(user=request.user,product=product).save()
    return redirect('checkout')

@login_required(login_url='/login/')
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    print("ID",custid)
    customer = Customer.objects.filter(id=custid).first()
    print("customer",customer)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order_placed(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')