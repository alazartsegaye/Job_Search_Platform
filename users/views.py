from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly, OnlyAdminAccess
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse

# User API ViewSet (Only Admins Can Access)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OnlyAdminAccess]

# Home View
def home_view(request):
    return render(request, 'users/home.html')

# User Profile API View (Authenticated Users Only)
class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user

# Register View (Token Generates )
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            messages.success(request, "Registration successful.")
            return JsonResponse({'token': token.key, 'message': 'Registration successful'})
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            return JsonResponse({'error': 'Registration failed. Please check the form.'}, status=400)
    form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

# Login View (Token Required)
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            token_exists = Token.objects.filter(user=user).exists()
            if not token_exists:
                return JsonResponse({'error': 'Token required. Please register again to get a token.'}, status=403)

            login(request, user)
            token = Token.objects.get(user=user)
            return JsonResponse({'token': token.key, 'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})
