// import { NgModule } from '@angular/core';
// import { RouterModule, Routes } from '@angular/router';
// import {LoginComponent} from "./auth/login/login.component";
// import {HomeComponent} from "./home/home.component";
// import {ProductComponent} from "./Product/product/product.component";
// import {AuthGuard} from "./auth.guard";
// import {PricingOptimizationComponent} from "./Product/pricing-optimization/pricing-optimization.component";
// const routes: Routes = [
//   { path: '', component: LoginComponent },
//   { path: 'home', component: HomeComponent,canActivate: [AuthGuard] },
//   {path: 'create-product', component: ProductComponent, canActivate: [AuthGuard]},
//   {path: 'pricing-optimization', component: PricingOptimizationComponent},
// ];

// @NgModule({
//   imports: [RouterModule.forRoot(routes)],
//   exports: [RouterModule]
// })
// export class AppRoutingModule { }
// app-routing.module.ts

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { HomeComponent } from './home/home.component';
import { AuthGuard } from './auth.guard';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
  {
    path: 'product',
    loadChildren: () => import('./Product/product.module').then(m => m.ProductModule),
    canActivate: [AuthGuard]
  },
  { path: '**', redirectTo: '' } // wildcard route for unmatched URLs
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
