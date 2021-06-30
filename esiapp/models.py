from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .enum import wilayas, universities

priorite = (
    ('priorite 1', 'priorite 1'),
    ('priorite 2', 'priorite 2'),
    ('priorite 3', 'priorite 3')
)


class MyUserManager(BaseUserManager):
    def create_user(self, Nom, prenom, email, telephone, adresse, is_admin, is_teacher, is_doctorant, password):
        """
        Creates and saves a User with the given data
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            adresse=adresse,
            telephone=telephone,
            Nom=Nom,
            prenom=prenom,
            is_admin=is_admin,
            is_teacher=is_teacher,
            is_doctorant=is_doctorant
        )

        user.set_password(password)
        user.save(using=self._db)
        print(user.email)
        return user

    def create_superuser(self, Nom, prenom, email, telephone, adresse, is_admin, is_teacher, is_doctorant, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(password=password,
                                email=self.normalize_email(email),
                                adresse=adresse,
                                telephone=telephone,
                                Nom=Nom,
                                prenom=prenom,
                                is_admin=is_admin,
                                is_teacher=is_teacher,
                                is_doctorant=is_doctorant
                                )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    objects = MyUserManager()
    username = None
    Nom = models.CharField(max_length=50, default="user")
    prenom = models.CharField(max_length=50, default="prenom")
    email = models.EmailField(_('email address'), unique=True)
    telephone = models.CharField(max_length=255, default="tel")
    adresse = models.CharField(max_length=255, default="adresse")
    is_admin = models.BooleanField('admin status', default=False)
    is_teacher = models.BooleanField('enseignant status', default=False)
    is_doctorant = models.BooleanField('doctorant status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Nom', 'prenom', 'telephone', 'adresse', 'is_admin','is_teacher', 'is_doctorant']

    def __str__(self):
        return self.email


class Category(models.Model):
    nom_categorie = models.CharField(max_length=60)
    description_categorie = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_categorie


class Publication(models.Model):
    titre = models.CharField(max_length=255)
    message = models.TextField()
    send_By = models.CharField(max_length=255)
    date_ajout = models.DateField(auto_now=True)
    date_limite = models.DateField()
    etat_publication = models.BooleanField(default=False)
    Categorie = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    editeur = models.CharField(max_length=255, default=None, null=True)
    priorite_contenu = models.CharField(choices=priorite, max_length=11, blank=True)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    commentaire_msg = models.TextField()
    date_ajout = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class PublicationFicher(models.Model):
    nom_fichier = models.CharField(max_length=255)
    path_fichier = models.FileField(null=True, upload_to='files/', blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_fichier


class Jury(models.Model):
    nom = models.CharField(max_length=80)
    prenom = models.CharField(max_length=80)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255, default="tel")
    wilaya = models.CharField(choices=wilayas, max_length=60, blank=True)
    university = models.CharField(choices=universities, max_length=255, blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom
