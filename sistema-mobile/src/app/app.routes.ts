import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'musica',
    loadComponent: () => import('./musica/musica.page').then( m => m.MusicaPage)
  },
  {
    path: 'adicionar-musica',
    loadComponent: () => import('./adicionar-musica/adicionar-musica.page').then( m => m.AdicionarMusicaPage)
  },
  {
    path: 'editar-musica/:id',
    loadComponent: () => import('./editar-musica/editar-musica.page').then( m => m.EditarMusicaPage)
  },
];
