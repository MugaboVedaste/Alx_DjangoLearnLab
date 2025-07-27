from django import forms
from .models import Book  # Or replace with the model you're using

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']  # Replace with your actual fields
