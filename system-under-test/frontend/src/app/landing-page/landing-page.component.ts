import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-landing-page',
  template: `
   <div *ngFor="let item of properties">
      <mat-card style="max-width: 400px">
        <mat-card-header>
          <mat-card-title>{{ item.title }}</mat-card-title>
          <mat-card-subtitle>€{{ item.price_per_night }} per night!</mat-card-subtitle>
        </mat-card-header>
        <img mat-card-image src="{{ item.image }}" alt="Photo of the property">
        <mat-card-content>
          <p>
            {{ item.text }}
          </p>
        </mat-card-content>
        <mat-card-actions>
          <button mat-button id="btn-book-{{item.id}}" [routerLink]="['/property', item.id]">BOOK</button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [
  ]
})
export class LandingPageComponent {
  properties: any;

  constructor(route: ActivatedRoute, private http: HttpClient) {
    this.http.get("http://localhost:5000/properties/").subscribe({
      next: (result) => {
        console.log(result)
        this.properties = result
      },
      error: (error) => {
        console.log(error)
        this.properties = [
          {
            id: "1",
            title: "Cozy colorful cottage",
            text: "A beautiful cottage located in the midst of the Ardennen.",
            price_per_night: 90,
            image: "https://i.imgur.com/cnWropD.png"
          },
          {
            id: "2",
            title: "Classy comfortable high-rise room",
            text: "A spacious high-rise room overlooking the port of Rotterdam.",
            price_per_night: 120,
            image: "https://i.imgur.com/QkYJ0Zo.png"
          }
        ]
      }}
    );
  }
}
