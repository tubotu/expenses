from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="app/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("chartjs/", views.chartjs, name="chartjs"),
    path(
        "api/index/get_itemList/", views.ajax_get_itemList, name="ajax_get_itemList"
    ),  # URLは何でもいい
    path(
        "api/index/get_category/", views.ajax_get_category, name="ajax_get_category"
    ),  # URLは何でもいい
]
