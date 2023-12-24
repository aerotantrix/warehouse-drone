import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Bin, Station } from './types/common';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  baseUrl: string = 'http://192.168.1.110/';

  constructor(private httpClient: HttpClient) {}

  loginUser(username: string, password: string): Observable<any> {
    return this.httpClient.post(this.baseUrl + 'login-user', {
      username: username,
      password: password,
    });
  }

  logoutUser(headers: any): Observable<any> {
    return this.httpClient.post(this.baseUrl + 'logout-user', headers);
  }

  registerStation(
    stationname: string,
    password: string,
    battery: number,
    headers: any
  ): Observable<any> {
    return this.httpClient.post(this.baseUrl + 'register-drone', {
      stationname: stationname,
      password: password,
      battery: battery,
      ...headers,
    });
  }

  getBins(droneName: string, headers: any): Bin[] {
    return [
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 0, 0, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 0, 1, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 0, 2, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 0, 3, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 0, 4, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 1, 0, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 1, 1, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 1, 2, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 1, 3, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 1, 4, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 2, 0, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 2, 1, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 2, 2, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 2, 4, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 2, 3, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 3, 0, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 3, 1, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 3, 2, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 3, 3, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 3, 4, 1, false),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 4, 0, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 4, 1, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 4, 2, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 4, 4, 1, true),
      new Bin('fa34ra', new Date('2023-12-25 12:15:45'), 4, 3, 1, true),
    ];
  }

  getStations(headers: any): Station[] {
    return [new Station('eagleEye', 69)];
  }
}
