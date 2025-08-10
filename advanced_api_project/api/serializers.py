from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields of the Book model

    # Custom validation for publication_year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to show related books dynamically
    books = BookSerializer(many=True, read_only=True)  # 'books' is the related_name in the Book model

    class Meta:
        model = Author
        fields = ['name', 'books']

    # Custom validation for name
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Author name should have at least 2 characters.")
        return value