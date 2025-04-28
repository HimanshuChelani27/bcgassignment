import { Component, OnInit } from '@angular/core';
import {  MatTableDataSource } from '@angular/material/table';
import {MatDialog} from "@angular/material/dialog";
import {DemandForecastComponent} from "../demand-forecast/demand-forecast.component";
import {AddProductComponent} from "../add-product/add-product.component";
import {EditProductComponent} from "../edit-product/edit-product.component";
import {DeleteProductComponent} from "../delete-product/delete-product.component";
import {ProductService} from "../services/product.service";
import {Router} from "@angular/router";
import { MatSnackBar } from '@angular/material/snack-bar';

interface Product {
  id: number;
  name: string;
  category: string;
  costPrice: number;
  sellingPrice: number;
  description: string;
  availableStock: number;
  unitsSold: number;
  selected?: boolean;
  category_name: string;
}

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  withDemandForecast: boolean = true;
  searchQuery: string = '';

  allColumns: string[] = ['select', 'name', 'category', 'costPrice', 'sellingPrice',
    'description', 'availableStock', 'unitsSold','demand_forecast', 'actions'];
  products: Product[] = [];
  displayedColumns: string[] = [];
  dataSource!: MatTableDataSource<Product>;
  selectedProductIds: number[] = [];
  username :any ;
  user_id :any ;
  categories: string[] = [];
  selectedCategory: string = '';
  constructor(private dialog: MatDialog, private apiService: ProductService, private router: Router,private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    this.username = sessionStorage.getItem('userName');
    this.user_id = sessionStorage.getItem('userId');
    this.getProductByUser();
    this.updateDisplayedColumns();
  }

  updateDisplayedColumns() {
    if (this.withDemandForecast) {
      this.displayedColumns = this.allColumns;
    } else {
      this.displayedColumns = this.allColumns.filter(col => col !== 'demand_forecast');
    }
  }
  getProductByUser(): void {
    this.apiService.getProductByUser(this.user_id).subscribe({
      next: (res: any) => {
        this.products = res.data;
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


  addNewProduct(): void {
    const dialogRef = this.dialog.open(AddProductComponent, {
      width: '400px'
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        this.getProductByUser(); // refresh table
      }
    });
  }
  


  openDemandForecast(): void {

    const selectedProductData = this.products.filter(p => p.selected);

    const dialogRef = this.dialog.open(DemandForecastComponent, {
      width: '1200px',
      panelClass: 'custom-dialog-container',
      data: selectedProductData //  Passing IDs
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Forecast viewed for IDs:', result);
      }
    });
  }

  // Called when a checkbox is toggled
  onSelectionChange(): void {
    this.selectedProductIds = this.products
      .filter(p => p.selected)
      .map(p => p.id);
    console.log('Selected product IDs:', this.selectedProductIds);
  }

// Select all logic
  toggleSelectAll(checked: boolean): void {
    this.products.forEach(p => p.selected = checked);
    this.onSelectionChange();
  }

  isAllSelected(): boolean {
    return this.products.every(p => p.selected);
  }

  filter(): void {
    console.log('Filter clicked');
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  viewProduct(product: Product): void {
    console.log('View product:', product);
    const dialogRef = this.dialog.open(EditProductComponent, {
      data: { ...product, readOnly: true }, // 👈 add readOnly flag
      width: '300px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('View dialog closed');
    });
  }

  editProduct(product: Product): void {
    const dialogRef = this.dialog.open(EditProductComponent, {
      data: product,
      width: '500px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.snackBar.open(result.message, 'Close', {
          duration: 3000,
          panelClass: result.success ? 'snackbar-success' : 'snackbar-error'
        });
  
        if (result.success) {
          this.getProductByUser(); // reload or refresh the list if needed
        }
      }
    });
  }

  openDeleteDialog(product: any): void {
    const dialogRef = this.dialog.open(DeleteProductComponent, {
      width: '400px',
      data: product
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.snackBar.open(result.message, 'Close', {
          duration: 3000,
          panelClass: result.success ? 'snackbar-success' : 'snackbar-error'
        });
  
        if (result.success) {
          this.getProductByUser();
        }
      }
    });
  }


  saveChanges(): void {
    console.log('Save changes clicked');
  }

  cancel(): void {
    console.log('Cancel clicked');
  }


  Back(){
    this.router.navigate(['/home']);
  }



}
