from django.urls import path, include
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('', views.index, name='index'),
     path('shop', views.shop, name='shop'),
     path('product-detail/<int:pk>', views.productDetail, name='product-detail'),

     path('register', views.register, name='register'),
     path('login', views.login, name='login'),
     path('logout', views.logout_user, name='logout'),
     path('acount', views.account, name='account'),

#     path('cart', views.cart, name='cart'),
     path('checkout', views.checkout, name='checkout'),
     # path('wish', views.wish, name='wish'),
     # for cart
     path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
     path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
     path('cart/item_increment/<int:id>/',
          views.item_increment, name='item_increment'),
     path('cart/item_decrement/<int:id>/',
          views.item_decrement, name='item_decrement'),
     path('cart_clear/', views.cart_clear, name='cart_clear'),
     path('cart-detail',views.cart_detail,name='cart_detail'),

     path('email',views.email,name='email'),
     path('payment',views.payment,name='payment'),
     path('accounts/', include('allauth.urls')),
     
]

if settings.DEBUG:
     urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
