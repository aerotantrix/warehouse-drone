import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BinsComponent } from './bins.component';

describe('BinsComponent', () => {
  let component: BinsComponent;
  let fixture: ComponentFixture<BinsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BinsComponent]
    });
    fixture = TestBed.createComponent(BinsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
