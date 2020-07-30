#General libs
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

#These here are needed for the login process
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

#These are required for the SENOSR PROJECT
from .models import EnvironmentData
from django.http import JsonResponse
import random
import sys
import urllib
from urllib.request import urlopen
#Raspberry and Sensors libs
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT as dht
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#The Physical Pins/Variables
#LEDs pin
LED_RED = 20
LED_GREEN = 21
GPIO.setwarnings(False)
GPIO.setup(LED_RED, GPIO.OUT, initial= GPIO.LOW)
GPIO.setwarnings(False)
GPIO.setup(LED_GREEN, GPIO.OUT, initial= GPIO.LOW)
#DHT DATA pin
DHT = 4
#BMP180 Set
Sensor = BMP085.BMP085()
#Set DefaultTemp
maxTemp = 100;

# Create your views here.

#This is the method to fetch the start/landing page
def landing(request):
    return render(request, 'Monitor/landing.html')
          
#The home webpage
@login_required   
def home(request):
    return render(request, 'Monitor/home.html')
    
#The base banner
def base(request):
    return render(request, 'Monitor/base.html')

    
#The Authentication Cluster
#This is the signup page
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'Monitor/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return erroruser(request)
        else:
            return errorpassword(request)
            
#The logout page
@login_required
def logoutuser(request):
   if request.method == 'POST':
       logout(request)
       return redirect('loggedout')
    
#The login page
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'Monitor/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            return render(request, 'Monitor/loginerror.html')
        else:
            login(request, user)
            return redirect('home')

#The Errors
#The undefined error page
def error(request):
    return render(request, 'Monitor/error.html')
#The specified errors
def erroruser(request):
    return render(request, 'Monitor/erroruser.html')
def errorpassword(request):
    return render(request, 'Monitor/errorpassword.html')
def loginerror(request):
    return render(request, 'Monitor/loginerror.html')   
#The exit page
def loggedout(request):
    return render(request, 'Monitor/loggedout.html')


#The Raspberry Codes
def BMP180_data():
    pres = float(format(Sensor.read_pressure()))  # The local pressure
    return pres

def DHT22_data():
    # Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT22, DHT)
    #Temp from C to F
    return humi, temp

def led_checking(request):
    global maxTemp
    temp_val= request.GET.get('temp_value',None)
    maxTemp = float(temp_val)
    GPIO.setwarnings(False)
    GPIO.setup(LED_RED, GPIO.OUT, initial= GPIO.LOW)
    GPIO.setwarnings(False)
    GPIO.setup(LED_GREEN, GPIO.OUT, initial= GPIO.LOW)
    data = {"message":"yes"}
    return JsonResponse(data)
    
def testChoice(request):
    Environment_Data = EnvironmentData.objects.all()
    #Read Temp and Hum from DHT22
    humi,temp = DHT22_data()
    pres = BMP180_data()

    #Print Temperature and Humidity on Shell window
    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temp,humi))

    #Print Pressure
    print ('Pressure={0:0.2f}Pa'.format(pres))

    #Led green if Temp < maxTemp and Red if Temp > maxTemp
    print(maxTemp)

    if (temp<maxTemp):
        print('green')
        GPIO.output(LED_GREEN,GPIO.HIGH)
    else :
        print('red')
        GPIO.output(LED_RED,GPIO.HIGH)

    EnvironmentData.objects.create(
                    temperature='{0:0.2f}*C'.format(temp),
                    humidity = '{0:0.2f}%'.format(humi),
                    pressure='{0:0.2f}Pa'.format(pres)

                )

    return render(request,'Monitor/testChoice.html',{'Environment_Data':Environment_Data})
