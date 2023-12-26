import { SharedService } from './../../shared/shared.service';
import { ColDef, ICellRendererParams } from 'ag-grid-community';
import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/shared/api.service';
import { AuthService } from 'src/app/shared/auth.service';
import { Station } from 'src/app/shared/types/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  stations!: any;
  schedules!: any;
  stationColDefs: ColDef[] = [];
  schedulesColDefs: ColDef[] = [];
  station_name!: string;
  scheduleStationName!: string;
  scheduleTime!: string;

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private sharedService: SharedService,
    private router: Router
  ) {
    this.authService.isLoggedIn.subscribe((status: boolean) => {
      if (status === false) {
        router.navigate(['/login']);
      }
    });
  }

  customButtonRenderer(params: ICellRendererParams) {
    this.station_name = params.data?.station_name;

    const button = document.createElement('button');
    button.innerHTML = 'View Shelves';
    button.className = 'view-shelves';

    return button;
  }

  ngOnInit(): void {
    this.stationColDefs = [
      {
        field: 'station_name',
        flex: 1,
        cellStyle: { textAlign: 'center' },
      },
      {
        field: 'battery',
        flex: 1,
        cellStyle: { textAlign: 'center' },
      },
    ];

    this.schedulesColDefs = [
      {
        field: 'station_name',
        flex: 1,
        cellStyle: { textAlign: 'center' },
      },
      {
        field: 'schedule_time',
        flex: 1,
        cellStyle: { textAlign: 'center' },
      },
    ];
    this.getStationsData();
    this.getSchedulesData();
  }

  getStationsData(): void {
    this.apiService
      .getStations(this.authService.getRequestOptions())
      .subscribe((data: any) => {
        this.stations = data;
      });
  }

  getSchedulesData(): void {
    this.apiService
      .getSchedules(this.authService.getRequestOptions())
      .subscribe((data: any) => {
        this.schedules = data;
      });
  }

  viewShelvesClick(params: any): void {
    try {
      const station_name = params.data?.station_name;
      const regex = /[a-zA-Z]/;
      if (regex.test(station_name)) {
        this.sharedService.setStationName(station_name);
        this.router.navigate(['dashboard/bins']);
      }
    } catch {}
  }

  deleteRow(params: any): void {
    try {
      const userResponse = window.confirm('Do you want to delete this row?');
      if (userResponse) {
        this.apiService
          .deleteSchedule(
            params.data.schedule_time,
            params.data.station_name,
            this.authService.getRequestOptions()
          )
          .subscribe(
            (res: any) => {
              alert('Deleted row');
              this.getSchedulesData();
            },
            (err: any) => {
              alert(err);
            }
          );
      }
    } catch {}
  }

  addNewRow(): void {
    try {
      this.apiService
        .addSchedule(
          this.scheduleTime,
          this.scheduleStationName,
          this.authService.getRequestOptions()
        )
        .subscribe(
          (res: any) => {
            this.getSchedulesData();
          },
          (err: any) => {
            alert(err);
          }
        );
    } catch {}
  }
}
