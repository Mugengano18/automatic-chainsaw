import folium
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm

from carmed.forms import Retail_info
from carmed.models import Business, service_detail  


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

        user_create = User.objects.create_user(username," ", pswd1)
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

        if user_login is not None:
            login(request, user_login)
            return redirect('home')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Username or password incorrect!!")
            return redirect('login')
    return render(request, 'user_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required(login_url='login')
def service(request):
        if request.method == 'POST':
            request_sender =request.POST.get('request_by')
            phone_n = request.POST.get('number')
            service_type = request.POST.get('service_type')
            description = request.POST.get('description')
            obj = service_detail()
            obj.service_type = service_type
            obj.request_sender = request_sender
            obj.phone_number = phone_n
            obj.description = description
            print(service_type)
            print(description)
            obj.save()

            return redirect('req_details')
        return render(request, "service.html")


def request_det(request):

    return render(request,"request_details.html")











def shop_register(request):
    if request.method == 'POST':
        # make requests from api.ipify.org
        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        # make requests from ip-api.com
        res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
        data_one = json.loads(res.text)

        ret = Business(name=request.POST["fullname"], business_name=request.POST["businessname"],
                       email=request.POST["email"], phone_number=request.POST["phone"],
                       business_type=request.POST["businesstype"], latitude=data_one['lat'], longitude=data_one['lon'],
                       city=request.POST['inputCity'], district=request.POST["inputDistrict"],
                       sector=request.POST["inputSector"])
        ret.save()
        # return HttpResponse('Successfully registered your business')
        return redirect('details')
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
    district = i["district"]
    sector = i["sector"]
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
    <td style="width: 150px;background-color: """ + right_col_color + """;">""" + business_type + """</td>
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Phone Number: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">""" + phone_number + """</td>
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">City: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">""" + city + """</td>
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">District: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">""" + district + """</td>
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Sector: </span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">""" + sector + """</td>
    </tr>
    </tbody>
    </table></center>
    </html>
    """
    return html


@login_required(login_url='login')
def map_location(request):
    # make requests from api.ipify.org
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    # make requests from ip-api.com
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    data_one = json.loads(res.text)
    map1 = folium.Map(location=[-1.952183, 30.054957], zoom_start=10, tiles='OpenStreetMap')
    folium.Marker([-1.9499, 30.0588], tooltip='Click for more', popup=data_one["city"],
                  icon=folium.Icon(color="red", icon='home', prefix='fa')).add_to(map1)
    data_list = Business.objects.all().values()
    for i in range(len(data_list)):

        bus_type = data_list[i]['business_type']
        if bus_type == 'Gas station':
            color = 'orange'
        elif bus_type == 'repair shop':
            color = 'gray'
        else:
            color = 'black'
        html = popup_html(data_list[i])
        popup = folium.Popup(folium.Html(html, script=True), max_width=500)
        labels = data_list[i]['business_name']
        lat = data_list[i]['latitude']
        long = data_list[i]['longitude']
        sector = data_list[i]['sector']
        folium.Marker([lat, long], tooltip='Click for more', popup=popup,
                      icon=folium.Icon(color=color, icon='car', prefix='fa')).add_to(map1)
    map1 = map1._repr_html_()

    context = {
        'map1': map1,
    }
    return render(request, "map.html", context)


def business_details(request):
    if request.method == 'POST':
        stat_id = request.POST.get('s_id')
        stat_id_2 = request.POST.get('f_id')
        print(stat_id_2)
        service_detail.objects.filter(services_id=stat_id_2).update(
            status="2")
        service_detail.objects.filter(services_id=stat_id_2).update(
            status="3")
    request_list = service_detail.objects.all()
    status_open = service_detail.objects.filter(status = "1")
    status_active = service_detail.objects.filter(status = "2")
    status_finished = service_detail.objects.filter(status = "3")
    print(status_finished)
    context = {'info': request_list,"status_open":status_open,"status_active":status_active,"status_finished":status_finished}
    return render(request, "service_provider_dashboard.html",context)

def business_details_id(request, pk):
    service_one = service_detail.objects.get(id=pk)

    return render(request, 'service_provider_dashboard.html', {'service': service_one})


