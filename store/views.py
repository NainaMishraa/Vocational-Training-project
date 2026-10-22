"""
store/views.py

CONCEPT 1 (MVT ARCHITECTURE - VIEWS):
In Django's Model-View-Template (MVT) pattern, Views represent the 'V'.
A View is a Python function that takes a web request (HttpRequest) and returns a web response
(HttpResponse, typically rendered HTML via render() or an HTTP redirect via redirect()).
Views act as the controller/coordinator: they query Models (ORM), perform business logic,
and pass data (context dictionary) to Templates.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import SignUpForm, OrderCreateForm


# ==============================================================================
# 1. HOME VIEW
# ==============================================================================
def home(request):
    """
    Renders the ecommerce home page with hero banner, categories, and new arrivals.
    
    CONCEPT 2 (ORM - OBJECT RELATIONAL MAPPING):
    - Category.objects.all(): Fetches all category records.
      Equivalent SQL: SELECT * FROM store_category ORDER BY name ASC;
    - Product.objects.filter(is_available=True).order_by('-created_at')[:8]:
      Equivalent SQL: SELECT * FROM store_product WHERE is_available = 1 ORDER BY created_at DESC LIMIT 8;
    
    CONCEPT 7 (CONTEXT):
    Data is passed to templates as a Python dictionary {'key': value}.
    """
    categories = Category.objects.all()
    # Fetch 8 most recently added available products for 'New Arrivals'
    new_arrivals = Product.objects.filter(is_available=True).select_related('category').order_by('-created_at')[:8]

    context = {
        'categories': categories,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'home.html', context)


# ==============================================================================
# 2. PRODUCT LIST VIEW (Shop, Filter, Search, Sort & Pagination)
# ==============================================================================
def product_list(request):
    """
    Displays the catalog with search, category filter, gender filter, price sorting, and pagination.
    
    CONCEPT 6 (REQUEST/RESPONSE - GET PARAMETERS):
    request.GET.get('param') reads URL query parameters (e.g., /products/?category=casual&gender=Men).
    
    CONCEPT 2 (ORM):
    - select_related('category'): Performs an SQL INNER JOIN with Category to prevent N+1 query problem.
    - filter(): WHERE clauses in SQL.
    - exclude(is_available=False): Equivalent SQL: WHERE is_available != 0
    - Q objects: Combines search conditions with SQL OR (WHERE name LIKE %q% OR description LIKE %q%).
    - order_by('price') / order_by('-price'): SQL ORDER BY price ASC / DESC.
    - count(): Equivalent SQL: SELECT COUNT(*) FROM store_product ...
    """
    products = Product.objects.select_related('category').filter(is_available=True)

    # 1. Search Query (Q objects for OR condition)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # CONCEPT 2 (ORM - Q OBJECTS):
        # Equivalent SQL: WHERE (name LIKE '%search_query%' OR description LIKE '%search_query%')
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # 2. Category Filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        # CONCEPT 2 (ORM - FILTER & GET):
        # Equivalent SQL: WHERE category_id = (SELECT id FROM store_category WHERE slug = 'category_slug')
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            products = products.filter(category=selected_category)

    # 3. Gender / Department Filter
    gender_filter = request.GET.get('gender', '').strip()
    if gender_filter in ['Men', 'Women', 'Kids']:
        products = products.filter(gender=gender_filter)

    # 4. Sorting
    sort_option = request.GET.get('sort', '')
    if sort_option == 'price_low':
        # Equivalent SQL: ORDER BY price ASC
        products = products.order_by('price')
    elif sort_option == 'price_high':
        # Equivalent SQL: ORDER BY price DESC
        products = products.order_by('-price')
    else:
        # Default newest first
        products = products.order_by('-created_at')

    # CONCEPT 2 (ORM - COUNT):
    total_count = products.count()

    # Pagination: Show 6 products per page
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': all_categories,
        'selected_category': selected_category,
        'category_slug': category_slug,
        'gender_filter': gender_filter,
        'sort_option': sort_option,
        'search_query': search_query,
        'total_count': total_count,
    }
    return render(request, 'product_list.html', context)


# ==============================================================================
# 3. PRODUCT DETAIL VIEW
# ==============================================================================
def product_detail(request, slug):
    """
    Renders single product view with size choices, stock, and related recommendations.
    
    CONCEPT 6 (REQUEST/RESPONSE - GET_OBJECT_OR_404):
    get_object_or_404() queries the database and raises an HTTP 404 error page if not found.
    Equivalent SQL: SELECT * FROM store_product WHERE slug = 'slug' LIMIT 1;
    
    CONCEPT 2 (ORM - EXCLUDE):
    exclude(id=product.id): Equivalent SQL: WHERE id != product.id
    """
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)

    # Related items in the same category excluding the current product
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


# ==============================================================================
# 4. CART VIEW
# ==============================================================================
@login_required
def cart_view(request):
    """
    CONCEPT 10 (AUTHENTICATION - @LOGIN_REQUIRED):
    Protects this view so only logged-in users can view their cart.
    Anonymous users are automatically redirected to LOGIN_URL ('login').
    
    CONCEPT 9 (CART - DATABASE STORED):
    Retrieves or creates the user's persistent Cart instance from the database.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    # CONCEPT 2 (ORM - SELECT_RELATED): joins Product for efficiency
    cart_items = cart.items.select_related('product').all()

    subtotal = cart.get_total_price()
    shipping = 0.00 if subtotal >= 999 or subtotal == 0 else 99.00
    grand_total = float(subtotal) + shipping

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)


