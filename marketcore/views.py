from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.hashers import make_password, check_password

from .models import User, Type, Product

from .psValidator import PSWvalid

from .forms import UploadFileForm

def index(response):

    user_name = None
    user_id = None

    if response.session.get('user_id'):
        usr = User.objects.get(pk=response.session.get('user_id'))
        user_name = usr.username
        user_id = usr.id

    context = {
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
    context = {
        'error_message': error_message,
        'title': 'User Form',
    }

    return render(response,'login.html',context)
def log_out(response):
    try:
        del response.session['user_id']
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

    if not response.session['user_id']:
        return HttpResponse('You need to be loged in');
    else:
        if response.method == 'POST' and response.FILES['myfile']:
            print('post geted')
            print('form too')
            name = response.POST.get('productnameinput','')
            description = response.POST.get('productdescriptioninput','')
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

    types = Type.objects.all();

    context = {

        'types': types,
        'title': 'Adding product'
    }


    return render(response,'add_product.html',context)

def add_product_success(response):


    return HttpResponse('<h1> Success ! </h1>')
