import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <!-- <button id="alert_btn" value="1" (click)="click()">Click!</button>
    <a *ngIf="clicked" id="text-box">TADA!<a> -->
    <mat-toolbar>
      <span routerLink="/" style="cursor:pointer">Booking-app</span>
    </mat-toolbar>
    <div style="width: 1100px; margin: 0px auto 0px auto;">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: ['']
})
export class AppComponent {
  title = 'frontend';
  clicked = false;

  constructor(private http: HttpClient) {}

  click() {
    this.clicked = true

    return this.http.get("http://localhost:5000/properties").subscribe(result => console.log(result));
  }
}
