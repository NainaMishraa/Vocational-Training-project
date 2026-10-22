"""
store/context_processors.py

CONCEPT 7 (CONTEXT & CONTEXT PROCESSORS):
A context processor is a Python function that takes the HTTP request object as an argument
and returns a dictionary of data to be merged into every template's rendering context.
This makes 'cart_item_count' globally available across header.html and all pages.
"""

from .models import Cart


def cart_counter(request):
    """
    CONCEPT 14 (PYTHON BASICS - FUNCTIONS & CONDITIONS):
    If the visitor is logged in, find their Cart in the database and sum all item quantities.
    If the visitor is an anonymous guest, return 0.
    """
    total_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                total_count = cart.get_total_count()
        except Exception:
            total_count = 0

    return {'cart_item_count': total_count}
