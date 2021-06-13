from django.db import models
from django.contrib.auth.models import AbstractUser


priorite = (
    ('priorite 1', 'priorite 1'),
    ('priorite 2', 'priorite 2'),
    ('priorite 3', 'priorite 3')
)


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    Nom = models.CharField(max_length=50, default="user")
    prenom = models.CharField(max_length=50, default="prenom")
    email = models.EmailField(max_length=255)
    telephone = models.CharField(max_length=255, default="tel")
    adresse = models.CharField(max_length=255, default="adresse")
    is_admin = models.BooleanField('admin status', default=False)
    is_teacher = models.BooleanField('enseignant status', default=False)
    is_doctorant = models.BooleanField('doctorant status', default=False)

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
#    editeur = models.
    priorite_contenu = models.CharField(choices=priorite, max_length=11, blank=True)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    commentaire_msg = models.TextField()
    date_ajout = models.DateField(auto_now=True)
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
