from django.shortcuts import render


def login(request):
    context = {}
    return render(request, 'login_page.html', context)
