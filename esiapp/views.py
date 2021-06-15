from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Publication, User, Category
import datetime
from django.core.mail import send_mail


def loginPage(request):
    context = {}
    return render(request, 'login_page.html', context)


def homeAdmin(request):
    publications = Publication.objects.order_by('-date_ajout')[:3]
    if request.user.is_authenticated:
        user = request.user
    return render(request, 'admin/home_page_admin.html', {'list': publications, 'user': user})


def homeUser(request):
    publications = Publication.objects.order_by('-date_ajout')[:3]
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


def new_publication(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        user = request.user
    return render(request, 'admin/new_publication.html', {'list': categories, 'user': user})


def ajouter_publication(request):
    titre = request.POST['titre']
    message = request.POST['message']
    sendBy = request.POST['sendBy']
    categorie = Category.objects.filter(nom_categorie=request.POST['categorie_op'])[0]
    contenu = request.POST['contenu']
    date_limite = datetime.datetime.strptime(request.POST['date_limite'], "%Y-%m-%d").date()
    file = request.POST['file']

    pub = Publication(titre=titre, message=message, send_By=sendBy, Categorie=categorie, etat_publication=True,
                      priorite_contenu=contenu, date_limite=date_limite)
    pub.save()

    publications = Publication.objects.order_by('-date_ajout')[:3]
    if request.user.is_authenticated:
        user = request.user
    recipient_list = ['joseph.london116@gmail.com', 'azizrcb2011@gmail.com']
    send_email(pub, user, recipient_list)
    return render(request, 'admin/home_page_admin.html', {'list': publications, 'user': user})


def send_email(pub, user, recipient_list):
    send_mail(
        pub.titre,
        pub.message,
        from_email='esidocs827@gmail.com',
        auth_password='ogthzi88999%77',
        recipient_list=recipient_list,
        fail_silently=False,
    )
