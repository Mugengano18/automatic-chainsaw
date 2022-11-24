from django.urls import path

from carmed import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('retail_register/', views.shop_register, name="shop_register"),
    path("login/", views.loginUser, name="login"),
    path("signup/", views.signUser, name="signup"),
    path('logout/', views.logoutUser, name="logout"),
    path('map/', views.map_location, name="map"),
    path("details/", views.business_details, name="details")
]
