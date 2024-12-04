import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MusicaPage } from './musica.page';

describe('MusicaPage', () => {
  let component: MusicaPage;
  let fixture: ComponentFixture<MusicaPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MusicaPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
