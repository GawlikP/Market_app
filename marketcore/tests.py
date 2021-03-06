from django.test import TestCase

# Create your tests here.

import unittest

from django.test import Client
from .models import User
from django.contrib.auth.hashers import make_password

class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(username='test',password='1234')
        User.objects.create(username='test2',password='3213')
        self.users = User.objects.all();

    def test_details(self):
        for u in self.users:
            response = self.client.get('/profile/'+str(u.id)+'/')
            self.failUnlessEqual(response.status_code,200)
        #response = self.client.get('/profile/1/')
        #self.failUnlessEqual(response.status_code,200)
class SingUpTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_SingUp(self):
        users = User.objects.all().count()
        response = self.client.post('/sing_up/',{'usernameinput':'name','password':'password','cpassword':'passsword'})
        self.failUnlessEqual(response.status_code,200)
        users2 = User.objects.all().count()
        self.failUnlessEqual(users,users2)
        response = self.client.post('/sing_up/',{'usernameinput':'name','password':'Password123','cpassword':'Password123'})
        users2 = User.objects.all().count()
        self.failUnlessEqual(users+1,users2)

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(username="test",password=make_password('test'))

    def test_Login(self):
        #users = User.objects.all()
        response = self.client.post('/log_in/',{'usernameinput':'test','passwordinput':'tt'})
        self.failUnlessEqual(response.status_code,200)
        response = self.client.post('/log_in/',{'usernameinput':'test','passwordinput':'test'})
        self.failUnlessEqual(response.status_code,302)
