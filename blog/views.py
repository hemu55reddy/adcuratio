from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User(username=username)
        user.set_password(password)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        return render(request, 'registration.html')


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny | IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
            return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You are not authorized to delete this blog"},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.author == self.request.user:
            serializer.save()
            return Response({"message": "Blog updated successfully"})
        else:
            return Response({"message": "You are not authorized to update this blog"},
                            status=status.HTTP_403_FORBIDDEN)

    def login(self, request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({"message": "Login successful"})
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def logout(self, request):
        if request.method == 'POST':
            logout(request)
            return Response({"message": "Logout successful"})
        else:
            return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
