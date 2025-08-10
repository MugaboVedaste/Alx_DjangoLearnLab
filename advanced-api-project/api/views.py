from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import Book, Author
from .serializers import BookSerializer


# ✅ ListView - Retrieve all books (Read-only for unauthenticated users)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read
    # ✅ Enable filtering, search, and ordering
    filter_backends = [
        DjangoFilterBackend,     # For filtering
        filters.SearchFilter,    # For searching
        filters.OrderingFilter,  # For ordering
    ]
    # Filter by exact matches
    filterset_fields = ['title', 'author', 'publication_year']

    # Search (partial matches, case-insensitive)
    search_fields = ['title', 'author__name']

    # Ordering (default and allowed fields)
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


# ✅ DetailView - Retrieve a single book by ID (Read-only for unauthenticated users)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ✅ CreateView - Add new book (Authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in

    def perform_create(self, serializer):
        # Custom logic before saving
        serializer.save()  # Save book normally (you could set author here if needed)


# ✅ UpdateView - Modify existing book (Authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Custom logic during update
        serializer.save()


# ✅ DeleteView - Remove existing book (Authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Custom logic before deleting
        instance.delete()