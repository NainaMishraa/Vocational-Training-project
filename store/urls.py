"""
store/urls.py

CONCEPT 8 (NAMED URL PATTERNS & URL ROUTING):
Django uses URL dispatcher to map URL patterns to Python view functions.
Giving every path a 'name=' allows reversing URLs cleanly inside views (redirect('home'))
and templates ({% url 'home' %}, {% url 'product_detail' product.slug %}).
This decouples the actual URL paths from the codebase, avoiding broken links if paths change.
"""

from django.urls import path
from . import views

urlpatterns = [
    # 1. Home
    path('', views.home, name='home'),

    # 2. Products / Catalog
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # 3. Cart operations
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # 4. Checkout & Payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.demo_payment, name='demo_payment'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # 5. Customer Orders
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # 6. User Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 7. Informational Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
