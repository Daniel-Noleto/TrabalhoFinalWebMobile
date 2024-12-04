import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdicionarMusicaPage } from './adicionar-musica.page';

describe('AdicionarMusicaPage', () => {
  let component: AdicionarMusicaPage;
  let fixture: ComponentFixture<AdicionarMusicaPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AdicionarMusicaPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
