from django.forms import ModelForm
from colecao.models import Colecao


class FormularioColecao(ModelForm):

    class Meta:
        model = Colecao
        exclude = ['usuario']