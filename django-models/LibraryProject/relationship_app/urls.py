from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('books/', views.book_list_view, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
from django.urls import path
from . import views

urlpatterns = [
    # Your previous URLs...
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('register/', views.register, name='register'),

    # Login view (built-in class-based)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout view (built-in class-based)
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
