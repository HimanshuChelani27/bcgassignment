import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from "@angular/router";
import { AuthService } from "../service/auth.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  authForm!: FormGroup;
  isLogin: boolean = true;
  loginError: string = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private apiService: AuthService
  ) {}

  ngOnInit(): void {
    this.initForm();
   
      // Initialize product data
      this.getAllRolesAPI();
    
  }
  roles: any[] = [];
  getAllRolesAPI(): void {
    this.apiService.getAllRoles().subscribe({
      next: (res: any) => {
        this.roles = res.data; // adjust if your response structure is different
        console.log(this.roles, "ROLES")
      },
      error: (err) => {
        console.error('Error fetching Roles:', err);
      }
    });
  }


  initForm(): void {
    this.authForm = this.fb.group({
      name: [''],
      role: ['buyer'],
      phone: [''],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  switchMode(): void {
    this.isLogin = !this.isLogin;
  }

  closeModal(): void {
    // Optional: You can define logic here to close the modal or navigate away
    this.router.navigate(['/']);
  }

  submit(): void {
    this.loginError = '';

    const { email, password, name, role, phone } = this.authForm.value;
    if (this.isLogin) {
      this.apiService.login(email, password).subscribe(
        (response: any) => {
          if (response.status_code === 200 && response.data?.access_token) {
            const userData = response.data;
            localStorage.setItem('access_token', userData.access_token);
            sessionStorage.setItem('token_type', userData.token_type);
            sessionStorage.setItem('userId', userData.userId.toString());
            sessionStorage.setItem('userName', userData.userName);
            sessionStorage.setItem('userRoleId', userData.userRoleId.toString());
            sessionStorage.setItem('userEmail', userData.userEmail);
            sessionStorage.setItem('username', email);
    
            alert('✅ Login successful!');
            this.router.navigate(['/home']);
          } else {
            alert('⚠️ Login failed: ' + (response.message || 'Unknown error'));
          }
        },
        (error: any) => {
          if (error.status === 400 && error.error?.message === 'Incorrect username or password') {
            alert('❌ Invalid email or password. Please try again.');
          } else if (error.status === 403 && error.error?.message === 'Email not verified') {
            alert(error.error.error || '⚠️ Email not verified. Please check your inbox and verify your account.');
          } else if (error.status === 0) {
            alert('🚫 Server is not responding. Please try again later.');
          } else {
            alert('❌ An unexpected error occurred: ' + (error.error?.message || 'Unknown issue'));
          }
    
          console.error('Login error:', error);
        }
      );
    
    } else {
      const selectedRole = this.roles.find(r => r.name === role);
      const role_id = selectedRole?.id || 0;
  

  
      if (!role_id) {
        this.loginError = 'Invalid role selected.';
        return;
      }
  
      this.apiService.registerUser(name, email, password, role_id).subscribe(
        (res: any) => {
          if (res.status === 'success') {
            alert('✅ Signup successful! Please verify your email.');
            this.switchMode(); // Switch to login after successful signup
          } else {
            alert('⚠️ Signup failed: ' + (res.message || 'Please try again.'));
          }
        },
        (err: any) => {
          if (err.status === 400 && err.error?.message === 'Username already registered') {
            alert('⚠️ This email is already registered. Please login or use a different email.');
          } else if (err.status === 0) {
            alert('🚫 Server is not responding. Please check your internet or try again later.');
          } else {
            alert('❌ An unexpected error occurred: ' + (err.error?.message || 'Unknown error.'));
          }
          console.error('Signup error:', err);
        }
      );
      
      
    }
  }
}
