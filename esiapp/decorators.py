from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('esiapp:admin_home')
            else:
                return redirect('esiapp:user_home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_doctorant or request.user.is_teacher:
                return redirect('esiapp:page_introuvable')
            elif request.user.is_admin:
                return redirect('esiapp:admin_home')
            else:
                return redirect('esiapp:logout')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
