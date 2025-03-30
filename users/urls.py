from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserViewSet, home_view, register_view, login_view, UserProfileView

urlpatterns = [
    path('home/', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),

]