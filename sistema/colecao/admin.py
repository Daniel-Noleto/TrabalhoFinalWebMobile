from django.contrib import admin
from colecao.models import Colecao


# Register your models here.
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'descricao', 'foto', 'exibir_musicas', 'usuario']
    search_fields = ['nome', 'usuario']

    # Método customizado para exibir as músicas associadas
    def exibir_musicas(self, obj):
        return ", ".join([musica.musica for musica in obj.musicas.all()])
    exibir_musicas.short_description = 'Músicas'

admin.site.register(Colecao, ColecaoAdmin)