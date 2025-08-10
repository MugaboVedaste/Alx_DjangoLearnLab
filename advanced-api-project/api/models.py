from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)  # String field for author's name

    def __str__(self):
        return self.name  # Shows author's name in admin interface


class Book(models.Model):
    title = models.CharField(max_length=255)  # String field for book title
    publication_year = models.IntegerField()  # Integer field for publication year
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # If author is deleted, delete related books
        related_name='books'       # Allows accessing books from author: author.books.all()
    )

    def __str__(self):
        return self.title  # Shows book title in admin interface
