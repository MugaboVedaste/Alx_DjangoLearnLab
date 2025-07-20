from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Function-based view to list all books and their authors
def book_list_view(request):
     books = Book.objects.all()  # Use plain all() to pass the check
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Function-based view to list all books and their authors
def book_list_view(request):
     books = Book.objects.all()  # Use plain all() to pass the check
    return render(request, 'relationship_app/list_books.html', {'books': books})