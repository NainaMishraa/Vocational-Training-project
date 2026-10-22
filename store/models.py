"""
store/models.py

CONCEPT 1 (MVT ARCHITECTURE - MODELS):
In Django's Model-View-Template (MVT) pattern, Models represent the 'M'.
A Model is a Python class that defines the structure and behavior of your database tables.
Each attribute of the model maps to a column in the database table.
Django ORM automatically translates these Python classes into SQL CREATE TABLE statements.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# ==============================================================================
# CATEGORY MODEL
# ==============================================================================
class Category(models.Model):
    """
    CONCEPT 14 (PYTHON BASICS - CLASSES):
    Category defines groups of clothing items (e.g., Casual, Formal, Ethnic).
    """
    name = models.CharField(max_length=100, unique=True, help_text="Category name, e.g., Formal Wear")
    slug = models.SlugField(max_length=120, unique=True, help_text="URL-friendly version of the name")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ==============================================================================
# PRODUCT MODEL
# ==============================================================================
class Product(models.Model):
    """
    Product represents clothing items in the store.
    
    CONCEPT 3 (RELATIONSHIPS - ONE-TO-MANY):
    ForeignKey creates a One-to-Many relationship between Category and Product.
    - One Category can contain many Products.
    - Each Product belongs to exactly one Category.
    - on_delete=models.CASCADE means if a Category is deleted, all its products are deleted too.
    """
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    ]

    SIZE_CHOICES = [
        ('S', 'Small (S)'),
        ('M', 'Medium (M)'),
        ('L', 'Large (L)'),
        ('XL', 'Extra Large (XL)'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        help_text="One-to-Many Relationship: Each product belongs to one category"
    )
    name = models.CharField(max_length=200, help_text="Name of the clothing product")
    slug = models.SlugField(max_length=220, unique=True, help_text="Unique slug for the product detail URL")
    description = models.TextField(help_text="Detailed description of the garment and fabric")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Selling price in INR (₹)")
    image = models.ImageField(upload_to='products/', help_text="Product image uploaded to media/products/")
    stock = models.PositiveIntegerField(default=10, help_text="Available inventory count")
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, default='M', help_text="Default/Sample size")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Men', help_text="Target audience")
    is_available = models.BooleanField(default=True, help_text="Controls if product is visible to shoppers")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when product was added")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # CONCEPT 8 (NAMED URLS): returns canonical URL for this product
        return reverse('product_detail', args=[self.slug])


# ==============================================================================
# CART & CART ITEM MODELS
# ==============================================================================
class Cart(models.Model):
    """
    CONCEPT 9 (CART - DATABASE MODELS):
    We store the shopping cart directly in the SQLite database linked to the User.
    This demonstrates Django relationships, persistent storage across user sessions,
    and allows inspecting cart rows directly in DB Browser for SQLite.
    
    CONCEPT 3 (RELATIONSHIPS):
    One-to-One or One-to-Many with User. Here ForeignKey with unique=True or OneToOneField:
    One User has One Cart.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        help_text="Every registered user has one shopping cart in the database"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        """Calculates grand total of all items in cart."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_count(self):
        """Calculates total quantity of all items in cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    A single line item in the shopping cart.
    
    CONCEPT 3 (RELATIONSHIPS):
    - Many CartItems belong to One Cart (ForeignKey).
    - Many CartItems can reference the same Product (ForeignKey).
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, default='M', help_text="Chosen garment size (S, M, L, XL)")

    class Meta:
        # Ensures same product with same size in a cart is unique (quantity increments instead)
        unique_together = ('cart', 'product', 'size')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})"

    def get_subtotal(self):
        """Calculates price x quantity for this item."""
        return self.product.price * self.quantity


# ==============================================================================
# ORDER & ORDER ITEM MODELS
# ==============================================================================
class Order(models.Model):
    """
    Represents an order placed by a customer.
    
    CONCEPT 3 (RELATIONSHIPS):
    One User can place Many Orders (One-to-Many ForeignKey).
    """
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    ORDER_STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Customer who placed the order"
    )
    full_name = models.CharField(max_length=150, help_text="Receiver's full name")
    phone = models.CharField(max_length=20, help_text="Contact telephone / mobile number")
    address = models.TextField(help_text="Shipping street address")
    city = models.CharField(max_length=100, help_text="Destination city")
    pincode = models.CharField(max_length=20, help_text="Postal or PIN code")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.payment_status})"


class OrderItem(models.Model):
    """
    Represents a specific product purchased inside an order.
    
    CONCEPT 3 (RELATIONSHIPS):
    - One Order has Many OrderItems (ForeignKey).
    - Each OrderItem references the purchased Product (ForeignKey).
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, default='M')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Historical price at time of purchase")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size}) in Order #{self.order.id}"

    def get_subtotal(self):
        return self.price * self.quantity
