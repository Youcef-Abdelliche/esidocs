from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages


def loginPage(request):
    context = {}
    return render(request, 'login_page.html', context)


def homeAdmin(request):
    list = ['element1', 'element2', 'element3']
    return render(request, 'admin/home_page_admin.html', {'list': list})


def admin_login_custom(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        if user.is_admin:
            messages.info(request, "admin authentifié")
            print("Bonjour" + user.email)
            return redirect('esiapp:login')
        # if user.is_teacher:
        #     messages.info(request, "enseignant authentifié")
        #     return redirect('esiapp:login')
        else:
            messages.info(request, "Bonjour" + user.email)
            print("Bonjour"+user.email)
            return redirect('esiapp:home')
    else:
        messages.warning(request, "Utilisateur n'existe pas")
        print("Utilisateur n'existe pas")
        return redirect('esiapp:login')
