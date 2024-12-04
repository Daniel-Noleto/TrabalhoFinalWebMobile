from django.contrib import admin
from django.urls import path, include
from sistema.views import Login, Logout, LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('musica/', include('musica.urls'), name='musica'),
    path('colecao/', include('colecao.urls'), name='colecao'),
    path('autenticacao-api/', LoginAPI.as_view()),
]
