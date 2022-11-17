import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from carmed.forms import Retail_info
from carmed.models import Business


def home(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def signUser(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['phone']
        pswd1 = request.POST['pswd1']
        pswd2 = request.POST['pswd2']

        user_create = User.objects.create_user(username, lname, pswd1)
        user_create.first_name = fname
        user_create.last_name = lname

        user_create.save()

        messages.success(request, "Successfully created account.")

        return redirect('login')
    return render(request, 'user_register.html')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == 'POST':
        phone = request.POST['phone']
        pswd1 = request.POST['pswd1']

        user_login = authenticate(username=phone, password=pswd1)
        print(user_login)
        if user_login:
            login(request, user_login)
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect!!")
            return redirect('login')
    return render(request, 'user_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def shop_register(request):
    if request.method == 'POST':
        # make requests from api.ipify.org
        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        # make requests from ip-api.com
        res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
        data_one = json.loads(res.text)

        ret = Business(name=request.POST["fullname"], business_name=request.POST["businessname"], email=request.POST["email"], phone_number=request.POST["phone"],
                       business_type=request.POST["businesstype"], latitude=data_one['lat'], longitude=data_one['lon'], city=request.POST['inputCity'], district=request.POST["inputDistrict"], sector=request.POST["inputSector"])
        ret.save()
        return HttpResponse('Successfully registered your business')

    else:
        form = Retail_info()

    return render(request, 'shop_register.html', context={'form': form})


@login_required(login_url='login')
def map(request):
    return render(request, "map.html")
