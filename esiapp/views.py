from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import Publication, User, Category, Commentaire, Jury, PublicationFicher
import datetime
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, admin_only
from .enum import wilayas, universities
# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse


@unauthenticated_user
def loginPage(request):
    context = {}
    return render(request, 'login_page.html', context)


@unauthenticated_user
def page_introuvable(request):
    return render(request, 'page_404.html')


@login_required
def homeAdmin(request):
    if request.user.is_doctorant or request.user.is_teacher:
        return render(request, 'page_404.html')

    publications_offres_bources = Publication.objects.filter(Categorie__nom_categorie="Offres de bources",
                                                             etat_publication=True).order_by('-date_ajout')[:3]
    publications_entreprise = Publication.objects.filter(Categorie__nom_categorie="Entreprise",
                                                         etat_publication=True).order_by('-date_ajout')[:3]
    publications_prfu = Publication.objects.filter(Categorie__nom_categorie="Projets de recherches",
                                                   etat_publication=True).order_by('-date_ajout')[:3]
    publications_projet_rech = Publication.objects.filter(Categorie__nom_categorie="PRFU",
                                                          etat_publication=True).order_by('-date_ajout')[:3]
    publications_autres = Publication.objects.filter(Categorie__nom_categorie="Autres",
                                                     etat_publication=True).order_by('-date_ajout')[:3]

    if request.user.is_authenticated:
        user = request.user
    context = {
        'pub_offres_brouces': publications_offres_bources,
        'pub_entreprise': publications_entreprise,
        'pub_prfu': publications_prfu,
        'pub_projet_rech': publications_projet_rech,
        'pub_autres': publications_autres,
        'user': user
    }
    return render(request, 'admin/home_page_admin.html', context)


@login_required
def homeUser(request):
    if request.user.is_admin:
        return render(request, 'page_404.html')

    Publication.objects.all().delete()
    publications_offres_bources = Publication.objects.filter(Categorie__nom_categorie="Offres de bources",
                                                             etat_publication=True).order_by('-date_ajout')[:3]
    publications_entreprise = Publication.objects.filter(Categorie__nom_categorie="Entreprise",
                                                         etat_publication=True).order_by('-date_ajout')[:3]
    publications_prfu = Publication.objects.filter(Categorie__nom_categorie="Projets de recherches",
                                                   etat_publication=True).order_by('-date_ajout')[:3]
    publications_projet_rech = Publication.objects.filter(Categorie__nom_categorie="PRFU",
                                                          etat_publication=True).order_by('-date_ajout')[:3]
    publications_autres = Publication.objects.filter(Categorie__nom_categorie="Autres",
                                                     etat_publication=True).order_by('-date_ajout')[:3]

    if request.user.is_authenticated:
        user = request.user
    context = {
        'pub_offres_brouces': publications_offres_bources,
        'pub_entreprise': publications_entreprise,
        'pub_prfu': publications_prfu,
        'pub_projet_rech': publications_projet_rech,
        'pub_autres': publications_autres,
        'user': user
    }
    return render(request, 'user/home_page_user.html', context)


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

@login_required
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
    file = request.FILES['file']

    emails = request.POST.getlist('list')[0]
    recipient_list = emails.split(',')
    print(recipient_list)

    pub = Publication(titre=titre, message=message, send_By=sendBy, Categorie=categorie, etat_publication=True,
                      priorite_contenu=contenu, editeur=request.user, date_limite=date_limite)
    pub.save()
    pub_file = PublicationFicher(nom_fichier=file, path_fichier=file, publication=pub)
    pub_file.save()

    URL = "https://herokuappdpgr.herokuapp.com/publications/"+str(pub.id)+"/"
    publications = Publication.objects.order_by('-date_ajout')[:3]
    if request.user.is_authenticated:
        user = request.user
    # recipient_list = ['joseph.london116@gmail.com', 'azizrcb2011@gmail.com']
    send_email(pub, user, recipient_list, url=URL)
    return redirect('esiapp:admin_home')


def send_email(pub, user, recipient_list, url):
    msg = "Lien de la publication : "
    send_mail(
        pub.titre,
        pub.message+"\n"+msg+url,
        from_email='esidocs827@gmail.com',
        auth_password='ogthzi88999%77',
        recipient_list=recipient_list,
        fail_silently=False,
    )


