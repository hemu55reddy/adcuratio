from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import LogoutView
from .views import BlogPostViewSet, register_view

app_name = 'blog'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('posts/', BlogPostViewSet.as_view({'get': 'list', 'post': 'create'}), name='blogpost-list'),
    path('posts/<int:pk>/', BlogPostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='blogpost-detail'),
]
