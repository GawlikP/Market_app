from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth.hashers import make_password, check_password

from .models import User

from .psValidator import PSWvalid

def index(response):

    context = {
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


    return render(response,'login.html')
