
# 📊 Price Optimization API

This is a FastAPI-powered backend for a Price Optimization platform. The application handles user registration, login, product management, optimized pricing, and more — including email verification using Ngrok, and it connects seamlessly with an Angular frontend.

---

## 🚀 Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **Database**: MySQL (via SQLAlchemy)
- **Frontend**: Angular
- **Email**: Gmail SMTP using app password
- **Token Auth**: JWT
- **Local Tunneling**: Ngrok
- **Migrations**: Alembic

---

## 📦 Installation (Local Setup)

### 1. Install Python 3.12

### 2. Create and activate a virtual environment

```bash
python3.12 -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up `.env` file

Create a `.env` file in the root folder and include the following environment variables:

```env
DATABASE_URL='mysql+pymysql://<user>:<password>@<host>/<database>'
SENDER_EMAIL='<your-email>'
EMAIL_APP_PASSWORD='<your-app-password>'
URL='https://<your-ngrok-url>/'
ALGORITHM_JWT='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_KEY='<your-secret-key>'
```

> ✅ **Important**: Replace `<your-ngrok-url>` with the actual Ngrok forwarding URL each time you restart it.

---

## 🔧 Alembic Migrations

Alembic is used for managing database migrations.

### 🛠 Initial Migration

To apply the initial migration that creates all the tables:

1. Open `alembic.ini` and update the following line with your actual database URL:
   ```ini
   sqlalchemy.url = mysql+pymysql://<user>:<password>@<host>/<database>
   ```

2. Run the migration:
   ```bash
   alembic upgrade head
   ```

> 📅 This initial migration was created on **6th April** and adds all the necessary tables to the database.

---

## 🌱 Seed Data

To populate the database with initial (seed) data for testing or demo purposes, a **seed data script** is included.

Run the seed script after applying the migration to add default users, roles, and initial product entries.  
Example usage:

```bash
python seed_data.py
```

---

## 🔗 Email Verification via Ngrok

We use Ngrok to expose the local FastAPI server to the internet, allowing users to receive valid verification links over email.

### Steps:

1. Start Ngrok:
   ```bash
   ngrok http 8000
   ```

2. Copy the HTTPS forwarding URL (e.g., `https://1f74-...ngrok-free.app`)

3. Paste it in the `.env` file under `URL`

Now, all email links sent for verification will be accessible outside localhost ✅

---

## 🧪 Running the App

To start the FastAPI application:

```bash
uvicorn main:app --reload
```

- Swagger documentation will be available at:  
  👉 [http://localhost:8000/docs](http://localhost:8000/docs)

- Or via your Ngrok URL:  
  👉 `https://<your-ngrok-url>/docs`

---

## ⚙️ Core Constants

The following constants are defined in `core/constants.py`. These values are used in the pricing logic and demand forecasting engine:

```python
DEFAULT_PROFIT_MARGIN = 1.5
SEASONAL_FACTOR = 1.1
PRICE_ELASTICITY_EXPONENT = 0.5
DEMAND_EXPONENT = 0.3
MIN_PRICE_MULTIPLIER = 1.2
PRICE_CEILING_MULTIPLIER = 1.5
```

> These values can be **tuned** as per business needs without changing the underlying logic.  
They play a key role in computing the **optimized price** and performing **demand forecasting** for products.

---

## 🗂 Project Structure

```
price_optimization/
├── app/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── migrations/
├── core/
│   └── constants.py
├── seed_data.py
├── .env
├── alembic.ini
├── README.md
├── requirements.txt

```

---

## 🔐 Roles & Permissions

| Role     | ID | Permissions                     |
|----------|----|----------------------------------|
| Admin    | 1  | Full Access                      |
| Buyer    | 2  | View-only                        |
| Supplier | 3  | Add/Edit their own products only |

---


Absolutely! Here's an extended **Frontend** section for your README, with details on setting the backend URL, running the Angular app, and installing dependencies:

---

## 🧑‍💻 Angular Frontend Setup

The frontend of this project is built using **Angular** and is responsible for handling the user interface and interacting with the FastAPI backend through REST APIs.

### 📁 Location

The Angular app is located in the `angular-frontend/` folder inside the root project directory.

---

### ⚙️ Environment Configuration

Before running the Angular application, you need to configure the backend URL in the environment file.

1. Navigate to `angular-frontend/src/environments/environment.ts`  
2. Set the API base URL to the current backend (usually your Ngrok forwarding URL):

```ts
export const environment = {
  production: false,
  apiUrl: 'https://<your-ngrok-url>' // 👈 Add your current backend URL here
};
```

> ✅ Make sure to **update this URL every time Ngrok restarts**, as the forwarding URL changes.

---

Absolutely! You can and **should** document the Angular folder structure in your README to help other developers (or your future self) quickly understand how the project is organized.

Here’s how you can add a clean and informative **Folder Structure** section based on your provided screenshot:

---

### 📂 Angular Project Structure

The main Angular code resides in the `src/app/` folder. Here’s a breakdown of the folder structure and what each section is responsible for:

```
src/
└── app/
    ├── auth/                     # Authentication (login, register)
    │   └── login/                # Login component and logic
    │   ├── auth.service.ts       # Handles auth-related API calls
    │   └── auth.service.spec.ts  # Unit tests for AuthService
    │
    ├── environments/             # Environment config (dev/prod API URLs)
    │
    ├── home/                     # Home/Dashboard component
    │
    ├── Product/                  # All Product-related features
    │   ├── add-product/          # UI for adding a product
    │   ├── create-product/       # Component to handle new product creation
    │   ├── delete-product/       # Component to delete products
    │   ├── demand-forecast/      # Predicts demand based on pricing model
    │   ├── edit-product/         # Component for updating product details
    │   ├── pricing-optimization/ # Calculates optimized product pricing
    │   ├── product.service.ts    # Handles API calls for products
    │   └── product.service.spec.ts # Unit tests for ProductService
    │
    ├── app-routing.module.ts     # App-level routing configuration
    ├── app.component.ts          # Root component logic
    ├── app.component.html        # Root component UI
    ├── app.component.css         # Root component styling
    └── app.module.ts             # Main app module declaration
    ├── auth-guard.ts             # Used for checking access token for API'S
    
```

---

### 🧠 Key Notes:

- ✅ **Separation of concerns**: Features like auth and product management are modularized into their respective folders.
- 🔄 **Scalability**: Adding new modules (e.g., user profiles, analytics) is easy with this structure.
- 🌐 **API integration**: `auth.service.ts` and `product.service.ts` handle backend API interaction cleanly using Angular's `HttpClient`.

---

Let me know if you want help generating component scaffolds or improving lazy loading!

### 📥 Install Dependencies

Run the following command inside the `angular-frontend/` directory to install all necessary packages:

```bash
npm install
```

---

### 🚀 Run the Angular App

Once dependencies are installed and the environment is set, start the frontend development server:

```bash
ng serve
```

This will start the app at:

```
http://localhost:4200
```


---

### 🔄 Live Reload

The app supports **live reloading**, so changes in the code will automatically refresh the browser.

---

### 🌐 CORS Note

CORS is already **enabled** on the FastAPI backend to allow smooth communication between the frontend (localhost:4200) and backend (via Ngrok or localhost:8000).

---
## 📫 Contact

**Developer**: Himanshu Chelani  
**Email**: [himanshuchelani4@gmail.com](mailto:himanshuchelani4@gmail.com)

