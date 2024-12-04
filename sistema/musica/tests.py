from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from musica.models import Musica
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from musica.consts import OPCOES_ESTILO 

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from musica.models import Musica
from musica.forms import FormularioMusica
from django.core.files.uploadedfile import SimpleUploadedFile
from musica.consts import OPCOES_ESTILO


class TestesModelMusica(TestCase):
    '''
    Classe de testes para o model Musica
    '''

    def setUp(self):
        # Criação de música
        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1  
        )

    def test_str(self):
        self.assertEqual(str(self.musica), 'Exemplo Banda - Exemplo Musica')

    def test_musica_fields(self):
        self.assertEqual(self.musica.banda, "Exemplo Banda")
        self.assertEqual(self.musica.musica, "Exemplo Musica")
        self.assertEqual(self.musica.ano, 2024)
        self.assertEqual(self.musica.estilo, 1)


class TestesViewListarMusicas(TestCase):
    '''
    Classe de testes para a view ListarMusicas
    '''

    def setUp(self):
        self.user = User.objects.create_superuser(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.url = reverse('listar-musicas')
        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1
        )
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Exemplo Musica')


class TestesViewAdicionarMusica(TestCase):
    '''
    Classe de testes para a view AdicionarMusica
    '''

    def setUp(self):
        self.user = User.objects.create_superuser(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.url = reverse('add-musicas')

        self.musica_data = {
            'musica': 'Exemplo Musica',
            'banda': 'Exemplo Banda',
            'ano': 2024,
            'estilo': 1,
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioMusica)

    def test_post(self):
        response = self.client.post(self.url, self.musica_data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('listar-musicas'))
        self.assertEqual(Musica.objects.count(), 1)
        self.assertEqual(Musica.objects.first().musica, 'Exemplo Musica')


class TestesViewEditarMusica(TestCase):
    '''
    Classe de testes para a view EditarMusica
    '''

    def setUp(self):
        self.user = User.objects.create_superuser(username='teste', password='teste')
        self.client.login(username='teste', password='teste')

        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1,
        )
        self.url = reverse('editar-musicas', kwargs={'pk': self.musica.pk})
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Musica)

    def test_post(self):
        updated_data = {
            'musica': 'Musica Atualizada',
            'banda': 'Banda Atualizada',
            'ano': 2025,
            'estilo': 1,
        }
        response = self.client.post(self.url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-musicas'))
        self.musica.refresh_from_db()
        self.assertEqual(self.musica.musica, 'Musica Atualizada')


class TestesViewDeletarMusica(TestCase):
    '''
    Classe de testes para a view DeletarMusica
    '''

    def setUp(self):
        self.user = User.objects.create_superuser(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1
        )
        self.url = reverse('deletar-musicas', kwargs={'pk': self.musica.pk})

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-musicas'))
        self.assertFalse(Musica.objects.filter(pk=self.musica.pk).exists())

