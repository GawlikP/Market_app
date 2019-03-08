from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.hashers import make_password, check_password

from .models import User

from .psValidator import PSWvalid

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

    if not User.objects.filter(id= id):
        return HttpResponse('Error there is no user with' + id + " id");
    else:
        user = User.objects.get(id= id)

    context = {
        'user': user,
        'title': 'Profile'
    }

    return render(response,'profile.html',context)

def add_product(response):


    return HttpResponse('Add product')
