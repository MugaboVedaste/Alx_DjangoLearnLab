from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # your blog home page
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # Add other blog URLs here
]
