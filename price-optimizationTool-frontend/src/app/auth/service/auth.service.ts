import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  apiUrl =environment.apiUrl;

  URL = this.apiUrl+'/auth';

  constructor(private http: HttpClient) { }

  login(username: string, password: string) {
    const loginData = {
      email: username,
      password: password
    };

    return this.http.post(`${this.URL}/login`, loginData);
  }

  registerUser(name: string, email: string, password: string,role_id: number) {
    const userData = {
      name: name,
      email: email,
      password: password,
      role_id: role_id
    };

    return this.http.post(`${this.URL}/register`, userData);
  }

  getAllRoles() {
    return this.http.get(`${this.URL}/get-all-roles`);
  }


}
