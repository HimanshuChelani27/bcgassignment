import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PricingOptimizationComponent } from './pricing-optimization.component';

describe('PricingOptimizationComponent', () => {
  let component: PricingOptimizationComponent;
  let fixture: ComponentFixture<PricingOptimizationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PricingOptimizationComponent]
    });
    fixture = TestBed.createComponent(PricingOptimizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
