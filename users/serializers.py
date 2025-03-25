from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'date_joined', 'phone_number', 'address', 'profile_picture'
        ]
        read_only_fields = ['id', 'date_joined']
