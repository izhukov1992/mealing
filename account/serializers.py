from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Account


class UserSerializer(serializers.ModelSerializer):
    """Serializer of User model
    """
    
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'password')
        read_only_fields = ('email', 'is_staff')


class AccountSerializer(serializers.ModelSerializer):
    """Serializer of Account model
    """
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = '__all__'
