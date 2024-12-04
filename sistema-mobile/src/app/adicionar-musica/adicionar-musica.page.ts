import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { IonicModule, LoadingController, NavController, ToastController } from '@ionic/angular';
import { Musica } from '../musica/musica.models'; 
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../home/usuario.model';

@Component({
  selector: 'app-adicionar-musica',
  templateUrl: './adicionar-musica.page.html',
  styleUrls: ['./adicionar-musica.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule], 
  providers: [HttpClient, Storage]
})
export class AdicionarMusicaPage implements OnInit {

  musica: Musica;
  foto: File | null = null; 
  usuario: Usuario = new Usuario(); 

  constructor(
    private http: HttpClient,
    private storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {
    this.musica = new Musica();
  }

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro); // Recupera dados do usuário
    } else {
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  // Função chamada ao enviar o formulário
  async adicionarMusica() {
    const loading = await this.controle_carregamento.create({
      message: 'Adicionando música...',
      duration: 60000
    });
    await loading.present();

    // Cria um FormData para enviar o arquivo junto com os dados da música
    const formData = new FormData();
    formData.append('banda', this.musica.banda);
    formData.append('musica', this.musica.musica);
    formData.append('ano', this.musica.ano.toString());
    formData.append('estilo', this.musica.estilo);
    
    // Se uma foto foi selecionada, adiciona ao FormData
    if (this.foto) {
      console.log('Foto a ser enviada :', this.foto);
      formData.append('foto', this.foto);
    }


    let http_headers: HttpHeaders = new HttpHeaders({
      'Authorization': `Token ${this.usuario.token}` // Passa o token de autenticação do usuário
    });
    console.log('Dados enviados para o servidor:', formData);
    // Envia o FormData para a API
    this.http.post('http://127.0.0.1:8000/musica/api/adicionar/', formData, { headers: http_headers })
      .subscribe({
        next: async (response) => {
          console.log('Música adicionada com sucesso!', response);
          await loading.dismiss();

          // Exibe um toast de sucesso
          const toast = await this.controle_toast.create({
            message: 'Música adicionada com sucesso!',
            duration: 2000,
            cssClass: 'ion-text-center'
          });
          toast.present();
          
          // Redireciona após adição de música
          this.controle_navegacao.navigateBack('/musica');
        },
        error: async (error) => {
          console.error('Erro ao adicionar música', error);
          await loading.dismiss();

          // Exibe um toast de erro
          const toast = await this.controle_toast.create({
            message: `Erro ao adicionar música: ${error.message}`,
            duration: 2000,
            cssClass: 'ion-text-center'
          });
          toast.present();
        }
      });
  }

  // Função para manipular o upload da foto
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.foto = file;
      console.log('Foto selecionada:', file);
    }
  }
}
