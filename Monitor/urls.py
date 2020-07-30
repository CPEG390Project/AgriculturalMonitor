"""Monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from MonitorApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #The Welcome page, where you first land
    path('',  views.landing, name='landing'),
    #The Home Page
    path('home', views.home, name='home'),
    #The base for banner
    path('base', views.base, name='base'),
    #The Auth [sign up, sing out and sign in]
    path('signupuser', views.signupuser, name='signupuser'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('loginuser', views.loginuser, name='loginuser'),
    

    
    #The Choice Pages
    #The three results of the choice
    path('testChoice', views.testChoice, name='testChoice'),
    
    
    
    #The error handle page
    path('error', views.error, name='error'),
    path('erroruser', views.erroruser),
    path('errorpassword', views.errorpassword),
    path('loginerror', views.loginerror),
    #The logged out page
    path('loggedout', views.loggedout, name = 'loggedout'),
    
    #The LED
    path('ajax/led_checking/', views.led_checking, name='led_checking'),
    
    
]
