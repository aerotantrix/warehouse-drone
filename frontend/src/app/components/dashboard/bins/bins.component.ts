import { ColDef } from 'ag-grid-community';
import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/shared/api.service';
import { AuthService } from 'src/app/shared/auth.service';
import { Bin } from 'src/app/shared/types/common';
import { ICellRendererParams } from 'ag-grid-community';
import { SharedService } from 'src/app/shared/shared.service';

@Component({
  selector: 'app-bins',
  templateUrl: './bins.component.html',
  styleUrls: ['./bins.component.scss'],
})
export class BinsComponent implements OnInit {
  stationname!: string;
  bins: Bin[] = [];
  colDefs: ColDef[] = [];

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private sharedService: SharedService
  ) {
    this.stationname = this.sharedService.getStationName();
  }

  timestampRenderer(params: ICellRendererParams): string {
    const date =
      params.value instanceof Date ? params.value : new Date(params.value);
    const formattedDateTime = `${date.toLocaleTimeString([], {
      hour12: false,
    })} ${date.toLocaleDateString()}`;
    return formattedDateTime;
  }

  ngOnInit(): void {
    this.colDefs = [
      { field: 'bin_id', flex: 1 },
      { field: 'row', flex: 1 },
      { field: 'rack', flex: 1 },
      { field: 'shelf', flex: 1 },
      {
        field: 'timestamp',
        flex: 1,
        cellRenderer: this.timestampRenderer,
      },
      { field: 'present', flex: 1 },
    ];
    this.bins = this.apiService.getBins(
      this.stationname,
      this.authService.getLoginHeaders()
    );
  }
}
