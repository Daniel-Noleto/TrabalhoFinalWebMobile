import { Usuario } from './usuario.model';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AlertController, IonicModule, NavController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular'
import { LoadingController } from '@ionic/angular/standalone';
import { HttpClientModule, HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class HomePage {
  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegação: NavController,
    public controle_alerta: AlertController,
    public controle_toast: ToastController,
    public http: HttpClient,
    public storage: Storage
  ){}

  async ngOnInit(){
    await this.storage.create();
  }

  public instancia: { username: string, password: string } = {
    username: '',
    password: ''
  };

  async autenticarUsuario() {

    const loading = await this.controle_carregamento.create({message: 'Autenticando...', duration: 15000});
    await loading.present()
  
    //Define infotmações 
    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json'
    })

    this.http.post(
      'http://127.0.0.1:8000/autenticacao-api/', 
      this.instancia,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) =>{
        alert('Sucesso')
        let usuario: Usuario = Object.assign(new Usuario(), resposta);
        await this.storage.set('usuario', usuario)

        loading.dismiss();
        this.controle_navegação.navigateRoot('/musica')
      },
      error: async (erro:any) => {
        loading.dismiss()
        const mensagem = await this.controle_toast.create({
          message: `Falha ao autenticar usuário: ${erro.message}`,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    })
  }

}