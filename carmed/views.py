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


def popup_html(row):
    i = row
    name = i["name"]
    business_name = i["business_name"]
    email = i["email"]
    phone_number = i["phone_number"]
    business_type = i["business_type"]
    city = i["city"]
    district =i["district"]
    sector = i["sector"]
    print(name)
    left_col_color = "#3e95b5"
    right_col_color = "#f2f9ff"

    html = """
    <!DOCTYPE html>
    <html>
    <center> <table style="height: 126px; width: 305px;">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Business Name: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">""" + business_name + """</td>
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Business Type: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>"""+ business_type + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Phone Number: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>"""+ phone_number + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">City: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""" + city + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">District: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>"""+ district + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Sector: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>"""+sector + """
    </tr>
    </tbody>
    </table></center>
    </html>
    """
    return html


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
    location = geocoder.osm(address)
    country = location.country
    map1 = folium.Map(location=[-1.952183, 30.054957], zoom_start=10, tiles='OpenStreetMap')
    data_list = Business.objects.all().values()
    for i in data_list:
        bus_type = i["business_type"]
        if bus_type == 'Gas station':
            color = 'orange'
        elif bus_type == 'repair shop':
            color = 'gray'
        else:
            color = 'black'
        html = popup_html(i)
        print(html)
        popup = folium.Popup(folium.Html(html, script=True), max_width=500)
        labels = i["business_name"]
        lat = i["latitude"]
        long = i["longitude"]
        sector = i["sector"]
        folium.Marker([lat, long], tooltip='Click for more', popup=popup, icon=folium.Icon(color=color, icon='car', prefix='fa')).add_to(map1)

    if lat is None or long is None:
        address.delete()
        return HttpResponse('Your address input is incorrect')

    map1 = map1._repr_html_()

    context = {
        'map1': map1,
        'form': form,
    }
    return render(request, "map.html", context)


def business_details(request):
    return render(request, "details.html")
