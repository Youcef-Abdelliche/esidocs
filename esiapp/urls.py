from django.urls import path
from . import views

app_name = "esiapp"

urlpatterns = [
    path('', views.homeAdmin, name='home'),
    path('login/', views.loginPage, name='login'),
    path('login/loggedin/', views.admin_login_custom, name="admin_login_custom")
]
