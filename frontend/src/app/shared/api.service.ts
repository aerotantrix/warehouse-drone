import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Bin, Station } from './types/common';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  baseUrl: string = 'http://192.168.192.50/';

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
    station_name: string,
    password: string,
    battery: number,
    headers: any
  ): Observable<any> {
    return this.httpClient.post(this.baseUrl + 'register-drone', {
      body: {
        station_name: station_name,
        password: password,
        battery: battery,
      },
      ...headers,
    });
  }

  getBins(droneName: string, headers: any): Observable<any> {
    return this.httpClient.get(this.baseUrl + `bins/${droneName}`, headers);
  }

  getStations(headers: any): Observable<any> {
    return this.httpClient.get(this.baseUrl + `get-stations`, headers);
  }

  getSchedules(headers: any): Observable<any> {
    return this.httpClient.get(this.baseUrl + `get-schedule`, headers);
  }

  deleteSchedule(
    schedule_time: any,
    station_name: any,
    headers: any
  ): Observable<any> {
    return this.httpClient.delete(this.baseUrl + `delete-schedule`, {
      body: { schedule_time: schedule_time, station_name: station_name },
      ...headers,
    });
  }

  addSchedule(
    schedule_time: any,
    station_name: any,
    headers: any
  ): Observable<any> {
    return this.httpClient.post(
      this.baseUrl + `add-schedule`,
      { schedule_time: schedule_time, station_name: station_name },
      { ...headers }
    );
  }
}
