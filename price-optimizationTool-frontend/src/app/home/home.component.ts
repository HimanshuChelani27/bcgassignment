import { Component } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import { AuthService } from '../auth/service/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  ngOnInit(): void {
    // Initialize product data
    this.getAllRolesAPI();
  }
  constructor(private route: ActivatedRoute, private router: Router, private apiService: AuthService) {

  }

  roles: any[] = [];
  getAllRolesAPI(): void {
    this.apiService.getAllRoles().subscribe({
      next: (res: any) => {
        this.roles = res.data; // adjust if your response structure is different
      },
      error: (err) => {
        console.error('Error fetching Roles:', err);
      }
    });
  }
  routetocreate(){
    this.router.navigate(['/product']);
  }
  routeToPriceOptimizer(){
    this.router.navigate(['/product/pricing-optimization']);
  }

}
