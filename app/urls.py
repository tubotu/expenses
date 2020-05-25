from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "app"
<<<<<<< HEAD

=======
>>>>>>> 2e536c5c9c8ba1e6aaac3b665c67a644444cf175
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="app/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
<<<<<<< HEAD
    path("chartjs/", views.chartjs, name="chartjs"),
    path(
        "api/index/get_itemList/", views.ajax_get_itemList, name="ajax_get_itemList"
    ),  # URLは何でもいい
    path(
        "api/index/get_category/", views.ajax_get_category, name="ajax_get_category"
    ),  # URLは何でもいい
]
=======
    path("graph_outgo/", views.graph_outgo, name="graph_outgo"),
    path("popup_table/<int:point_id>/", views.popup_table, name="popup_table"),
]

>>>>>>> 2e536c5c9c8ba1e6aaac3b665c67a644444cf175
