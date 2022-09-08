from distutils.ccompiler import get_default_compiler
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as loguser
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from cart.cart import Cart

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#Social Auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html" 



# Create your views here.
def index(request):
    products = Product.objects.filter(status=True)
    context = {
        'products': products
        }
    
    return render(request, 'index.html', context)

def shop(request):
    categories = Categorie.objects.all()
    products = Product.objects.filter(status=True)
    brands = Brand.objects.all()
    price_filter = PriceFilter.objects.all()
    pro_len = len(products)
    
    # Filtering Product
    catid = request.GET.get('categoryid')
    p_filter = request.GET.get('p_filter')
    brand_id = request.GET.get('brandid')
    atozid = request.GET.get('ATOZ')
    ztoaid = request.GET.get('ZTOA')
    low_high= request.GET.get('low_high')
    high_low= request.GET.get('high_low')
    new_old= request.GET.get('new_old')
    old_new= request.GET.get('old_new')
    
    if catid:
        products = Product.objects.filter(categorie=catid, status=True)
        pro_len = len(products)
    elif p_filter:
        products = Product.objects.filter(price_filter=p_filter, status=True)
        pro_len = len(products)
    elif brand_id:
        products = Product.objects.filter(brand=brand_id,status=True)
        pro_len = len(products)
    elif atozid:
        products = Product.objects.filter(status=True).order_by('name')
    elif ztoaid:
        products = Product.objects.filter(status=True).order_by('-name')
    elif low_high:
        products = Product.objects.filter(status=True).order_by('price')
    elif high_low:
        products = Product.objects.filter(status=True).order_by('-price')
    elif new_old:
        products = Product.objects.filter(status=True).order_by('-createed_at')
    elif old_new:
        products = Product.objects.filter(status=True).order_by('createed_at')
    else:
        products = Product.objects.filter(status=True)
    
    context = {
        'products': products,
        'pro_len': pro_len,
        'categories': categories,
        'brands': brands,
        'price_filter': price_filter,
    }
    return render(request, 'shop.html', context)

def productDetail(request, pk):
    products = Product.objects.filter(id=pk)
    color = Color.objects.all()
    veriant = Veriant.objects.all()
    all_products = Product.objects.filter(status=True)
    context = {
        'veriant':veriant,
        'color': color,
        'products': products,
        'all_products': all_products,
    }
    
    return render(request, 'single.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email = request.POST.get('email')
        
        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = f_name
        customer.last_name = l_name
        customer.pass1 = pass1
        customer.save()
        return redirect('login')
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            loguser(request, user)
            return redirect('index')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')

# From djnago pip 
@login_required(login_url="login")

def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    
    return redirect("shop")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'cart.html')


# def cart(request):
#     return render(request, 'cart.html')
@login_required(login_url="login")
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        post = request.POST.get('post')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        method = request.POST.get('method')
        
        additional_info = request.POST.get('message')
        s_total = 100
        amount = s_total
        
        new_order = Order(
            user = request.user,
            first_name = first_name,
            last_name = last_name,
            address = address,
            city = city,
            phone = phone,
            email = email,
            amount = amount,
            
        )
        new_order.save()
        
        for i in cart:
            a = cart[i]['quantity']
            b = cart[i]['price']
            total = int(a)*int(b)
            s_total+=total
            item = OrderItem(
                order = new_order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()
        if method == 'bkash':
            return render(request,'bkash.html')
        elif method == 'rocket':
            return render(request,'rocket.html')
        elif method == 'nagad':
            return render(request,'nagad.html')
    return render(request, 'checkout.html')

#Payment
def payment(request):
    if request.method == 'POST':
        user = request.user
        p_number = request.POST.get('p_number')
        p_tra_id = request.POST.get('p_tra_id')
        new_pay = Payment(
            user=user,
            p_number = p_number,
            p_tra_id = p_tra_id
        )
        new_pay.save()
        
        cart = Cart(request)
        cart.clear()        
        
#email option
        user = request.user
        html_content = render_to_string('email.html',{'user': user})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            #Sub
            'Order Confirmation',
            #content
            text_content,
            settings.EMAIL_HOST_USER,
            #Recipient 
            ['samircd4@gmail.com',user.email]
            
        )
        email.attach_alternative(html_content, 'text/html')
        email.send()
        # first_name = 'Samir'
        # s_total = 100
        
        # subject = f'{first_name} placed new order'
        # body = str(s_total)
        # sender = 'imjesual@gmail.com'
        # to = ['samircd4@gmail.com']
        
        
    return render(request, 'thank-you-page.html')
            
        # send_mail(
        #     subject,
        #     body,
        #     sender,
        #     to,
        #     fail_silently=False,
        # )
        
    
        

# def wish(request):
#     return render(request, 'wishlist.html')

def email(request):
    return render(request, 'email.html')

def account(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        # 'profile':profile,
        'orders':orders,
    }
    return render(request, 'account.html', context)

