import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <button id="alert_btn" (click)="clicked = true">Click!</button>
    <a *ngIf="clicked" id="text-box">TADA!<a>
    <router-outlet></router-outlet>
  `,
  styles: []
})
export class AppComponent {
  title = 'frontend';
  clicked = false;
}
