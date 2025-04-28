import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {AuthService} from "../../auth/service/auth.service";
import {ProductService} from "../services/product.service";
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-add-product',
  templateUrl: './add-product.component.html',
  styleUrls: ['./add-product.component.css']
})
export class AddProductComponent implements OnInit{
  productForm: FormGroup;



  @Output() close = new EventEmitter<void>();

  constructor(private fb: FormBuilder,  private apiService: ProductService,private snackBar: MatSnackBar,
    private dialogRef: MatDialogRef<AddProductComponent>) {
    this.productForm = this.fb.group({
      productName: ['', Validators.required],
      productCategory: ['', Validators.required],
      costPrice: ['', [Validators.required, Validators.min(0)]],
      sellingPrice: ['', [Validators.required, Validators.min(0)]],
      description: [''],
      availableStock: ['', [Validators.required, Validators.min(0)]],
      unitsSold: ['', [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    // Initialize product data
    this.getAllCategory();
  }

  categories: any[] = [];
  getAllCategory(): void {
    this.apiService.getAllCategory().subscribe({
      next: (res: any) => {
        this.categories = res.data; // adjust if your response structure is different
      },
      error: (err) => {
        console.error('Error fetching categories:', err);
      }
    });
  }
  onCategoryChange(event: Event) {
    const selectedValue = (event.target as HTMLSelectElement).value;
    console.log('Selected category_id:', selectedValue);
    // Optionally: update form or perform logic
  }



  showSuccessMessage = false;

  onSubmit() {
    if (this.productForm.valid) {
      const formValues = this.productForm.value;

      const productData = {
        name: formValues.productName,
        description: formValues.description,
        category_id: parseInt(formValues.productCategory),
        cost_price: parseFloat(formValues.costPrice),
        selling_price: parseFloat(formValues.sellingPrice),
        stock_available: parseInt(formValues.availableStock),
        units_sold: parseInt(formValues.unitsSold),
        customer_rating: 0,
        created_by_user_id: parseInt(sessionStorage.getItem('userId') || '0')
      };

      this.apiService.createProduct(productData).subscribe({
        next: (res: any) => {
          this.snackBar.open(res?.message || 'Product added successfully!', 'Close', {
            duration: 3000,
            panelClass: 'snackbar-success'
          });
          this.dialogRef.close(true); // signal success
        },
        error: (err) => {
          const errorMessage = err?.error?.message || 'Failed to add product';
          this.snackBar.open(errorMessage, 'Close', {
            duration: 3000,
            panelClass: 'snackbar-error'
          });
          this.dialogRef.close(false); // optionally close or stay open
        }
      });
    }
  }

  showSuccess() {
    this.showSuccessMessage = true;

    // Automatically close popup and modal after 2 seconds
    setTimeout(() => {
      this.showSuccessMessage = false;
      this.closeModal(); // ✅ Close the dialog/modal
    }, 2000);
  }

  closeModal() {
    this.dialogRef.close(false);
  }
}
