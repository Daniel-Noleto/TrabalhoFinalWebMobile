from django.contrib import admin
from musica.models import Musica


# Register your models here.
class MusicaAdmin(admin.ModelAdmin):
    list_display = ['banda', 'musica', 'ano', 'foto', 'estilo']
    search_fields = ['banda','musica', 'estilo']

admin.site.register(Musica, MusicaAdmin)