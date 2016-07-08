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


class ReporterSerializer(serializers.ModelSerializer):
    """
    Model serializer of Reporter model
    """

    user = UserSerializer()

    class Meta:
        model = Reporter

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['user']['username'])
        user.set_password(validated_data['user']['password'])
        user.save()

        return Reporter.objects.create(user=user, limit=validated_data['limit'])
