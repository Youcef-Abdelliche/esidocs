from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Publication, User


def loginPage(request):
    context = {}
    return render(request, 'login_page.html', context)


def homeAdmin(request):
    publications = Publication.objects.filter()
    if request.user.is_authenticated:
        user = request.user
    return render(request, 'admin/home_page_admin.html', {'list': publications, 'user': user})


def homeUser(request):
    publications = Publication.objects.filter()
    if request.user.is_authenticated:
        user = request.user
    return render(request, 'user/home_page_user.html', {'list': publications, 'user': user})


def admin_login_custom(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        if user.is_admin:
            messages.info(request, "admin authentifié")
            print("admin authentifié: " + user.email)
            return redirect('esiapp:admin_home')
        if user.is_teacher or user.is_doctorant:
            messages.info(request, "enseignant/doctorant authentifié")
            print("enseignant/doctorant authentifié: " + user.email)
            return redirect('esiapp:user_home')
    else:
        messages.warning(request, "Utilisateur n'existe pas")
        print("Utilisateur n'existe pas")
        return redirect('esiapp:login')


