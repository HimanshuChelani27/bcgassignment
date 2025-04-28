import { Component } from '@angular/core';
import {MatDialog} from "@angular/material/dialog";
import {ActivatedRoute, Router} from "@angular/router";
import { MatTableDataSource } from '@angular/material/table';
import {ProductService} from "../services/product.service";

interface Product {
  id: number;
  name: string;
  category: string;
  costPrice: number;
  sellingPrice: number;
  description: string;
  availableStock: number;
  optimisePrise: number;
  unitsSold: number;
  selected?: boolean;
  category_name: string;
}


@Component({
  selector: 'app-pricing-optimization',
  templateUrl: './pricing-optimization.component.html',
  styleUrls: ['./pricing-optimization.component.css']
})
export class PricingOptimizationComponent {

  withDemandForecast: boolean = false;
  searchQuery: string = '';
  allColumns: string[] = [ 'name', 'category',
    'description', 'costPrice', 'sellingPrice','demand_forecast', 'Optimized_Price'];
  dataSource!: MatTableDataSource<Product>;
  products: Product[] = [];
  displayedColumns: string[] = [];
  selectedProductIds: number[] = []; 

  constructor(private dialog: MatDialog,private route: ActivatedRoute, private router: Router, private apiService: ProductService) {}
  username :any ;
  user_id :any ;
  ngOnInit(): void {
    // Initialize product data
    this.username = sessionStorage.getItem('userName');
    this.user_id = sessionStorage.getItem('userId');
    this.getProductByUser();

    this.updateDisplayedColumns();
    this.filterByCategory();
  }


  getProductByUser(): void {
    this.apiService.getProductByUser(this.user_id).subscribe({
      next: (res: any) => {
        this.products = res.data;
        // Extract unique categories
        this.categories = [
          ...new Set(this.products.map(p => p.category_name))
        ];

        this.dataSource = new MatTableDataSource<Product>(this.products); // Move this here
      },
      error: (err) => {
        console.error('Error fetching Products:', err);
      }
    });
  }

  categories: string[] = [];
  selectedCategory: string = '';
  filterByCategory(): void {
    if (!this.selectedCategory) {
      this.dataSource = new MatTableDataSource<Product>(this.products);
    } else {
      const filteredProducts = this.products.filter(
        product => product.category_name === this.selectedCategory
      );
      this.dataSource = new MatTableDataSource<Product>(filteredProducts);
    }
  }
  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  saveChanges(): void {
    console.log('Save changes clicked');
  }

  cancel(): void {
    console.log('Cancel clicked');
  }

  Back(){
    this.router.navigate(['/home']);
    console.log("clicked back button")
  }

  updateDisplayedColumns() {
    if (this.withDemandForecast) {
      this.displayedColumns = this.allColumns;
    } else {
      this.displayedColumns = this.allColumns.filter(col => col !== 'demand_forecast');
    }
  }


}
