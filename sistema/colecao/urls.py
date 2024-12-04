from django.urls import path
from colecao.views import ListarColecoes, EditarColecoes, DeletarColecoes, CriarColecoes, FotoColecao, RemoverMusicaColecao, ListarMusicas, AdicionarMusicaColecao


urlpatterns = [
    path('', ListarColecoes.as_view(), name='listar-colecoes'),
    path('<int:pk>/', EditarColecoes.as_view(), name='editar-colecoes'),
    path('deletar/<int:pk>/', DeletarColecoes.as_view(), name='deletar-colecoes'),
    path('novo/', CriarColecoes.as_view(), name='criar-colecoes'),
    path('fotos/<str:arquivo>/', FotoColecao.as_view(), name='foto-colecao'),
    path('<int:colecao_pk>/remover-musica/<int:musica_pk>/', RemoverMusicaColecao.as_view(), name='remover-musica-colecao'),
    path('<int:colecao_pk>/musicas/', ListarMusicas.as_view(), name='listar-musicas-colecao'),
    path('<int:colecao_pk>/adicionar-musica/<int:musica_pk>/', AdicionarMusicaColecao.as_view(), name='adicionar-musica-colecao'),
]
