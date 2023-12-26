import { ColDef, GridReadyEvent } from 'ag-grid-community';
import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/shared/api.service';
import { AuthService } from 'src/app/shared/auth.service';
import { Bin, GridBin } from 'src/app/shared/types/common';
import { ICellRendererParams } from 'ag-grid-community';
import { SharedService } from 'src/app/shared/shared.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-bins',
  templateUrl: './bins.component.html',
  styleUrls: ['./bins.component.scss'],
})
export class BinsComponent implements OnInit {
  station_name!: string;
  bins!: any[];
  colDefs: ColDef[] = [];
  maxRow!: number;
  maxRack!: number;
  grid!: GridBin[][];

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
    this.station_name = this.sharedService.getStationName();
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
      { field: 'status', flex: 1 },
    ];
    setInterval(() => {
      this.getBinsData();
    }, 1000);
  }

  getMaxRow(data: any) {
    let max = 0;
    data.forEach((bin: any) => {
      if (bin.row > max) {
        max = bin.row;
      }
    });
    return max;
  }

  getMaxRack(data: any) {
    let max = 0;
    data.forEach((bin: any) => {
      if (bin.rack > max) {
        max = bin.rack;
      }
    });
    return max;
  }

  createArray(m: number, n: number, initialValue: string) {
    const newArray: GridBin[][] = [];

    for (let i = 0; i < m; i++) {
        const row: GridBin[] = [];
        for (let j = 0; j < n; j++) {
            row.push(new GridBin("NULL", "black"));
        }
        newArray.push(row);
    }

    return newArray;
  }

  async getBinsData() {
    this.apiService
      .getBins(this.station_name, this.authService.getRequestOptions())
      .subscribe((data: any) => {
        this.bins = data;
        this.maxRow = this.getMaxRow(data);
        this.maxRack = this.getMaxRack(data);

        this.grid = this.createArray(this.maxRow + 1, this.maxRack + 1, 'NULL');
        this.bins.forEach((bin: any) => {
          if (
            bin.row >= 0 &&
            bin.row < this.maxRow + 1 &&
            bin.rack >= 0 &&
            bin.rack < this.maxRack + 1
          ) {
            this.grid[bin.row][bin.rack].bin_id = bin.bin_id;
            this.grid[bin.row][bin.rack].color = bin.status ? 'red': 'green';
          } else {
            console.error(
              `Invalid bin coordinates: row ${bin.row} > ${this.maxRow}, rack ${bin.rack}`
            );
          }
        });
      });
  }
}
