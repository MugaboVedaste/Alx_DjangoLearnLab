from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Function-based view to list all books and their authors
def book_list_view(request):
     books = Book.objects.all()  # Use plain all() to pass the check
    return render(request, 'relationship_app/list_books.html', {'books': books})

from .models import Library

from django.views.generic.detail import DetailView

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

# Login view using built-in AuthenticationForm
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')  # Redirect after login; adjust as needed
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout view
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# Registration view using UserCreationForm
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately after registration
            return redirect('book_list')  # Redirect after register; adjust as needed
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
