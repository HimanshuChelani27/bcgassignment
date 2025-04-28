import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProductRoutingModule } from './product-routing.module';
import { ProductComponent } from './product/product.component';
import { PricingOptimizationComponent } from './pricing-optimization/pricing-optimization.component';
import { DemandForecastComponent } from './demand-forecast/demand-forecast.component';
import { AddProductComponent } from './add-product/add-product.component';
import { EditProductComponent } from './edit-product/edit-product.component';
import { DeleteProductComponent } from './delete-product/delete-product.component';
import { MaterialModule } from '../shared/material/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    ProductComponent,
    DemandForecastComponent,
    AddProductComponent,
    EditProductComponent,
    DeleteProductComponent,
    PricingOptimizationComponent,
    // Add other Product components
  ],
  imports: [
    CommonModule,
    ProductRoutingModule,
    MaterialModule,
    FormsModule,           // Add this
    ReactiveFormsModule, 
  ]
  ,
  exports: [ProductComponent]
})
export class ProductModule { }
