import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SharedService {
  station_name!: string;
  constructor() {}

  setStationName(station_name: string): void {
    this.station_name = station_name;
  }

  getStationName(): string {
    return this.station_name;
  }
}
