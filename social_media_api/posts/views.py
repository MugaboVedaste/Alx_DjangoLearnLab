from rest_framework import viewsets, permissions, status, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification



class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allow owners of an object to edit/delete it."""

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for owner
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

class LikePostView(generics.GenericAPIView):
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ Required
        like, created = Like.objects.get_or_create(user=request.user, post=post)  # ✅ Required

        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target=post
        )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_200_OK)

class UnlikePostView(generics.GenericAPIView):
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            like.delete()
            return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
