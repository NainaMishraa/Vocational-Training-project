# ClothStore - Ecommerce Fashion & Clothing Store

A modern, responsive, end-to-end ecommerce web application built with **Python 3**, **Django 6**, and **Vanilla CSS**. Designed with beginner-friendly, clean, readable code and function-based views for college and vocational project evaluation.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Prerequisites & Requirements](#prerequisites--requirements)
3. [Quick Setup Guide (Windows PowerShell)](#quick-setup-guide-windows-powershell)
4. [Default Credentials](#default-credentials)
5. [End-to-End User Flow](#end-to-end-user-flow)
6. [Project Structure & File Explanations](#project-structure--file-explanations)
7. [How to Inspect the Database in DB Browser for SQLite](#how-to-inspect-the-database-in-db-browser-for-sqlite)
8. [Understanding Migrations (makemigrations vs. migrate)](#understanding-migrations-makemigrations-vs-migrate)
9. [Django Concepts Reference](#django-concepts-reference)

---

## Key Features

- **Storefront & Catalog:**
  - Modern hero banner, category showcase cards, and latest 8 "New Arrivals".
  - Responsive product grid with real-time text search (ORM `Q` objects).
  - Multi-attribute filtering (Department: Men/Women/Kids, Categories) and price sorting (Low to High, High to Low).
  - Clean pagination (6 items per page).
- **Product Details:**
  - High-resolution imagery, garment description, and stock indicator badges.
  - Interactive size selection (S, M, L, XL), quantity selector, and related items carousel.
- **Database-Backed Shopping Cart:**
  - Carts and Cart Items stored in SQLite models (`Cart` and `CartItem`) linked to the customer.
  - Cart counter badge displayed dynamically across all page headers via a custom context processor.
  - In-cart quantity increment, decrement, and item removal with live subtotal/total calculations.
- **Secure Authentication:**
  - Built-in Django auth system (`django.contrib.auth`) for signup, login, and logout.
  - Protected views (`@login_required`) for cart, checkout, and order history.
  - Flash notification messages (`django.contrib.messages`).
- **Checkout & Simulated Payment:**
  - Shipping address collection via Django `ModelForm` (`OrderCreateForm`).
  - Realistic demo card payment interface with visual card mockup and clear academic test warning.
  - Automated post-payment processing: order status set to `Paid`, product inventory stock automatically decremented, user cart cleared, and customer redirected to receipt page.
- **Customer Order Tracking:**
  - Past order history with fulfillment status pills (`Placed`, `Shipped`, `Delivered`).
  - Detailed single-order invoices displaying shipping address and purchased item snapshots.
- **Django Admin Portal:**
  - Customized dashboard (`ModelAdmin`) with search bars, filters, and direct inline table editing for prices, stock, and fulfillment status.

---

## Prerequisites & Requirements

- Python 3.10+ (Tested on Python 3.13)
- Windows PowerShell
- Virtual Environment: `.env`
- Dependencies listed in `requirements.txt`:
  - `django>=5.0,<7.0`
  - `pillow>=10.0.0` (for image processing and sample data generation)

---

## Quick Setup Guide (Windows PowerShell)

Open PowerShell inside the project directory (`d:\Projects\VT ecom project`) and run the following commands step-by-step:

### 1. Create and Activate the Virtual Environment
```powershell
# Create the virtual environment named .env
python -m venv .env

# Activate the virtual environment
.env\Scripts\Activate.ps1
```
*(If PowerShell shows an execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### 2. Install Project Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Apply Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed the Database with Categories, Products, and Images
We created a custom management command that automatically creates 3 categories and 12 sample clothing products with local placeholder images:
```powershell
python manage.py seed_data
```

### 5. Create / Verify Superuser
An administrator account is already prepared:
```powershell
# Or create your own custom superuser:
python manage.py createsuperuser
```

### 6. Run the Local Development Server
```powershell
python manage.py runserver
```
Visit the website in your browser at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Default Credentials

### Administrator Dashboard
- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `admin123`

### Test Customer Shopper
- **Username:** `shopper1`
- **Password:** `SecretPass123!`
*(Or register any new account instantly using the **Sign Up** button on the website)*

---

## End-to-End User Flow

1. **Sign Up / Sign In:** Navigate to `/signup/` or `/login/` to access user-specific features.
2. **Browse & Filter:** Visit `/products/` to search garments or filter by department (Men, Women, Kids) or category.
3. **Select Product:** Open any product (e.g. `/products/classic-oxford-cotton-shirt/`), select size (`S`, `M`, `L`, `XL`), choose quantity, and click **Add to Shopping Cart**.
4. **Manage Cart:** On `/cart/`, verify items, use `+` or `-` to adjust quantity, or remove items.
5. **Checkout:** Click **Proceed to Checkout** (`/checkout/`), fill out delivery name, mobile number, address, city, and PIN code.
6. **Demo Payment:** On `/payment/<order_id>/`, review the interactive card preview and demo warning banner. Click **Authorize & Pay (Demo)** to simulate payment.
7. **Order Confirmation & History:** The app marks the order as `Paid`, reduces product inventory stock in the database, empties the cart, and redirects to `/order-success/<order_id>/`. You can review all past orders at `/orders/`.

---

## Project Structure & File Explanations

```text
VT ecom project/
├── clothstore/                       # Main Project Configuration Package
│   ├── __init__.py
│   ├── settings.py                  # Core configuration (INSTALLED_APPS, Templates, Static, Media, Auth)
│   ├── urls.py                      # Root URL dispatcher; delegates to store/urls.py and serves media
│   ├── wsgi.py                      # WSGI server entry point for web deployment
│   └── asgi.py                      # ASGI server entry point
│
├── store/                           # Store Application Package
│   ├── management/commands/
│   │   └── seed_data.py             # Custom management command: creates categories, 12 products & Pillow images
│   ├── migrations/
│   │   └── 0001_initial.py          # Initial database migration blueprint
│   ├── __init__.py
│   ├── admin.py                     # Customized ModelAdmin for Category, Product, Cart, Order, Inlines
│   ├── apps.py                      # Store application configuration
│   ├── context_processors.py        # Global cart_item_count injected into all template headers
│   ├── forms.py                     # SignUpForm (UserCreationForm) and OrderCreateForm (ModelForm)
│   ├── models.py                    # Category, Product, Cart, CartItem, Order, OrderItem models
│   ├── urls.py                      # Store routes (/products/, /cart/, /checkout/, /orders/, etc.)
│   └── views.py                     # Function-based views for the entire ecommerce lifecycle
│
├── templates/                       # Presentation Layer (HTML + Django Template Language)
│   ├── base.html                    # Master layout skeleton (HTML5 boilerplate, fonts, CSS, messages)
│   ├── header.html                  # Global sticky header with navigation and cart badge
│   ├── footer.html                  # Global footer with links, copyright, and evaluation notes
│   ├── home.html                    # Homepage (Hero banner, category cards, new arrivals)
│   ├── product_list.html            # Catalog with filters, search box, price sorting, pagination
│   ├── product_detail.html          # Single product page with size choices, stock, and add-to-cart
│   ├── cart.html                    # Shopping bag with line items, quantity update (+/-), subtotal
│   ├── checkout.html                # Shipping details ModelForm and order item summary
│   ├── payment.html                 # Simulated card payment gateway with test card preview & warning
│   ├── order_success.html           # Order confirmation receipt and invoice breakdown
│   ├── order_history.html           # Customer past orders list with status pills
│   ├── order_detail.html            # Single order invoice showing items and shipping address
│   ├── login.html                   # Authentication sign-in form
│   ├── signup.html                  # Customer registration form
│   ├── about.html                   # Brand narrative, craftsmanship, and evaluation overview
│   └── contact.html                 # Customer care inquiry form and showroom contact info
│
├── static/                          # Static Developer Assets (Bundled with code)
│   ├── css/
│   │   └── style.css                # Custom modern vanilla CSS design system, responsive grid, tokens
│   ├── js/
│   │   └── main.js                  # Vanilla JS for flash alerts dismissal, live credit card preview
│   └── images/                      # Static logos and icons
│
├── media/                           # Media Uploads (Dynamic runtime files uploaded via ImageField)
│   └── products/                    # Generated product JPEG images linked to Product models
│
├── db.sqlite3                       # Default SQLite database file
├── requirements.txt                 # Python package dependencies
├── CONCEPTS.md                      # Complete mapping of 14 Django concepts with code references
└── README.md                        # Documentation and project manual
```

---

## How to Inspect the Database in DB Browser for SQLite

[DB Browser for SQLite](https://sqlitebrowser.org/) is a visual tool that lets you inspect tables, records, foreign keys, and raw SQL queries inside `db.sqlite3`.

### Step-by-Step Instructions:
1. Download and install **DB Browser for SQLite** (free and open source).
2. Launch DB Browser for SQLite on your computer.
3. Click **Open Database** (or press `Ctrl + O`).
4. Navigate to your project folder:
   ```text
   D:\Projects\VT ecom project\db.sqlite3
   ```
5. Select `db.sqlite3` and click **Open**.
6. Click the **Browse Data** tab at the top.
7. Select any table from the dropdown menu to inspect its records:

| Database Table Name | Description | Key Columns to Inspect |
|---|---|---|
| `auth_user` | Django built-in user accounts | `id`, `username`, `email`, `password` (hashed with PBKDF2), `is_superuser` |
| `store_category` | Fashion style categories | `id`, `name`, `slug` |
| `store_product` | Apparel items in catalog | `id`, `name`, `slug`, `price`, `stock`, `size`, `gender`, `image`, `category_id` |
| `store_cart` | Shopping carts tied to users | `id`, `user_id`, `created_at` |
| `store_cartitem` | Items currently in user carts | `id`, `cart_id`, `product_id`, `size`, `quantity` |
| `store_order` | Orders placed by customers | `id`, `user_id`, `full_name`, `phone`, `address`, `city`, `pincode`, `total_amount`, `payment_status`, `order_status` |
| `store_orderitem` | Historical snapshot of items in an order | `id`, `order_id`, `product_id`, `size`, `quantity`, `price` |

### Try It Live:
- Place an order on the website, then switch to DB Browser for SQLite and click **Refresh**.
- You will see a new row appear in `store_order` with `payment_status = 'Paid'` and matching items in `store_orderitem`.
- Check `store_product`: you will see the product's `stock` column decremented by the purchased quantity.

---

## Understanding Migrations (`makemigrations` vs. `migrate`)

Django uses a two-step migration system to keep your Python models in sync with your database tables:

1. **`python manage.py makemigrations`**:
   - Inspects [`store/models.py`](file:///d:/Projects/VT%20ecom%20project/store/models.py) and compares it against your existing migrations.
   - Detects any newly added models, deleted models, or modified fields.
   - Creates a new Python migration blueprint file in `store/migrations/` (e.g. `0001_initial.py`).
   - *It does NOT touch or modify the database yet.*

2. **`python manage.py migrate`**:
   - Reads the unapplied migration blueprint files.
   - Executes the corresponding SQL `CREATE TABLE`, `ALTER TABLE`, or `DROP TABLE` statements on `db.sqlite3`.
   - Records the applied migration in the `django_migrations` table so it won't be run twice.

---

## Django Concepts Reference

For the complete reference guide mapping each concept to exact files, functions, and lines of code with plain-English explanations, read:

👉 **[CONCEPTS.md](file:///d:/Projects/VT%20ecom%20project/CONCEPTS.md)**
