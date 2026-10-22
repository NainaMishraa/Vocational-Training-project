"""
store/admin.py

CONCEPT 11 (DJANGO ADMIN CUSTOMIZATION):
Django provides a built-in, production-ready admin dashboard out of the box.
By subclassing admin.ModelAdmin, we customize how our models look and behave in the admin:
- list_display: specifies which columns/fields appear in the list table.
- search_fields: adds a live search bar matching specified fields.
- list_filter: generates right-side filter menus (by category, date, status, etc.).
- list_editable: allows editing fields directly from the list page without opening each record.
- prepopulated_fields: automatically generates slugs as the admin types the name.
- inlines: displays child records (like OrderItem) inline inside the parent record (Order).
"""

from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


# ==============================================================================
# CATEGORY ADMIN
# ==============================================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


# ==============================================================================
# PRODUCT ADMIN
# ==============================================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns shown in admin product table
    list_display = [
        'name',
        'category',
        'price',
        'stock',
        'size',
        'gender',
        'is_available',
        'created_at',
    ]
    # Allow quick in-table editing of stock, price and availability
    list_editable = ['price', 'stock', 'is_available']
    # Filter sidebar options
    list_filter = ['category', 'gender', 'is_available', 'created_at']
    # Search box for products
    search_fields = ['name', 'description']
    # Auto-generate URL slug from product name
    prepopulated_fields = {'slug': ('name',)}


# ==============================================================================
# CART & CART ITEM ADMIN
# ==============================================================================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'size']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'item_count', 'grand_total']
    inlines = [CartItemInline]

    def item_count(self, obj):
        return obj.get_total_count()
    item_count.short_description = 'Total Items'

    def grand_total(self, obj):
        return f"₹{obj.get_total_price():.2f}"
    grand_total.short_description = 'Grand Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'size', 'quantity']
    list_filter = ['size', 'cart__user']
    search_fields = ['product__name', 'cart__user__username']


# ==============================================================================
# ORDER & ORDER ITEM ADMIN
# ==============================================================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'size', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'full_name',
        'phone',
        'city',
        'total_amount',
        'payment_status',
        'order_status',
        'created_at',
    ]
    # Allow staff to update order_status and payment_status directly in the table
    list_editable = ['order_status', 'payment_status']
    list_filter = ['order_status', 'payment_status', 'created_at']
    search_fields = ['full_name', 'phone', 'city', 'pincode', 'user__username', 'id']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'size', 'quantity', 'price']
    list_filter = ['size']
    search_fields = ['product__name', 'order__id', 'order__user__username']
