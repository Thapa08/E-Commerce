from django.urls import path,include
from . import views
urlpatterns = [

    path('', views.home,name='home'),
    path('register/', views.registration,name='register'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('profile/', views.profile,name='profile'),
    path('address/', views.address,name='address'),
    path('orders/', views.orders,name='orders'),
    path('change/', views.change_password,name='change_password'),
    path('product/<int:id>', views.product_detail,name='product'),
    path('smartphones/', views.smartphones,name='smartphones'),
    path('smartphones/<slug:data>', views.smartphones,name='phonedata'),
    path('laptops/', views.Laptops,name='laptops'),
    path('laptops/<slug:data>', views.Laptops,name='laptopdata'),
    path('topwears/', views.Topwears,name='topwears'),
    path('topwears/<slug:data>', views.Topwears,name='topweardata'),
    path('bottomwears/', views.Bottomwears,name='bottomwears'),
    path('bottomwears/<slug:data>', views.Bottomwears,name='bottomweardata'),
    path('cart/', views.Carts,name='cart'),
    path('add_cart/<int:id>', views.add_cart,name='add_cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('paymentdone/', views.paymentdone,name='paymentdone'),
    path('buy/<int:id>', views.buy,name='buy'),

# AJAX
    path('minus/', views.minus,name='minus'),
    path('plus/', views.plus,name='plus'),
    path('remove/', views.remove,name='remove'),
]
