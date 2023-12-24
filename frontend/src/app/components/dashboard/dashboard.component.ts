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
  stations: Station[] = [];
  colDefs: ColDef[] = [];
  stationname!: string;

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private sharedService: SharedService,
    private router: Router
  ) {}

  customButtonRenderer(params: ICellRendererParams) {
    this.stationname = params.data?.stationname;

    const button = document.createElement('button');
    button.innerHTML = 'View Shelves';
    button.className = 'view-shelves';

    return button;
  }

  ngOnInit(): void {
    this.colDefs = [
      {
        field: 'stationname',
        flex: 1,
        cellStyle: { textAlign: 'center' },
      },
      {
        field: 'battery',
        flex: 1,
        cellStyle: { textAlign: 'center' },
      },
    ];
    this.stations = this.apiService.getStations(
      this.authService.getLoginHeaders()
    );
  }

  viewShelvesClick(params: any): void {
    try {
      const stationname = params.data?.stationname;
      console.log(stationname);
      const regex = /[a-zA-Z]/;
      if (regex.test(stationname)) {
        this.sharedService.setStationName(stationname);
        this.router.navigate(['dashboard/bins']);
      }
    } catch {}
  }
}
