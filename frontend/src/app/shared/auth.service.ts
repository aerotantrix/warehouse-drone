import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { ApiService } from './api.service';
import { HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private _isLoggedIn = new BehaviorSubject<boolean>(false);
  public isLoggedIn = this._isLoggedIn.asObservable();
  public accessToken: string | null = null;

  constructor(private apiService: ApiService) {
    const storedToken = sessionStorage.getItem('access_token');
    // this._isLoggedIn.next(!!this.accessToken);
    if (storedToken) {
      this.accessToken = storedToken as string;
      this._isLoggedIn.next(true);
    }
  }

  getLoginHeaders(): any {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${this.accessToken}`,
    });
  }

  getRequestOptions(headers?: HttpHeaders): {} {
    return { headers: headers || this.getLoginHeaders() };
  }

  login(username: string, password: string): Observable<any> {
    return this.apiService.loginUser(username, password).pipe(
      tap((response: any) => {
        this.accessToken = response.access_token;
        this._isLoggedIn.next(true);

        if (this.accessToken) {
          sessionStorage.setItem('access_token', this.accessToken);
        }
      })
    );
  }

  logout() {
    sessionStorage.removeItem('access_token');
    return this.apiService.logoutUser(this.getRequestOptions()).pipe(
      tap((response: any) => {
        this.accessToken = null;
        this._isLoggedIn.next(false);
      })
    );
  }
}
