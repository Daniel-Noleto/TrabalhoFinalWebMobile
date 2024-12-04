import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { IonicModule, LoadingController, NavController, ToastController } from '@ionic/angular';
import { ActivatedRoute } from '@angular/router';
import { Musica } from '../musica/musica.models';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../home/usuario.model';

@Component({
  selector: 'app-editar-musica',
  templateUrl: './editar-musica.page.html',
  styleUrls: ['./editar-musica.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class EditarMusicaPage implements OnInit {
  musica: Musica = new Musica();
  usuario: Usuario = new Usuario();
  musicaId!: number;
  selectedFile: File | null = null;  // Variável para armazenar o arquivo da foto

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private storage: Storage,
    private controle_toast: ToastController,
    private controle_carregamento: LoadingController,
    private controle_navegacao: NavController
  ) {}

  async ngOnInit() {
    // Obter ID da música pela URL
    this.musicaId = parseInt(this.route.snapshot.paramMap.get('id') || '0', 10);

    // Recuperar dados do usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
    } else {
      this.controle_navegacao.navigateRoot('/home');
      return;
    }

    // Carregar dados da música
    this.carregarMusica();
  }

  // Carregar música para edição
  async carregarMusica() {
    const loading = await this.controle_carregamento.create({ message: 'Carregando música...' });
    await loading.present();

    const headers = new HttpHeaders({ Authorization: `Token ${this.usuario.token}` });
    
    this.http.get<Musica[]>(`http://127.0.0.1:8000/musica/api/`, { headers })
      .subscribe({
        next: (musicas) => {
          const musicaEncontrada = musicas.find(m => m.id === this.musicaId);
          if (musicaEncontrada) {
            this.musica = musicaEncontrada;
          } else {
            console.error('Música não encontrada!');
            this.controle_navegacao.navigateBack('/musica');
          }
          loading.dismiss();
        },
        error: (error) => {
          console.error('Erro ao carregar músicas:', error);
          loading.dismiss();
          this.controle_navegacao.navigateBack('/musica');
        }
      });
  }

  // Função para manipular o arquivo de imagem selecionado
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  // Função para editar música
  async editarMusica() {
    const loading = await this.controle_carregamento.create({ message: 'Salvando alterações...' });
    await loading.present();

    const formData = new FormData();
    formData.append('banda', this.musica.banda);
    formData.append('musica', this.musica.musica);
    formData.append('ano', this.musica.ano.toString());
    formData.append('estilo', this.musica.estilo);

    // Adicionar foto se foi selecionada
    if (this.selectedFile) {
      formData.append('foto', this.selectedFile, this.selectedFile.name);
    }

    const headers = new HttpHeaders({ Authorization: `Token ${this.usuario.token}` });
    console.log('Musica:', this.musica);
    this.http.put(`http://127.0.0.1:8000/musica/api/editar/${this.musicaId}/`, formData, { headers })
      .subscribe({
        next: async () => {
          await loading.dismiss();
          const toast = await this.controle_toast.create({
            message: 'Música editada com sucesso!',
            duration: 2000,
          });
          toast.present();
          this.controle_navegacao.navigateBack('/musica');
        },
        error: async (error) => {
          console.error('Erro ao editar música:', error);
          await loading.dismiss();
          const toast = await this.controle_toast.create({
            message: 'Erro ao editar música.',
            duration: 2000,
          });
          toast.present();
        },
      });
  }
}
