import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | Observable<boolean> | Promise<boolean> {
    const token = localStorage.getItem('access_token'); 

    if (token) {
      if (this.isTokenExpired(token)) {
        localStorage.removeItem('access_token');
        this.router.navigate(['/'], { queryParams: { returnUrl: state.url } });
        return false;
      }
      return true;
    } else {
      this.router.navigate(['/'], { queryParams: { returnUrl: state.url } });
      return false;
    }
  }

  private isTokenExpired(token: string): boolean {
    try {
      const decoded: any = jwtDecode(token);
      const currentTime = Date.now() / 1000; // in seconds
      return decoded.exp < currentTime;
    } catch (error) {
      return true; 
    }
  }
}
