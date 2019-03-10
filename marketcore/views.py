from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.hashers import make_password, check_password

from .models import User, Type, Product, Message

from .psValidator import PSWvalid
from .my_messages_constants import *

from .forms import UploadFileForm

from decimal import *

def index(response):

    user_name = None
    user_id = None
    products = None
    types_filter = 0;
    max_price = 0
    min_price = 0
    alert = None

    if response.session.get('user_id'):
        usr = User.objects.get(pk=response.session.get('user_id'))
        user_name = usr.username
        user_id = usr.id

    if response.session.get('alert'):
        alert = response.session.get('alert')
        try:
            del response.session['alert']
        except KeyError:
            pass

    if response.POST:
        type_filter = response.POST.get('type_filter','')
        min_price = response.POST.get('min_price','')
        max_price = response.POST.get('max_price','')
        response.session['type_filter'] = type_filter;
        response.session['min_price'] = min_price
        response.session['max_price'] = max_price
    if response.session.get('type_filter'):
        if response.session.get('type_filter') != '0':
            types_filter = int(response.session.get('type_filter'))
            type = Type.objects.get(id= response.session.get('type_filter'))
            products = Product.objects.all().filter(type=type);
        else: products = Product.objects.all()
    else: products = Product.objects.all()


    if response.session.get('min_price'):
        min_price = float(response.session.get('min_price'))
        print(min_price)
        products = products.filter(price__gt=min_price)
    if response.session.get('max_price'):
        max_price = float(response.session.get('max_price'))
        print(max_price)
        products = products.filter(price__lt=max_price)

    types = Type.objects.all()

    products = products.filter(buyer__isnull=True)

    context = {
        'alert' : alert,
        'min_price': min_price,
        'max_price': max_price,
        'types_filter': types_filter,
        'types': types,
        'products': products,
        'user_id': user_id,
        'user_name': user_name,
        'title' : 'Main'
    }

    return render(response,'main.html',context)

def sing_up(response):

    username_error = None
    password_error = None
    cpassword_error = None
    user = None
    usr = None
    psw = None
    cpsw = None

    if response.POST:
        usr = response.POST.get('usernameinput','')
        psw = response.POST.get('password','')
        cpsw = response.POST.get('cpassword','')
        if usr == None or psw == None or cpsw == None:
            username_error = 'Pls fill it up'
            password_error = 'Pls fill it up'
            cpassword_error = 'Pls fill it up'
        if not User.objects.filter(username=usr):
            out = PSWvalid(psw)
            if out != 'Its fine':
                password_error = out
            else:
                if psw != cpsw:
                    cpassword_error = 'It\'s not the same as up';
                else:
                    psw = make_password(psw)
                    user = User.objects.create(username= usr,password= psw)
                    user = user.username
        else:
            username_error = 'User already exist'


    context = {
        'usr':usr,
        'psw': psw,
        'cpsw': cpsw,
        'user': user,
        'username_error' : username_error,
        'password_error': password_error,
        'cpassword_error': cpassword_error,
        'title': 'Sing Up'

    }

    return render(response,'sing_up.html',context)

def log_in(response):

    error_message = None
    usr = None

    if response.POST:
        usr = response.POST.get('usernameinput','')
        psw = response.POST.get('passwordinput','')
        print(usr)
        if not User.objects.filter(username= usr):
            error_message = 'There is no user with that username'
        else:
            user = User.objects.get(username= usr)
            if check_password(psw,user.password):
                response.session['user_id'] = user.pk;
                print('logged')
                return HttpResponseRedirect('/')
            else:
                error_message = 'Unknow combination'
    context = {
        'error_message': error_message,
        'title': 'User Form',
    }

    return render(response,'login.html',context)
def log_out(response):
    try:
        del response.session['user_id']
        del response.session['type_filter']
        del response.session['min_price']
        del response.session['max_price']
    except KeyError:
        pass
    return HttpResponseRedirect("/")

