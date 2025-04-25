from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from .models import Book, Cart, CartItem
from users.models import CustomUser
from django.views.generic import TemplateView

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover_image', 'stock']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        return self.request.user.is_admin

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover_image', 'stock']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        return self.request.user.is_admin

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        return self.request.user.is_admin

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        cart = get_or_create_cart(request)
        
        if cart:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                book=book,
                defaults={'quantity': 1}
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            messages.success(request, f"Added {book.title} to your cart")
            return redirect('book-detail', pk=pk)
        else:
            messages.error(request, "You must be logged in to add to cart")
            return redirect('login')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = get_or_create_cart(request)

        if cart:
            cart_items = cart.items.select_related('book')
            total = sum(item.total_price for item in cart_items)
            return render(request, 'books/cart.html', {
                'cart': cart,
                'cart_items': cart_items,
                'total': total
            })
        return render(request, 'books/cart.html', {'cart_items': [], 'total': 0})

class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        try:
            quantity
