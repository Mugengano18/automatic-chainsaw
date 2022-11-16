from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

# Create your views here.


def home(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def shop_register(request):
    return render(request, "shop_register.html")


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


@login_required(login_url='login')
def map(request):
    return render(request, "map.html")