def profile(response,id):

    user = None
    unlock = False

    if not User.objects.filter(id= id):
        return HttpResponse('Error there is no user with' + id + " id");
    else:
        if not response.session['user_id']:
            return HttpResponse('You are not logged');
        else:
            user = User.objects.get(id= id)
            uuser = User.objects.get(pk= response.session.get('user_id'))
            if uuser == user:
                unlock = True

    context = {
        'unlock': unlock,
        'user': user,
        'title': 'Profile'
    }

    return render(response,'profile.html',context)

def add_product(response):

    types = None
    error_message = None

    if not response.session['user_id']:
        return HttpResponse('You need to be loged in');
    else:
        if response.method == 'POST' and response.FILES['myfile']:
            print('post geted')
            print('form too')
            name = response.POST.get('productnameinput','')
            description = response.POST.get('productdescriptioninput','')
            if response.POST.get('typeinput','') != 'Type':
                type = response.POST.get('typeinput','')
                quality = response.POST.get('quialityinput','')
                myfile = response.FILES['myfile']
            # =request.FILES['file']
                price = response.POST.get('pricefield')
                price = float(price)
                type = Type.objects.get(id=type);
                seller = User.objects.get(id=response.session.get('user_id'))
                product = Product.objects.create(name=name,type=type,description= description, quality='NEW',price=price, seller=seller,image=myfile)
                print(product)
                product.save()
                print(name)
                print(description)
                print(type)
                print(quality)
                print(price)
                if product:
                    return HttpResponseRedirect('/add_product_success/')
            else:
                error_message = "Choose type !"
                print(error_message)

    types = Type.objects.all();

    context = {
        'error_message': error_message,
        'types': types,
        'title': 'Adding product'
    }


    return render(response,'add_product.html',context)

def add_product_success(response):


    context = {
        'title': 'Success !'
    }

    return render(response,'add_product_success.html',context)

def buy_product(response,id):

    user_name = None
    user_id = None

    if response.session.get('user_id'):
        usr = User.objects.get(pk=response.session.get('user_id'))
        user_name = usr.username
        user_id = usr.id
    else:
        response.session['alert'] = 'You need to be loged in to buy product'
        return HttpResponseRedirect('/')

    product = Product.objects.get(id= id);


    context = {
        'product': product,
        'user_name': user_name,
        'title':'Buy'
    }

    return render(response,'buy_product.html',context)

def buy_accept(response,id):


    user_id = None
    usr = None
    error = None

    if response.session.get('user_id'):
        usr = User.objects.get(pk=response.session.get('user_id'))
        user_id = usr.id
    else:
        response.session['alert'] = 'You need to be loged in to buy product'
        return HttpResponseRedirect('/')

    product = Product.objects.get(id= id)

    if user_id == product.seller.id:
        response.session['alert'] = 'You can not buy your own product'
        return HttpResponseRedirect('/')

    if response.POST:
        password = response.POST.get('password')
        if check_password(password,usr.password):
            product = Product.objects.get(id= id)
            seller = product.seller
            product.buyer= usr;
            product.save()
            msg = Message.objects.create(title=MM_title_generator(product),content=MM_content_generator(seller.username,product),to=product.buyer,mailer=seller)
            print('yep its him')
            msg2 = Message.objects.create(title=MM_Stitle_generator(product),content=MM_Scontent_generator(product.buyer,product),to=seller,mailer=product.buyer)
            context = {
                'th':True,
                'title':'Buy'
            }
            return render(response,'buy_accept.html',context)
        else:
            error = "Wrong Password !"
    context = {
        'error': error,
        'title':'Buy'
    }

    return render(response,'buy_accept.html',context)

def messeges(response):

    if response.session.get('user_id'):
        usr = User.objects.get(pk=response.session.get('user_id'))
        user_id = usr.id
        user_name = usr.username
    else:
        response.session['alert'] = 'You need to be loged in to check your messeges'
        return HttpResponseRedirect('/')

    messages = Message.objects.all().filter(to=usr)


    context = {
        'messages': messages,
        'user_name': user_name,
        'title':'Messeges'
    }

    return render(response,'messeges.html',context)
