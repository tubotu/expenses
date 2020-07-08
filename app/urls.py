from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="app/login.html"),
        name="login",
    ),
    path("big/category/new/", views.big_category_new, name="big_category_new"),
    path("small/category/new/", views.small_category_new, name="small_category_new"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("item/new/", login_required(views.PostCreate.as_view()), name="item_new"),
    path("graph/", login_required(views.Graph.as_view()), name="graph"),
    path("api/category/get/", views.ajax_get_category, name="ajax_get_category"),
    path("api/item/get", views.ajax_get_item, name="ajax_get_item"),  # URLは何でもいい
]
