import { Component, Inject, EventEmitter, Output,Input } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {ProductService} from "../services/product.service";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-edit-product',
  templateUrl: './edit-product.component.html',
  styleUrls: ['./edit-product.component.css']
})
export class EditProductComponent {
  productForm: FormGroup;
  @Input() readOnly: boolean = false;

  @Output() close = new EventEmitter<void>();

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private apiService: ProductService,
    private dialogRef: MatDialogRef<EditProductComponent>, // ✅ Inject dialog ref
    private snackBar: MatSnackBar
  ) {
    this.readOnly = data.readOnly || false;

    this.productForm = this.fb.group({
      productName: [{ value: data?.name || '', disabled: this.readOnly }, Validators.required],
      productCategory: [{ value: data?.category_name || '', disabled: true }, Validators.required],
      costPrice: [{ value: data?.cost_price || 0, disabled: this.readOnly }, [Validators.required, Validators.min(0)]],
      sellingPrice: [{ value: data?.cost_price || 0, disabled: this.readOnly }, [Validators.required, Validators.min(0)]],
      description: [{ value: data?.description || '', disabled: this.readOnly }],
      availableStock: [{ value: data?.stock_available || 0, disabled: this.readOnly }, [Validators.required, Validators.min(0)]],
      unitsSold: [{ value: data?.units_sold || 0, disabled: this.readOnly }, [Validators.required, Validators.min(0)]]
    });
  }

  EditSubmit() {
    if (this.productForm.valid) {
      const formValues = this.productForm.value;

      const productData = {
        name: formValues.productName,
        description: formValues.description,
        category_id: this.data.category_id,
        cost_price: formValues.costPrice,
        selling_price: formValues.sellingPrice,
        stock_available: formValues.availableStock,
        units_sold: formValues.unitsSold,
        customer_rating: 4,
        updated_by_user_id: parseInt(sessionStorage.getItem('userId') || '0')
      };

      this.apiService.updateProduct(this.data.id, productData).subscribe({
        next: (res: any) => {
          const message = res?.message || 'Product updated successfully';
          // Return success response to parent
          this.close.emit();
          this.dialogRef.close({ success: true, message });
        },
        error: (err) => {
          const errorMsg = err?.error?.message || 'Error updating product';
          console.error('Error updating product', err);
          this.dialogRef.close({ success: false, message: errorMsg });
        }
      });
    }
  }
  closeModal() {
    this.dialogRef.close(false);
  }
}
