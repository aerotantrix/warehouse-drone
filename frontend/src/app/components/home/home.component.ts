import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/shared/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  constructor(private authService: AuthService, private router: Router) {
    this.authService.isLoggedIn.subscribe((status: boolean) => {
      if (status === true) {
        router.navigate(['/dashboard']);
      }
    });
  }
}
