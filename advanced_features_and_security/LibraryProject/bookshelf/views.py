from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render, redirect
from books.models import Book

@permission_required('books.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        # Process form data (not shown here)
        pass
    return render(request, 'books/create_book.html')

@permission_required('books.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        # Update book (not shown here)
        pass
    return render(request, 'books/edit_book.html', {'book': book})

@permission_required('books.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/confirm_delete.html', {'book': book})

@permission_required('books.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# views.py
from .forms import BookSearchForm

def search_books(request):
    form = BookSearchForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data['title']
        books = Book.objects.filter(title__icontains=title)
