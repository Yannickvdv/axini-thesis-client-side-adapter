import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { PropertyComponent } from './property/property.component';

const routes: Routes = [
  { path: '', component: LandingPageComponent },
  { path: 'property/:id', component: PropertyComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
