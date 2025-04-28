import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  apiUrl =environment.apiUrl;
  constructor(private http: HttpClient) { }

  URL = this.apiUrl+'/products';
  getAllCategory() {
    return this.http.get(`${this.URL}/get-all-category`);
  }
  getProductByUser(user_id:any) {
    return this.http.get(`${this.URL}/by-user?user_id=${user_id}`);
  }

  deleteProduct(product_id:any) {
    return this.http.delete(`${this.URL}/delete-product-by-id/${product_id}`);
  }

  createProduct(productData: any) {
    return this.http.post(`${this.URL}/create`, productData);
  }

  updateProduct(productId: number, productData: any) {
    return this.http.put(`${this.URL}/update-product-by-id/${productId}`, productData);
  }
}
