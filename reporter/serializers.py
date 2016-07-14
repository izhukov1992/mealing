#from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Reporter


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer of User model
    """
    
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class ReporterSerializer(serializers.ModelSerializer):
    """
    Model serializer of Reporter model
    """
    
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model = Reporter
