from django.contrib import admin
from app.models import Colonne, Tache

class ColonneAdmin(admin.ModelAdmin):
    list_display = ("id_colonne", "titre_colonne", "position_colonne")

class TacheAdmin(admin.ModelAdmin):
    list_display = ("id_tache", "titre_tache", "position_tache", "colonne")

admin.site.register(Colonne, ColonneAdmin)
admin.site.register(Tache, TacheAdmin)
