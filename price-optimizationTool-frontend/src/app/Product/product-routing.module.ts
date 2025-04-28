// import { NgModule } from '@angular/core';
// import { RouterModule, Routes } from '@angular/router';

// const routes: Routes = [];

// @NgModule({
//   imports: [RouterModule.forChild(routes)],
//   exports: [RouterModule]
// })
// export class ProductRoutingModule { }
// product-routing.module.ts

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductComponent } from './product/product.component';
import { PricingOptimizationComponent } from './pricing-optimization/pricing-optimization.component';

const routes: Routes = [
  { path: '', component: ProductComponent },
  { path: 'pricing-optimization', component: PricingOptimizationComponent },
  // you can add more child routes here
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductRoutingModule {}
