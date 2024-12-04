from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from colecao.models import Colecao
from musica.models import Musica
from colecao.forms import FormularioColecao
from django.core.files.uploadedfile import SimpleUploadedFile


class TestesModelColecao(TestCase):
    '''
    Classe de testes para o model Colecao
    '''

    def setUp(self):
        # Criação de usuário
        self.user = User.objects.create_user(username='teste', password='teste')

        # Criação de musica
        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1  
        )
        #Criação de coleção
        self.colecao = Colecao.objects.create(
            nome="Exemplo Colecao", 
            descricao="Exemplo Descricao", 
            usuario=self.user
        )
    
    def test_str(self):
        # Testa o método __str__ do modelo Colecao
        self.assertEqual(str(self.colecao), f'Exemplo Colecao - {self.user.username}')
    
    def test_musicas(self):
        # Testa a relação ManyToMany entre Colecao e Musica
        self.colecao.musicas.add(self.musica)
        self.assertIn(self.musica, self.colecao.musicas.all())

    def test_usuario(self):
        # Testa a relação com o usuário
        self.assertEqual(self.colecao.usuario, self.user)



class TestesViewListarColecoes(TestCase):
    '''
    Classe de testes para a view ListarColecoes
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.url = reverse('listar-colecoes')
        self.colecao = Colecao.objects.create(nome="Exemplo Colecao", descricao="Exemplo Descricao", usuario=self.user)
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Exemplo Colecao')


class TestesViewCriarColecoes(TestCase):
    '''
    Classe de testes para a view CriarColecoes
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.url = reverse('criar-colecoes')
        fake_image = SimpleUploadedFile("fake_image.jpg", b"file_content", content_type="image/jpeg")

        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1,
            foto=fake_image
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioColecao)

    def test_post(self):
        data = {
            'nome': 'Exemplo Colecao',
            'descricao': 'Exemplo Descricao',
            'musicas': [self.musica.pk],
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-colecoes'))

        self.assertEqual(Colecao.objects.count(), 1)
        self.assertEqual(Colecao.objects.first().nome, 'Exemplo Colecao')


class TestesViewEditarColecoes(TestCase):
    '''
    Classe de testes para a view EditarColecoes
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        fake_image = SimpleUploadedFile("fake_image.jpg", b"file_content", content_type="image/jpeg")
        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1,
            foto=fake_image
        )
        self.colecao = Colecao.objects.create(nome="Exemplo Colecao", descricao="Exemplo Descricao", usuario=self.user)
        self.colecao.musicas.add(self.musica)  
        self.url = reverse('editar-colecoes', kwargs={'pk': self.colecao.pk})
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Colecao)
        self.assertEqual(response.context.get('object').pk, self.colecao.pk)

    def test_post(self):
        data = {'nome': 'Colecao', 'descricao': 'Descricao', 'musicas': [self.musica.pk],}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-colecoes'))
        self.assertEqual(Colecao.objects.first().nome, 'Colecao')


class TestesViewDeletarColecoes(TestCase):
    '''
    Classe de testes para a view DeletarColecoes
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.colecao = Colecao.objects.create(nome="Exemplo Colecao", descricao="Exemplo Descricao", usuario=self.user)
        self.url = reverse('deletar-colecoes', kwargs={'pk': self.colecao.pk})

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-colecoes'))
        self.assertFalse(Colecao.objects.filter(pk=self.colecao.pk).exists())


class TestesViewRemoverMusicaColecao(TestCase):
    '''
    Classe de testes para a view RemoverMusicaColecao
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste')
        self.client.login(username='teste', password='teste')
        self.colecao = Colecao.objects.create(nome="Exemplo Colecao", descricao="Exemplo Descricao", usuario=self.user)
        
        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1  
        )

        self.colecao.musicas.add(self.musica)
        self.url = reverse('remover-musica-colecao', kwargs={'colecao_pk': self.colecao.pk, 'musica_pk': self.musica.pk})

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('editar-colecoes', kwargs={'pk': self.colecao.pk}))
        self.assertNotIn(self.musica, self.colecao.musicas.all())


class TestesViewAdicionarMusicaColecao(TestCase):
    '''
    Classe de testes para a view AdicionarMusicaColecao
    '''

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='password')
        self.client.login(username='teste', password='password')
        self.colecao = Colecao.objects.create(nome="Exemplo Colecao", descricao="Exemplo Descricao", usuario=self.user)

        fake_image = SimpleUploadedFile("fake_image.jpg", b"file_content", content_type="image/jpeg")

        self.musica = Musica.objects.create(
            musica="Exemplo Musica", 
            banda="Exemplo Banda", 
            ano=2024, 
            estilo=1,
            foto=fake_image
        )

        self.url = reverse('adicionar-musica-colecao', kwargs={'colecao_pk': self.colecao.pk, 'musica_pk': self.musica.pk})

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('editar-colecoes', kwargs={'pk': self.colecao.pk}))
        self.assertIn(self.musica, self.colecao.musicas.all())
