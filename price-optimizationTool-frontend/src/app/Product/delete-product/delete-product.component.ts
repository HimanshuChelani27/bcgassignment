import { Component, Inject } from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog, MatDialogRef} from '@angular/material/dialog';
import {ProductService} from "../services/product.service";

@Component({
  selector: 'app-delete-product',
  templateUrl: './delete-product.component.html',
  styleUrls: ['./delete-product.component.css']
})
export class DeleteProductComponent {
  constructor(
    public dialogRef: MatDialogRef<DeleteProductComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private apiService: ProductService
  ) {}
  confirmDelete(): void {
    this.apiService.deleteProduct(this.data?.id).subscribe({
      next: (response: any) => {
        // If backend returns a success message, pass it to parent
        this.dialogRef.close({ success: true, message: response?.message || 'Product deleted successfully' });
      },
      error: (err) => {
        console.error('Delete failed:', err);
        const errorMessage = err?.error?.message || 'Failed to delete the product';
        this.dialogRef.close({ success: false, message: errorMessage });
      }
    });
  }


  cancel(): void {
    this.dialogRef.close(false); // Cancel delete
  }
}
