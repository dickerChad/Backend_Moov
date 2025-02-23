from django.contrib import admin
from .models import Projet, Departement, Tache, User, Document

admin.site.register(Departement)

admin.site.register(Tache)
admin.site.register(User)
admin.site.register(Document)

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut', 'date_fin', )
    ordering = ('nom', )
    search_fields =  ('nom', )


