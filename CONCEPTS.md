# Django Concepts Reference Guide (ClothStore Project)

This document maps all 14 core Django concepts used in the **ClothStore** project directly to the files, functions, and lines of code where they appear. Each concept includes a plain-English explanation designed to help you confidently answer evaluators during project defense.

---

## 1. MVT (Model-View-Template) Architecture
- **Where it is used:**
  - **Models ('M'):** [`store/models.py`](file:///d:/Projects/VT%20ecom%20project/store/models.py)
  - **Views ('V'):** [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py)
  - **Templates ('T'):** [`templates/`](file:///d:/Projects/VT%20ecom%20project/templates/)
- **Plain-English Explanation:**
  Django uses MVT instead of traditional MVC. The **Model** defines the database schema and data rules using Python classes. The **View** contains the business logic, queries the models, and coordinates which data to fetch. The **Template** defines the presentation layer (HTML/CSS) and displays dynamic data to the user.

---

## 2. ORM (Object-Relational Mapping)
- **Where it is used:** [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py)
- **Methods & Equivalent SQL:**
  1. `Category.objects.all()`: In `home()`.
     - *Equivalent SQL:* `SELECT * FROM store_category ORDER BY name ASC;`
  2. `Product.objects.filter(is_available=True)`: In `home()` and `product_list()`.
     - *Equivalent SQL:* `SELECT * FROM store_product WHERE is_available = 1;`
  3. `Product.objects.get(slug=slug)` / `get_object_or_404`: In `product_detail()`.
     - *Equivalent SQL:* `SELECT * FROM store_product WHERE slug = '...' LIMIT 1;`
  4. `.order_by('-created_at')` and `.order_by('price')`: In `home()`, `product_list()`, `order_history()`.
     - *Equivalent SQL:* `ORDER BY created_at DESC;` or `ORDER BY price ASC;`
  5. `.exclude(id=product.id)`: In `product_detail()` for related items.
     - *Equivalent SQL:* `SELECT * FROM store_product WHERE id != ...;`
  6. `CartItem.objects.create(...)`: In `add_to_cart()` and `checkout()`.
     - *Equivalent SQL:* `INSERT INTO store_cartitem (...) VALUES (...);`
  7. `products.count()`: In `product_list()`.
     - *Equivalent SQL:* `SELECT COUNT(*) FROM store_product;`
  8. `Q(name__icontains=q) | Q(description__icontains=q)`: In `product_list()`.
     - *Equivalent SQL:* `WHERE (name LIKE '%q%' OR description LIKE '%q%');`
  9. `.select_related('category')` and `.select_related('product')`: In `product_list()`, `cart_view()`, `order_detail()`.
     - *Equivalent SQL:* Performs an SQL `INNER JOIN` in a single query, preventing the "N+1 query" database performance bottleneck.
- **Plain-English Explanation:**
  The ORM allows Python developers to work with database tables as ordinary Python objects. Instead of writing manual SQL strings which are prone to SQL injection, you invoke clean Python methods that Django translates into optimized SQL queries.

---

## 3. Relationships (One-to-Many & One-to-One)
- **Where it is used:** [`store/models.py`](file:///d:/Projects/VT%20ecom%20project/store/models.py)
  - `Product.category = models.ForeignKey(Category, on_delete=models.CASCADE)`
  - `Order.user = models.ForeignKey(User, on_delete=models.CASCADE)`
  - `OrderItem.order = models.ForeignKey(Order, on_delete=models.CASCADE)`
  - `OrderItem.product = models.ForeignKey(Product, on_delete=models.CASCADE)`
  - `Cart.user = models.OneToOneField(User, on_delete=models.CASCADE)`
- **Plain-English Explanation:**
  A **One-to-Many** relationship means a single parent record can have multiple child records. For example, one Category contains many Products, and one Customer can place many Orders. `on_delete=models.CASCADE` specifies that if a parent record is deleted, all dependent child records are automatically removed to maintain referential integrity.

---

## 4. Forms & ModelForms
- **Where it is used:** [`store/forms.py`](file:///d:/Projects/VT%20ecom%20project/store/forms.py), [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py#L190-L245)
  - `SignUpForm`: Extends Django's `UserCreationForm` to register new shoppers.
  - `OrderCreateForm`: A `forms.ModelForm` bound directly to the `Order` model.
- **Plain-English Explanation:**
  A `ModelForm` automatically creates HTML input elements corresponding to model fields, validates incoming user data against field constraints (length, data types), and saves cleaned data into the database using `form.save()`. In views, `form.is_valid()` checks that required inputs were filled properly before saving.

---

## 5. CSRF (Cross-Site Request Forgery) Protection
- **Where it is used:** All templates containing POST forms:
  - [`templates/login.html`](file:///d:/Projects/VT%20ecom%20project/templates/login.html)
  - [`templates/signup.html`](file:///d:/Projects/VT%20ecom%20project/templates/signup.html)
  - [`templates/product_detail.html`](file:///d:/Projects/VT%20ecom%20project/templates/product_detail.html)
  - [`templates/cart.html`](file:///d:/Projects/VT%20ecom%20project/templates/cart.html)
  - [`templates/checkout.html`](file:///d:/Projects/VT%20ecom%20project/templates/checkout.html)
  - [`templates/payment.html`](file:///d:/Projects/VT%20ecom%20project/templates/payment.html)
  - [`templates/contact.html`](file:///d:/Projects/VT%20ecom%20project/templates/contact.html)
- **Plain-English Explanation:**
  The `{% csrf_token %}` tag generates a secret, unpredictable cryptographically signed token embedded in every POST form. When submitted, Django's `CsrfViewMiddleware` verifies this token to ensure the form was genuinely sent from your website, preventing malicious external sites from performing unauthorized actions on behalf of your logged-in users.

---

## 6. Request / Response Lifecycle & HTTP Methods
- **Where it is used:** [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py)
  - `request.method == "POST"`: Distinguishes between loading a form (GET) and submitting data (POST).
  - `request.POST.get('quantity')`: Retrieves form inputs submitted via POST.
  - `request.GET.get('q')`, `request.GET.get('category')`, `request.GET.get('sort')`: Retrieves URL search parameters.
  - `render(request, 'template.html', context)`: Compiles the template with data and returns an `HttpResponse`.
  - `redirect('cart_view')`: Sends an HTTP 302 redirect response (following the Post/Redirect/Get pattern).
  - `get_object_or_404(Product, slug=slug)`: Fetches an object or immediately raises an HTTP 404 page if not found.
- **Plain-English Explanation:**
  Web browsers communicate via HTTP requests (GET for viewing pages, POST for submitting changes). Django views take this `HttpRequest` object, inspect headers/parameters, execute logic, and return an `HttpResponse` containing HTML or a redirect header.

---

## 7. Context & Template Tags/Filters
- **Where it is used:**
  - View dictionaries in [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py)
  - Global Context Processor in [`store/context_processors.py`](file:///d:/Projects/VT%20ecom%20project/store/context_processors.py)
  - Template files in [`templates/`](file:///d:/Projects/VT%20ecom%20project/templates/)
- **Features Demonstrated:**
  - `{{ variable }}`: Renders dynamic values (e.g., `{{ product.name }}`).
  - `{% for item in items %}` and `{% empty %}`: Iterates over lists.
  - `{% if condition %}` / `{% else %}`: Renders conditional blocks.
  - `|floatformat:2` and `|intcomma`: Formats numeric decimal prices with 2 decimal places and humanized separators (e.g., `₹1,499.00`).
  - `|truncatewords:12`: Shortens product descriptions to fit cleanly on product cards.
  - `store.context_processors.cart_counter`: Injects `cart_item_count` into every template across the site.
- **Plain-English Explanation:**
  A context is a Python dictionary (`{'key': value}`) passed from views to templates. Inside HTML, Django Template Language (DTL) syntax accesses dictionary keys and formats output using pipes called filters.

---

## 8. Named URL Patterns & Reversing
- **Where it is used:**
  - Project routing: [`clothstore/urls.py`](file:///d:/Projects/VT%20ecom%20project/clothstore/urls.py)
  - Store routing: [`store/urls.py`](file:///d:/Projects/VT%20ecom%20project/store/urls.py)
  - Templates: `{% url 'home' %}`, `{% url 'product_detail' product.slug %}`, `{% url 'add_to_cart' product.id %}`
  - Python views: `redirect('home')`, `redirect('order_success', order_id=order.id)`
- **Plain-English Explanation:**
  Instead of hardcoding URLs like `href="/products/shirt-1/"`, every route is assigned a unique name like `name='product_detail'`. Django dynamically generates the correct URL path using `{% url %}` in templates or `redirect()` in views. If a URL path ever changes in `urls.py`, all site links update automatically without broken links.

---

## 9. Database-Backed Cart System
- **Where it is used:** [`store/models.py`](file:///d:/Projects/VT%20ecom%20project/store/models.py#L90-L145), [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py#L140-L240)
- **Plain-English Explanation:**
  Rather than saving cart items temporarily inside browser cookies or session storage, the cart is modeled directly in the SQLite database via `Cart` and `CartItem` tables linked to the `User`. This demonstrates database relationships, prevents cart data loss when customers switch devices, and allows examiners to inspect cart items directly in SQLite DB Browser.

---

## 10. Authentication & Messaging Framework
- **Where it is used:** [`store/views.py`](file:///d:/Projects/VT%20ecom%20project/store/views.py)
  - User registration (`SignUpForm`, `form.save()`).
  - User sign-in (`authenticate()`, `login()`).
  - User sign-out (`logout()`).
  - Route protection (`@login_required`).
  - Flash notifications (`messages.success()`, `messages.warning()`, `messages.error()`, `messages.info()`).
- **Plain-English Explanation:**
  Django includes a robust authentication system with password salting and hashing (PBKDF2 SHA-256). The `@login_required` decorator restricts sensitive checkout and order history views to authenticated users only. The messages framework stores flash notifications that display on the next page view.

---

## 11. Django Admin Customization
- **Where it is used:** [`store/admin.py`](file:///d:/Projects/VT%20ecom%20project/store/admin.py)
  - `list_display`: Specifies which columns appear in the table.
  - `list_editable`: Allows instant inline editing of prices, stock, and order statuses.
  - `list_filter`: Adds filter sidebars by category, gender, and date.
  - `search_fields`: Enables search for product names and order details.
  - `prepopulated_fields`: Automatically generates URL slugs while typing names.
  - `inlines`: Renders line items (`CartItemInline`, `OrderItemInline`) inside their parent records.
- **Plain-English Explanation:**
  Django's built-in `/admin/` provides a staff management portal. Subclassing `admin.ModelAdmin` customizes the interface with column sorting, filters, search, and direct in-place editing.

---

## 12. Static Files vs. Media Files
- **Where it is configured:** [`clothstore/settings.py`](file:///d:/Projects/VT%20ecom%20project/clothstore/settings.py#L110-L135), [`clothstore/urls.py`](file:///d:/Projects/VT%20ecom%20project/clothstore/urls.py)
- **Plain-English Explanation:**
  - **Static Files (`static/`):** Fixed developer assets that ship with your code and do NOT change during user interaction, such as `style.css`, `main.js`, and site icons. Managed via `STATIC_URL` and `STATICFILES_DIRS`.
  - **Media Files (`media/`):** Dynamic files uploaded at runtime by users or administrators, such as product photography uploaded to `media/products/`. Managed via `MEDIA_URL` and `MEDIA_ROOT`.

---

## 13. Migrations System
- **Where it is used:** [`store/migrations/0001_initial.py`](file:///d:/Projects/VT%20ecom%20project/store/migrations/0001_initial.py)
- **Plain-English Explanation:**
  - `python manage.py makemigrations`: Reads changes in `models.py` and generates Python migration blueprint files describing what database changes are needed.
  - `python manage.py migrate`: Executes those blueprints against `db.sqlite3`, creating or altering tables without writing SQL manually.

---

## 14. Core Python Programming Foundations
- **Where it is used:** Throughout the entire codebase:
  - **Classes & Inheritance:** Models inherit from `models.Model`, forms inherit from `forms.ModelForm` or `UserCreationForm`, admin classes inherit from `admin.ModelAdmin`.
  - **Functions:** Views (`home()`, `product_list()`, `checkout()`, etc.) and context processors (`cart_counter()`).
  - **Dictionaries:** Context dictionaries and choice tuples (`GENDER_CHOICES`, `SIZE_CHOICES`).
  - **Loops & Conditions:** Seeding automation in [`seed_data.py`](file:///d:/Projects/VT%20ecom%20project/store/management/commands/seed_data.py) and filtering logic in views.
