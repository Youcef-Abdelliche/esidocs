from django.urls import path, include
from . import views

app_name = "esiapp"

urlpatterns = [
    path('home/', views.homeAdmin, name='admin_home'),
    path('', views.homeUser, name="user_home"),
    path('login/', views.loginPage, name='login'),
    path('login/loggedin/', views.admin_login_custom, name="admin_login_custom"),
    path('logout/', views.Logout, name='logout'),
    path('nouvelle_publication/', views.new_publication, name='new_publication'),
    path('pubs/nouvelle_publication/', views.ajouter_publication, name="ajouter_publication"),
    path('delete/<int:item_id>/', views.delete_publication, name="delete_publication"),
    path('publications/edit/<int:item_id>/', views.edit_publication_page, name="edit_publication_page"),
    path('edit/<int:item_id>/', views.edit_publication, name="edit_publication"),
    path('publications/<int:item_id>/', views.display_publication_page_admin, name="display_publication_page_admin"),
    path('publications/<int:item_id>/commentaire/', views.ajouter_commentaire, name="ajouter_commentaire"),
    #path('publication/<int:item_id>/', views.display_publication_page_user, name="display_publication_page_user"),
    path('page_introuvable/', views.page_introuvable, name="page_introuvable"),
    path('catégories/', views.categorie_page, name="categorie_page")
]
