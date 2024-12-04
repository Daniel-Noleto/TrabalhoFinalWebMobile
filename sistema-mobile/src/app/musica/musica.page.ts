import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Musica } from './musica.models';
import { Usuario } from '../home/usuario.model';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { IonicModule, LoadingController, NavController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';


@Component({
  selector: 'app-musica',
  templateUrl: './musica.page.html',
  styleUrls: ['./musica.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class MusicaPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public lista_musicas: Musica[] = [];

  constructor(
    public http: HttpClient,
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) { }

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro){
      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarMusicasSistemaWeb();
    }
    else{
      this.controle_navegacao.navigateRoot('/home');
    }
  }


  async consultarMusicasSistemaWeb(){
    const loading = await this.controle_carregamento.create({message: 'Pesquisando...', duration:60000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
     'Content-Type': 'application/json',
     'Authorization': `Token ${this.usuario.token}`
    });
   
   
    this.http.get(
     'http://127.0.0.1:8000/musica/api/',
     {
       headers: http_headers
     }
    ).subscribe({
     next: async (resposta: any) => {

       this.lista_musicas = resposta;

       loading.dismiss();
     },
     error: async (erro: any) => {
       loading.dismiss();
       const mensagem = await this.controle_toast.create({
         message: `Falha ao consultar músicas: ${erro.message}`,
         cssClass: 'ion-text-center',
         duration: 2000
       });
       mensagem.present();
     }
    });
 }


   async excluirMusica(id: number) {

    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Autenticando...', duration: 30000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });

    // Deleta instância de música via API do sistema web
    this.http.delete(
      `http://127.0.0.1:8000/musica/api/${id}/`,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {

        this.consultarMusicasSistemaWeb();

        // Finaliza interface com efeito de carregamento
        loading.dismiss();
      },
      error: async (erro: any) => {
        loading.dismiss();
        const mensagem = await this.controle_toast.create({
          message: `Falha ao excluir a música: ${erro.message}`,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    });
  }

  async editarMusica(id: number){
    this.controle_navegacao.navigateForward(`/editar-musica/${id}`)
  }

  acessarAdicionarMusica() {
    this.controle_navegacao.navigateForward('/adicionar-musica');
  }

  async logout() {
    // Remover dados de autenticação armazenados (exemplo usando Ionic Storage)
    await this.storage.remove('user');
    await this.storage.remove('token');

    // Redirecionar para a página de login
    this.controle_navegacao.navigateRoot('/home'); 
  }

  
}

