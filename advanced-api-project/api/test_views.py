from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.staff_user = User.objects.create_user(username='staffuser', password='pass1234', is_staff=True)

        # Create authors and books
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')

        self.book1 = Book.objects.create(title='Book A', publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title='Book B', publication_year=2021, author=self.author2)

        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

    # ------------------ LIST & DETAIL TESTS ------------------

    def test_list_books(self):
        """Anyone can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_detail_book(self):
        """Anyone can view book details"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book A')

    # ------------------ CREATE TESTS ------------------

    def test_create_book_authenticated(self):
        """Authenticated user can create a book"""
        self.client.login(username='testuser', password='pass1234')
        data = {
            'title': 'Book C',
            'publication_year': 2022,
            'author': self.author1.pk
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Unauthenticated user cannot create a book"""
        data = {
            'title': 'Book D',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------ UPDATE TESTS ------------------

    def test_update_book_authenticated(self):
        """Authenticated user can update a book"""
        self.client.login(username='testuser', password='pass1234')
        data = {
            'title': 'Updated Book A',
            'publication_year': 2019,
            'author': self.author1.pk
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book A')

    def test_update_book_unauthenticated(self):
        """Unauthenticated user cannot update a book"""
        data = {
            'title': 'Fail Update',
            'publication_year': 2018,
            'author': self.author1.pk
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------ DELETE TESTS ------------------

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book"""
        self.client.login(username='testuser', password='pass1234')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_unauthenticated(self):
        """Unauthenticated user cannot delete a book"""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------ FILTERING, SEARCHING, ORDERING ------------------

    def test_filter_books_by_author(self):
        url = f"{self.list_url}?author={self.author1.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(book['author'] == self.author1.pk for book in response.data))

    def test_search_books_by_title(self):
        url = f"{self.list_url}?search=Book A"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Book A' in book['title'] for book in response.data))

    def test_order_books_by_publication_year(self):
        url = f"{self.list_url}?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
