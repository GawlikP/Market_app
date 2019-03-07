from django.shortcuts import render

from django.http import HttpResponse

def index(response):

    context = {
        'title' : 'Main'
    }

    return render(response,'main.html',context)

def sing_up(response):

    username_error = None
    password_error = None
    cpassword_error = None

    if response.POST:
        usr = response.POST.get('username','')
        psw = response.POST.get('password','')
        cpsw = response.POST.get('cpassword','')
        if usr == None or psw == None or cpsw == None:
            username_error = 'Pls fill it up'
            password_error = 'Pls fill it up'
            cpassword_error = 'Pls fill it up'
        else:
            if psw != cpsw:
                cpassword_error = 'It\'s not the same as up';
            else:
                print(usr)
                print(psw)
                print(cpsw)

    context = {
        'username_error' : username_error,
        'password_error': password_error,
        'cpassword_error': cpassword_error,
        'title': 'Sing Up'
    }

    return render(response,'sing_up.html',context)
