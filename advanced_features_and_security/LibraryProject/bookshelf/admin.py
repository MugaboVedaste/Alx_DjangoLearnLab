from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these columns in the list view
    list_filter = ('author', 'publication_year')            # Add sidebar filters
    search_fields = ('title', 'author')                     # Enable search box

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add the additional fields to the existing UserAdmin forms
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth']

admin.site.register(CustomUser, CustomUserAdmin)
