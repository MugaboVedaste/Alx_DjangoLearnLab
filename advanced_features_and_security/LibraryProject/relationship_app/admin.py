from django.contrib import admin
from .models import Author, Library, Librarian, UserProfile, Review

admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)
admin.site.register(Review)
