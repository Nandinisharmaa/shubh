from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from shop.models import Profile, Product, Customer, Cart, OrderPlaced
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import CustomerProfileform
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# from django.contrib.auth.decorators import @login_required


# Create your views here.
def base(request):
    return render(request, 'base.html')


def login_attemp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_ob = User.objects.filter(username=username).first()
        if user_ob is None:
            messages.success(request, 'User not found.')
            return redirect('/login')

        profile_ob = Profile.objects.filter(user=user_ob).first()
        if not profile_ob.is_verified:
            messages.success(request, 'Your profile is not verified, Please check your email.')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong Password.')
            return redirect('/login')
        login(request, user)
        return redirect('/profile')
    return render(request, 'login.html')


def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is already Exist.')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Username is already Exist.')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            send_mail_after_registration(email, auth_token)
            messages.success(request, "your account is created successfully")
            return redirect('/token')

        # return HttpResponse("<script>alert(' We hav' ); window.location.href=''</script>")
        except Exception as e:
            print(e)

    return render(request, 'register.html')


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token.html')


# def MyMail(email, token):

# send_mail('subject', 'body message here', 'nandinisharma713@gmail.com', ['nandinisharma6392@gmail.com'],
# fail_silently=False)
def send_mail_after_registration(email, token):
    subject = "Your account need to be verify"
    message = f'hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message=message, from_email=from_email, recipient_list=recipient_list)


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your Email is already verified')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your Email has been verified')
            return redirect('/login')
        else:
            return HttpResponse("<script>alert('Error');</script>")
    except Exception as e:
        print(e)


def base1(request):
    """if 'search' in request.GET:
       search=request.GET['search']
       finds=Product.objects.filter(title_icontains=search)
    else:
        finds=Product.objects.all()"""
    return render(request, 'base1.html')


def search(request):
    if request.method=="POST":
        search=request.POST['search']
        items=Product.objects.filter(title__contains='search')
    return render(request, 'search.html',{'search':search,'items':items})


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        women_wear = Product.objects.filter(category='W')
        kid_wear = Product.objects.filter(category='K')
        electronic = Product.objects.filter(category='E')
        accessories = Product.objects.filter(category='A')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'home.html',
                      {'topwear': topwear, 'bottomwear': bottomwear, 'mobiles': mobiles, 'laptop': laptop,
                       'women_wear': women_wear, 'kid_wear': kid_wear, 'electronic': electronic,
                       'accessories': accessories, 'totalitem': totalitem})


class ProductDetailVeiw(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'productdetail.html',
                      {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


def Mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Realme' or 'Oneplus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'Above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'Mobile.html', {'mobiles': mobiles})


# @login_required(login_url="/login/")
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        products = Product.objects.get(id=product_id)
        cart_data = Cart(user=user, product=products)
        cart_data.save()
        return redirect('/show_cart')
    else:
        return HttpResponse(
            "<script>alert('First login then add the product into cart');window.location.href='/login'</script>")


# @login_required(login_url="/login/")
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'addtocart.html',
                          {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem': totalitem})
        else:
            return render(request, 'emptycart.html')
    else:
        return HttpResponse("<script>alert('First login then buy product ');window.location.href='/login'</script>")


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }
        return JsonResponse(data)


def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        c.delete()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }
        return JsonResponse(data)


@login_required
def check(request):
    totalitem = 0
    user = request.user
    if user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
    totalamount = amount + shipping_amount
    return render(request, 'checkout.html',
                  {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("/order")


# @login_required(login_url="/login/")
def order(request):
    if request.user.is_authenticated:
        op = OrderPlaced.objects.filter(user=request.user)
        return render(request, 'order.html', {'orderplaced': op})
    else:
        return HttpResponse("<script>alert('first login ');window.location.href='/login'</script>")


@login_required(login_url="/login/")
def address(request):
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.filter(user=request.user)
        effect = {'addr': 'active'}
    return render(request, 'address.html', {'add': add, 'effect': effect, 'totalitem': totalitem})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            form = CustomerProfileform()
            effect = {'pro': 'active'}
            return render(request, 'profile.html', {'form': form, 'effect': effect, 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileform(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            udata = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
            udata.save()
            messages.success(request, 'Congratulatoins! Profile updated')
            return render(request, 'profile.html', {'form': form, 'effect': 'effect'})


"""
def profile(request):
    return render(request, 'profile.html')"""
