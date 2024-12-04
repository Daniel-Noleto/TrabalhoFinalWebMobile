from django.db import models
from musica.consts import *


# Create your models here.
class Musica(models.Model):
    banda = models.CharField(max_length=100)
    musica = models.CharField(max_length=100)
    ano = models.IntegerField()
    foto = models.ImageField(blank=True, null=True, upload_to='musica/fotos')
    estilo = models.SmallIntegerField(choices=OPCOES_ESTILO)

    def __str__(self):
        return '{0} - {1}'.format(

            self.banda,
            self.musica,
            self.ano,
            self.get_estilo_display()
        )
    
  
    