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
        fields = ('id', 'username', 'email', 'is_staff', 'password')
        read_only_fields = ('email', 'is_staff')


class ReporterSerializer(serializers.ModelSerializer):
    """
    Model serializer of Reporter model
    """
    
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model = Reporter


class ReporterSerializer(serializers.ModelSerializer):
    """
    Model serializer of Reporter model
    """
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reporter
