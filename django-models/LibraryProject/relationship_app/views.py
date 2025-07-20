from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Function-based view to list all books and their authors
def book_list_view(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Function-based view to list all books and their authors
def book_list_view(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/book_list.html', {'books': books})
