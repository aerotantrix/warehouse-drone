import { AuthService } from 'src/app/shared/auth.service';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  username!: string;
  password!: string;
  constructor(private authService: AuthService, private router: Router) {}

  login(): void {
    this.authService.login(this.username, this.password).subscribe(
      (res: any) => {
        alert(`Login Successful`);
        this.router.navigate(['/dashboard']);
      },
      (error: any) => {
        alert(`Login Failed, ${error.error.detail}`);
      }
    );
  }
}