# ==============================================================================
# 5. ADD TO CART VIEW
# ==============================================================================
@login_required
def add_to_cart(request, product_id):
    """
    Adds a chosen product with selected size and quantity into the user's database cart.
    
    CONCEPT 6 (REQUEST/RESPONSE - POST & REDIRECT):
    Reads form parameters using request.POST.get(). Returns a redirect() to avoid
    form re-submission upon browser refresh (Post/Redirect/Get pattern).
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        size = request.POST.get('size', product.size)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
    else:
        size = product.size
        quantity = 1

    # Check inventory
    if product.stock < 1:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('product_detail', slug=product.slug)

    # Get or create customer's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # CONCEPT 2 (ORM - FILTER & CREATE):
    # Check if item with exact same product and size already exists in this cart
    item = CartItem.objects.filter(cart=cart, product=product, size=size).first()
    if item:
        # Increase quantity up to available stock
        if item.quantity + quantity <= product.stock:
            item.quantity += quantity
            item.save()
            messages.success(request, f"Updated quantity for {product.name} ({size}) in your cart.")
        else:
            item.quantity = product.stock
            item.save()
            messages.warning(request, f"Set to maximum available stock ({product.stock}) for {product.name}.")
    else:
        # CONCEPT 2 (ORM - CREATE):
        # Equivalent SQL: INSERT INTO store_cartitem (cart_id, product_id, size, quantity) VALUES (...);
        qty_to_add = min(quantity, product.stock)
        CartItem.objects.create(cart=cart, product=product, size=size, quantity=qty_to_add)
        messages.success(request, f"Added {product.name} ({size}) to your cart.")

    return redirect('cart_view')


# ==============================================================================
# 6. UPDATE CART ITEM QUANTITY
# ==============================================================================
@login_required
def update_cart(request, item_id):
    """
    Increases or decreases the quantity of a specific cart item.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, f"Cannot add more than {cart_item.product.stock} items in stock.")
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                messages.info(request, f"Removed {cart_item.product.name} from your cart.")
                return redirect('cart_view')
            else:
                cart_item.save()

    return redirect('cart_view')


# ==============================================================================
# 7. REMOVE CART ITEM
# ==============================================================================
@login_required
def remove_from_cart(request, item_id):
    """
    Removes a line item completely from the cart.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"Removed {product_name} from your cart.")
    return redirect('cart_view')


# ==============================================================================
# 8. CHECKOUT VIEW
# ==============================================================================
@login_required
def checkout(request):
    """
    CONCEPT 4 (FORMS - MODELFORM):
    Collects shipping details using OrderCreateForm.
    Creates an Order in 'Pending' status and transfers CartItems into OrderItems.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()

    # Prevent checkout if cart is empty
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add items before checking out.")
        return redirect('product_list')

    subtotal = cart.get_total_price()
    shipping = 0.00 if subtotal >= 999 or subtotal == 0 else 99.00
    grand_total = float(subtotal) + shipping

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        # CONCEPT 4 (FORM VALIDATION):
        # form.is_valid() verifies that all required fields are filled and valid.
        if form.is_valid():
            # commit=False creates the model instance without immediately saving to the database
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = grand_total
            order.payment_status = 'Pending'
            order.order_status = 'Placed'
            order.save()

            # CONCEPT 3 (RELATIONSHIPS - ONE-TO-MANY):
            # Create an OrderItem for every CartItem
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    price=item.product.price
                )

            # Redirect user to the demo payment gateway page
            return redirect('demo_payment', order_id=order.id)
    else:
        # Prepopulate with user details if available
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        }
        form = OrderCreateForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)


