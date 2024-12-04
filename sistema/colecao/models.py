from django.db import models
from musica.models import Musica
from django.contrib.auth.models import User

# Create your models here.
class Colecao(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    foto = models.ImageField(blank=True, null=True, upload_to='colecao/fotos')
    
    musicas = models.ManyToManyField(Musica, related_name='colecoes')
    usuario = models.ForeignKey(User, related_name='colecoes_realizadas', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(
            self.nome,
            self.usuario
        )