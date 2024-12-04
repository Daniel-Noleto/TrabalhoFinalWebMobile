from django.shortcuts import render, redirect, get_object_or_404
from colecao.models import Colecao
from musica.models import Musica
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, View
from django.urls import reverse_lazy
from colecao.forms import FormularioColecao
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class ListarColecoes(LoginRequiredMixin, ListView):
    """
    View para listar colecoes cadastrados.
    """
    
    model = Colecao
    context_object_name = 'colecoes'
    template_name = 'colecao/listar.html'

    def get_queryset(self):
        # Retorna apenas coleções do usuário atual
        return Colecao.objects.filter(usuario=self.request.user)    


class CriarColecoes(LoginRequiredMixin, CreateView):
    model = Colecao
    form_class = FormularioColecao
    template_name = 'colecao/novo.html'
    success_url = reverse_lazy('listar-colecoes')

    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        return super().form_valid(form)    


class EditarColecoes(LoginRequiredMixin, UpdateView):
    model = Colecao
    form_class = FormularioColecao
    template_name = 'colecao/editar.html'
    success_url = reverse_lazy('listar-colecoes')

    def dispatch(self, request, *args, **kwargs):
        colecao = self.get_object()
        if colecao.usuario != request.user:
            messages.error(request, "Você não tem permissão para editar esta coleção.")
            return redirect('listar-colecoes')
        return super().dispatch(request, *args, **kwargs)    


class DeletarColecoes(LoginRequiredMixin, DeleteView):
    model = Colecao
    template_name = 'colecao/deletar.html'
    success_url = reverse_lazy('listar-colecoes')

    def dispatch(self, request, *args, **kwargs):
        colecao = self.get_object()
        if colecao.usuario != request.user:
            messages.error(request, "Você não tem permissão para editar esta coleção.")
            return redirect('listar-colecoes')
        return super().dispatch(request, *args, **kwargs)    


class FotoColecao(LoginRequiredMixin, View):
    def get(self, request, arquivo):
        try:
            colecao = Colecao.objects.get(foto='colecao/fotos/{}'.format(arquivo))
            return FileResponse(colecao.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso não autorizado")
        except Exception as exception:
            raise exception
        

class RemoverMusicaColecao(LoginRequiredMixin, View):
    """
    Remove uma música de uma coleção específica.
    """
    def post(self, request, colecao_pk, musica_pk):
        colecao = get_object_or_404(Colecao, pk=colecao_pk, usuario=request.user)
        musica = get_object_or_404(Musica, pk=musica_pk)

        if musica in colecao.musicas.all():
            colecao.musicas.remove(musica)
            messages.success(request, "Música removida com sucesso!")
        else:
            messages.error(request, "Música não encontrada na coleção.")

        return redirect('editar-colecoes', pk=colecao_pk)
    

class ListarMusicas(LoginRequiredMixin, View):
    def get(self, request, colecao_pk):
        colecao = get_object_or_404(Colecao, pk=colecao_pk)
        if colecao.usuario != request.user:
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('listar-colecoes')
                
        musicas = Musica.objects.exclude(colecoes=colecao) 
        return render(request, 'colecao/listar_musicas.html', {'musicas': musicas, 'colecao': colecao})


class AdicionarMusicaColecao(LoginRequiredMixin, View):
    def post(self, request, colecao_pk, musica_pk):
        colecao = get_object_or_404(Colecao, pk=colecao_pk)

        if colecao.usuario != request.user:
            messages.error(request, "Você não tem permissão para adicionar músicas a esta coleção.")
            return redirect('listar-colecoes')        
                
        musica = get_object_or_404(Musica, pk=musica_pk)
        colecao.musicas.add(musica)
        messages.success(request, f'A música "{musica.musica}" foi adicionada à coleção.')
        return redirect('editar-colecoes', pk=colecao_pk)