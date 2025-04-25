__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'A Bookstore Management System'

from .models import Book, User
from .views import BookListView, BookDetailView, CartView
from .forms import AddToCartForm

def init_app():
    print(f"Welcome to {__description__}, Version {__version__}")

import logging
logging.basicConfig(level=logging.INFO)

def log_init():
    logging.info("Bookstore Management System package initialized")
