from rest_framework import serializers
from musica.models import Musica
from drf_extra_fields.fields import Base64ImageField

class SerializadorMusica(serializers.ModelSerializer):
    '''
    Serializador para o model Musica
    '''

    foto = Base64ImageField(required=False, represent_in_base64=True)
    nome_estilo = serializers.SerializerMethodField()
    
    class Meta:
        model = Musica
        exclude = []


    def get_nome_estilo(self, instacia):
        return instacia.get_estilo_display()
    

    
class SerializadorAddMusica(serializers.ModelSerializer):
    '''
    Serializador para adicionar música
    '''

    nome_estilo = serializers.SerializerMethodField()
    
    class Meta:
        model = Musica
        exclude = []


    def get_nome_estilo(self, instacia):
        return instacia.get_estilo_display()
    

class SerializadorEditarMusica(serializers.ModelSerializer):
    '''
    Serializador para editar música
    '''
    nome_estilo = serializers.SerializerMethodField()

    class Meta:
        model = Musica
        exclude = [] 

    def get_nome_estilo(self, instancia):
        return instancia.get_estilo_display()