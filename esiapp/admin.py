from django.contrib import admin
from .models import User, Publication, PublicationFicher, Category, Commentaire

admin.site.register(User)
admin.site.register(Publication)
admin.site.register(PublicationFicher)
admin.site.register(Category)
admin.site.register(Commentaire)
