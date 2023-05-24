import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-property',
  template: `
    <div *ngIf="booking_error">
      <mat-card class="booking-failed-card" style="background-color: #FFCCCC">
          <mat-card-header>
            <mat-card-title>Booking failed...</mat-card-title>
            <mat-card-subtitle>Try again.</mat-card-subtitle>
          </mat-card-header>
      </mat-card>
    </div>

    <div *ngIf="booking_success">
      <mat-card class="booking-success-card" style="background-color: #e6ffcc">
          <mat-card-header>
            <mat-card-title>Booking success!</mat-card-title>
          </mat-card-header>
      </mat-card>
    </div>

    <ng-template *ngIf="waiting_for_property">
      Loading...
    </ng-template>

    <div *ngIf="property && !waiting_for_property">
      <mat-card class="property-card">
        <mat-card-header>
          <mat-card-title>{{property.title}}</mat-card-title>
          <mat-card-subtitle>€{{ property.price_per_night }} per night.</mat-card-subtitle>
        </mat-card-header>
        <img mat-card-image src="{{property.image}}" alt="Photo of property" style="width: 700px">
        <mat-card-content>
        <p>
          {{ property.text }} 
        </p>
        </mat-card-content>
        <mat-card-actions>
          <button mat-raised-button color="primary" [disabled]="waiting_for_booking" id="btn-book" (click)="openBookDialog()">Book!</button>
          <mat-spinner *ngIf="waiting_for_booking" diameter="36"></mat-spinner>
        </mat-card-actions>
      </mat-card>
    </div>
    
    <ng-template *ngIf="!property && !waiting_for_property">
      <mat-card class="not-found-card" style="background-color: #FFCCCC">
          <mat-card-header>
            <mat-card-title>Property not found!</mat-card-title>
          </mat-card-header>
        
          <mat-card-actions>
            <button mat-button id="btn-refresh" (click)="reloadPage()">Refresh!</button>
          </mat-card-actions>
        </mat-card>
    </ng-template>
  `,
  styles: []
})
export class PropertyComponent {
  property: any;
  property_error = false;
  waiting_for_property = false;
  
  booking_error = false;
  booking_success = false;
  waiting_for_booking = false;

  constructor(route: ActivatedRoute, private http: HttpClient, private dialog: MatDialog) {
    const id = route.snapshot.paramMap.get('id');

    // this.property = {
    //   "id": "1",
    //   "title": "Cozy colorful cottage",
    //   "text": "A beautiful cottage located in the midst of the Ardennen.",
    //   "price_per_night": 90,
    //   "image": "https://i.imgur.com/cnWropD.png"
    // }
    this.waiting_for_property = true;
    this.http.get(`http://localhost:5000/properties/${id}`).subscribe({
      next: (result) => {
        this.property = result
      },
      error: (error) => {
        this.property_error = error
      }}
    ).add(() => {
      this.waiting_for_property = false;
    });
  }

  openBookDialog(): void {
    const dialogRef = this.dialog.open(bookingConfirmationDialog);

    dialogRef.afterClosed().subscribe(result => {
        if(result == true) {
          this.waiting_for_booking = true;

          this.http.post(
            `http://localhost:5000/booking/${this.property.id}`, 
            {
              name: "James Doe",
              start_date: Date.now(),
              end_date: Date.now() + 86400000
            }).subscribe({
              next: (result) => this.booking_success = true,
              error: (error) => this.booking_error = error,
            }).add(() => {
              this.waiting_for_booking = false;
            });
        }
    })
  }

  reloadPage() {
    window.location.reload();
 }
}

@Component({
  selector: 'dialog-content-example-dialog',
  template: `
    <h2 mat-dialog-title>Are you sure?</h2>
    <mat-dialog-actions>
      <button id="btn-dialog-deny" mat-button mat-dialog-close>No</button>
      <button id="btn-dialog-confirm" mat-button color="primary" [mat-dialog-close]="true" cdkFocusInitial>Yes</button>
    </mat-dialog-actions>
    `,
})
export class bookingConfirmationDialog {}
