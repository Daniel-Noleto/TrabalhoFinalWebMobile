from django.urls import path
from musica.views import ListarMusicas, FotoMusica, AdicionarMusicas, DeletarMusicas, EditarMusicas
from musica.views import APIListarMusicas, APIDeletarMusicas, APIAdicionarMusica, APIEditarMusica
urlpatterns = [
    path('', ListarMusicas.as_view(), name='listar-musicas'),
    path('fotos/<str:arquivo>/', FotoMusica.as_view(), name='foto-musica'),
    path('novo/', AdicionarMusicas.as_view(), name='add-musicas'),
    path('deletar/<int:pk>/', DeletarMusicas.as_view(), name='deletar-musicas'),
    path('<int:pk>/', EditarMusicas.as_view(), name='editar-musicas'),
    path('api/', APIListarMusicas.as_view(), name='api-listar-musicas'),
    path('api/<int:pk>/', APIDeletarMusicas.as_view(), name='api-deletar-musicas'),
    path('api/adicionar/', APIAdicionarMusica.as_view(), name='api-adicionar-musica'),
    path('api/editar/<int:pk>/', APIEditarMusica.as_view(), name='api-editar-musica'),
]