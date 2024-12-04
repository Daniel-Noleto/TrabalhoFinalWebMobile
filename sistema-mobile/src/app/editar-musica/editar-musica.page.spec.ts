import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditarMusicaPage } from './editar-musica.page';

describe('EditarMusicaPage', () => {
  let component: EditarMusicaPage;
  let fixture: ComponentFixture<EditarMusicaPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(EditarMusicaPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
