import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <button id="alert_btn" (click)="click()">Click!</button>
    <a *ngIf="clicked" id="text-box">TADA!<a>
    <router-outlet></router-outlet>
  `,
  styles: []
})
export class AppComponent {
  title = 'frontend';
  clicked = false;

  constructor(private http: HttpClient) {}

  click() {
    this.clicked = true

    return this.http.get("http://localhost:5000/users").subscribe(result => console.log(result));
  }
}
