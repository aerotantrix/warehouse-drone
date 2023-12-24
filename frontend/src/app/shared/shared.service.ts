import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SharedService {
  stationname!: string;
  constructor() {}

  setStationName(stationname: string): void {
    this.stationname = stationname;
  }

  getStationName(): string {
    return this.stationname;
  }
}
