import folium
import geocoder
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from folium import plugins

from carmed.forms import Retail_info, SearchForm
from carmed.models import Business, Search


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
        print("ip data", ip_data)
        print("data_one", data_one)

        ret = Business(name=request.POST["fullname"], business_name=request.POST["businessname"],
                       email=request.POST["email"], phone_number=request.POST["phone"],
                       business_type=request.POST["businesstype"], latitude=data_one['lat'], longitude=data_one['lon'],
                       city=request.POST['inputCity'], district=request.POST["inputDistrict"],
                       sector=request.POST["inputSector"])
        ret.save()
        return HttpResponse('Successfully registered your business')

    else:
        form = Retail_info()

    return render(request, 'shop_register.html', context={'form': form})


@login_required(login_url='login')
def map_location(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/map')
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    data_list = Business.objects.values_list('latitude', 'longitude')
    location = geocoder.osm(address)
    lat = Business.objects.values_list('latitude')[0][0]
    long = Business.objects.values_list('longitude')[0][0]
    sector = Business.objects.values_list('sector')[0][0]
    country = location.country
    if lat is None or long is None:
        address.delete()
        return HttpResponse('Your address input is incorrect')
    map1 = folium.Map(location=[-1.952183, 30.054957], zoom_start=10, tiles='OpenStreetMap')

    pp = folium.Html('<a href="' + "{% url 'details' %}" + '">' + 'View Details' + '</a>', script=True)
    popup = folium.Popup(pp, max_width=2650)
    folium.Marker([lat, long], tooltip='Click for more', popup=popup).add_to(map1)
    # plugins.FastMarkerCluster(data_list, icon='Rwanda',popup=country, tooltip="Click for more",).add_to(map1)

    map1 = map1._repr_html_()

    context = {
        'map1': map1,
        'form': form,
    }
    return render(request, "map.html", context)


def business_details(request):
    return render(request, "details.html")
