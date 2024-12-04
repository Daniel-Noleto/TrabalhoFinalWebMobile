from django.forms import ModelForm
from musica.models import Musica


class FormularioMusica(ModelForm):

    class Meta:
        model = Musica
        exclude = []