@login_required(login_url='login')
def edit_publication_page(request, item_id):
    pub = Publication.objects.filter(id=item_id)[0]
    categories = Category.objects.all()
    print(pub.date_limite)
    date = str(pub.date_limite)
    return render(request, 'admin/modifier_publication.html', {'pub': pub, 'list': categories, 'date': date})


def edit_publication(request, item_id):
    titre = request.POST['titre']
    message = request.POST['message']
    sendBy = request.POST['sendBy']
    categorie = Category.objects.filter(nom_categorie=request.POST['categorie_op'])[0]
    contenu = request.POST['contenu']
    date_limite = datetime.datetime.strptime(request.POST['date_limite'], "%Y-%m-%d").date()

    Publication.objects.filter(id=item_id).update(titre=titre, message=message, send_By=sendBy, Categorie=categorie,
                                                  priorite_contenu=contenu, date_limite=date_limite)

    return redirect('esiapp:admin_home')


def delete_publication(request, item_id):
    Publication.objects.filter(id=item_id).delete()
    return redirect('esiapp:admin_home')

@login_required
def display_publication_page_admin(request, item_id):
    pub = Publication.objects.filter(id=item_id)[0]

    pub_file = PublicationFicher.objects.filter(publication_id=item_id)
    comm = Commentaire.objects.filter(publication_id=item_id)

    if request.user.is_authenticated:
        user = request.user

    context = {'pub': pub, 'com': comm, 'user': user, 'file': pub_file}
    # if user.is_teacher or user.is_doctorant:
    #     return render(request, 'user/display_publication_user.html', context)
    # else:
    return render(request, 'admin/display_publication_admin.html', context)


def ajouter_commentaire(request, item_id):
    msg = request.POST['message']
    if msg is None:
        print("NULL")
        msg = "NULL"
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    pub = Publication.objects.filter(id=item_id)[0]
    comm = Commentaire(commentaire_msg=msg, user=user, publication=pub)

    comm.save()
    return redirect('esiapp:display_publication_page_admin', item_id)


# @login_required(login_url='/login')
# def display_publication_page_user(request, item_id):
#     pub = Publication.objects.filter(id=item_id)[0]
#
#     comm = Commentaire.objects.filter(publication_id=item_id)
#
#     if request.user.is_authenticated:
#         user = request.user
#
#     context = {'pub': pub, 'com': comm, 'user': user}
#     return render(request, 'user/display_publication_user.html', context)


@login_required
def categorie_page(request):
    cat = Category.objects.all()
    user = request.user
    pub = Publication.objects.all()
    cat_dict = []
    for item in cat:
        cat_dict.append(len(Publication.objects.filter(Categorie__nom_categorie=item.nom_categorie)))
    mylist = zip(cat, cat_dict)
    context = {'cat': mylist, 'user': user}
    return render(request, 'categories_page.html', context)


def ajouter_categorie(request):
    nom = request.POST['categorie_name']
    cat = Category(nom_categorie=nom, description_categorie=nom)
    cat.save()
    return redirect('esiapp:categorie_page')


@login_required
def publications_page(request, item_id):
    pubs = Publication.objects.filter(Categorie_id=item_id)
    cat = Category.objects.filter(id=item_id)[0]
    user = request.user
    context = {'pubs': pubs, 'cat_name': cat.nom_categorie, 'user': user}
    return render(request, 'publications_page.html', context)


def jurys_page(request):

    jurys = Jury.objects.all()

    context = {'jurys': jurys}
    return render(request, 'jury_list_page.html', context)


def new_jury_page(request):

    context = {'wilayas': wilayas, 'universities': universities}
    return render(request, 'admin/new_jury_page.html', context)


def new_jury(request):
    nom = request.POST['nom']
    prenom = request.POST['prenom']
    email_jury = request.POST['email']
    telephone = request.POST['telephone']
    wilaya = request.POST['wilaya']
    university = request.POST['univ']

    jury = Jury(nom=nom, prenom=prenom, email=email_jury, telephone=telephone, wilaya=wilaya, university=university)
    jury.save()

    return redirect('esiapp:jurys_page')


def download_file(request, item_id):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'test.txt'

    file = PublicationFicher.objects.filter(id=item_id)[0]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
    print(MEDIA_ROOT)
    # Define the full file path
    filepath = MEDIA_ROOT + "/"+file.path_fichier
    print(filepath)
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def Logout(request):
    logout(request)
    messages.info(request, 'Deconnexion avec succés')
    return render(request, 'login_page.html')
