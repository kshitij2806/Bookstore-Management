__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'Bookstore Management System'

from .models import Book, Cart, CartItem
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, AddToCartView, CartView, RemoveFromCartView, UpdateCartItemView, CheckoutView
from .forms import AddToCartForm
from .urls import urlpatterns

def init_app():
    print(f"Initializing {__description__} - Version {__version__}")

import logging
logging.basicConfig(level=logging.INFO)

def log_init():
    logging.info(f"{__description__} Initialized Successfully.")
