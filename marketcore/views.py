from django.shortcuts import render

from django.http import HttpResponse

def index(response):

    context = {
        'title' : 'Main'
    }

    return render(response,'main.html',context)
