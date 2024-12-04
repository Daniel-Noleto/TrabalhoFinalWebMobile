from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView
from musica.models import Musica
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from musica.forms import FormularioMusica



from musica.serializers import SerializadorMusica, SerializadorAddMusica, SerializadorEditarMusica
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication




class ListarMusicas(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View para listar Musicas cadastradas.
    """
    
    model = Musica
    context_object_name = 'musicas'
    template_name = 'musica/listar.html'

    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser
    

class AdicionarMusicas(LoginRequiredMixin, CreateView, UserPassesTestMixin):
    model = Musica
    form_class = FormularioMusica
    template_name = 'musica/novo.html'
    success_url = reverse_lazy('listar-musicas')

    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser
    


class DeletarMusicas(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Musica
    template_name = 'musica/deletar.html'
    success_url = reverse_lazy('listar-musicas')

    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser


class EditarMusicas(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Musica
    form_class = FormularioMusica
    template_name = 'musica/editar.html'
    success_url = reverse_lazy('listar-musicas')

    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser    


class FotoMusica(LoginRequiredMixin, View):
    def get(self, request, arquivo):
        try:
            musica = Musica.objects.get(foto='musica/fotos/{}'.format(arquivo))
            return FileResponse(musica.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso não autorizado")
        except Exception as exception:
            raise exception
        


class APIListarMusicas(ListAPIView):
    '''
    View para listar instâncias de músicas (por meio do API REST)
    '''
    serializer_class = SerializadorMusica
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Musica.objects.all()


class APIDeletarMusicas(DestroyAPIView):
    """
    View para deletar instâncias de músicas (por meio da API REST)
    """
    serializer_class = SerializadorMusica
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Musica.objects.all()
    

class APIAdicionarMusica(CreateAPIView):
    """
    API para adicionar músicas.
    """
    serializer_class = SerializadorAddMusica
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class APIEditarMusica(UpdateAPIView):
    """
    API para editar músicas.
    """
    serializer_class = SerializadorEditarMusica
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Musica.objects.all()


