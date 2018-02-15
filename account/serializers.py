from django.contrib.auth.models import User
from rest_framework import serializers

from meal.serializers import MealSerializer

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

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    meals = MealSerializer(source='user.meal_set', many=True)

    class Meta:
        model = Account
        exclude = ('user', )