# ==============================================================================
# 9. DEMO PAYMENT GATEWAY VIEW
# ==============================================================================
@login_required
def demo_payment(request, order_id):
    """
    A simulated payment gateway interface.
    
    CRITICAL DEMO SAFETY:
    No real transactions occur. On submission, the order is marked 'Paid',
    the product stock is reduced, and the user's cart is emptied.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # If order is already paid, redirect straight to success
    if order.payment_status == 'Paid':
        return redirect('order_success', order_id=order.id)

    if request.method == 'POST':
        # Simulated payment processing
        # 1. Update order status to Paid
        order.payment_status = 'Paid'
        order.save()

        # 2. Reduce stock for each purchased product
        for item in order.items.all():
            product = item.product
            # Decrement stock safely
            if product.stock >= item.quantity:
                product.stock -= item.quantity
            else:
                product.stock = 0
            product.save()

        # 3. Empty the user's cart after successful payment
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass

        # CONCEPT 10 (MESSAGES FRAMEWORK):
        messages.success(request, f"Payment simulated successfully! Order #{order.id} is confirmed.")
        return redirect('order_success', order_id=order.id)

    context = {
        'order': order,
    }
    return render(request, 'payment.html', context)


# ==============================================================================
# 10. ORDER SUCCESS VIEW
# ==============================================================================
@login_required
def order_success(request, order_id):
    """
    Displays confirmation for a successfully completed order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'order_success.html', context)


# ==============================================================================
# 11. ORDER HISTORY VIEW
# ==============================================================================
@login_required
def order_history(request):
    """
    Lists past orders placed by the currently logged-in user.
    
    CONCEPT 2 (ORM - FILTER & ORDER_BY):
    Equivalent SQL: SELECT * FROM store_order WHERE user_id = request.user.id ORDER BY created_at DESC;
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)


# ==============================================================================
# 12. ORDER DETAIL VIEW
# ==============================================================================
@login_required
def order_detail(request, order_id):
    """
    Shows detailed item breakdown, shipping address, and tracking status for one order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.select_related('product').all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_detail.html', context)


# ==============================================================================
# 13. AUTHENTICATION VIEWS (Signup, Login, Logout)
# ==============================================================================
def signup_view(request):
    """
    CONCEPT 10 (AUTHENTICATION - REGISTRATION):
    Handles user signup with validation and password encryption.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # CONCEPT 4 (FORM SAVE):
            # Saves new User record with hashed password in auth_user table
            user = form.save()
            # CONCEPT 10 (LOGIN):
            # Automatically log the user in after registration
            login(request, user)
            # Create cart for user immediately
            Cart.objects.get_or_create(user=user)
            messages.success(request, f"Welcome to ClothStore, {user.first_name or user.username}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def login_view(request):
    """
    CONCEPT 10 (AUTHENTICATION - LOGIN):
    Authenticates username and password against the auth_user table.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # CONCEPT 10 (AUTHENTICATE):
            # Verifies password hash in database
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Ensure cart exists
                Cart.objects.get_or_create(user=user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout_view(request):
    """
    CONCEPT 10 (AUTHENTICATION - LOGOUT):
    Flushes user session and logs the current user out.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully. Come back soon!")
    return redirect('home')


# ==============================================================================
# 14. STATIC INFORMATIONAL PAGES (About & Contact)
# ==============================================================================
def about(request):
    """
    Renders the company About Us page.
    """
    return render(request, 'about.html')


def contact(request):
    """
    Renders the Contact Us page and handles feedback submission.
    """
    if request.method == 'POST':
        # Simple simulated contact feedback
        sender_name = request.POST.get('name', 'Friend')
        messages.success(request, f"Thank you, {sender_name}! Your message has been received. Our team will get back to you shortly.")
        return redirect('contact')
    return render(request, 'contact.html')
