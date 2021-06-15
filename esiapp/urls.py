from django.urls import path
from . import views

app_name = "esiapp"

urlpatterns = [
    path('home/', views.homeAdmin, name='admin_home'),
    path('', views.homeUser, name="user_home"),
    path('login/', views.loginPage, name='login'),
    path('login/loggedin/', views.admin_login_custom, name="admin_login_custom"),
    path('nouvelle_publication/', views.new_publication, name='new_publication'),
    path('pubs/nouvelle_publication/', views.ajouter_publication, name="ajouter_publication"),
    path('delete/<int:item_id>/', views.delete_publication, name="delete_publication")
]
