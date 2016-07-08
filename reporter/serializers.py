from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reporter


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer of User model
    """
    
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        Reporter.objects.create(user=user)
        return user


class ReporterSerializer(serializers.ModelSerializer):
    """
    Model serializer of Reporter model
    """

    class Meta:
        model = Reporter
