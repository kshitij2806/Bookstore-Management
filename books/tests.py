from django.test import TestCase
from django.urls import reverse
from .models import Book, User

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            price=19.99,
            stock=10
        )

    def test_book_creation(self):
        book = self.book
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.price, 19.99)
        self.assertEqual(book.stock, 10)

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Test Book")

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

    def test_user_creation(self):
        user = self.user
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))

class BookViewTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            price=19.99,
            stock=10
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_book_detail_view(self):
        response = self.client.get(reverse('books:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertContains(response, "Test Author")
