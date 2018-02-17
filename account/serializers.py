from django.contrib.auth.models import User
from rest_framework import serializers

from meal.serializers import MealSerializer

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Used for listing, viewing, creating and updating Acounts.
    """

    class Meta:
        model = Account
        fields = ('id', 'role', 'limit')
        read_only_fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account.
    Used for creating (signing up) and updating Users and Accounts.
    """

    account = AccountSerializer()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', )

    def create(self, validated_data):
        account_data = validated_data.pop('account')

        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        Account.objects.update_or_create(user=user, defaults=account_data)

        return user

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)

        user = super(UserSerializer, self).update(instance, validated_data)
        if validated_data.get('password'):
            user.set_password(validated_data.get('password'))
            user.save()

        if account_data is not None:
            Account.objects.update_or_create(user=user, defaults=account_data)

        return user


class UserSignInSerializer(serializers.ModelSerializer):
    """Serializer of User model.
    Used for posting credentials (signing in) of User in native interface.
    """

    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')


class AccountPartialSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Used for listing main Users and related Accounts info.
    """

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Account
        fields = '__all__'


class AccountFullSerializer(AccountPartialSerializer):
    """Serializer of Account model.
    Used for listing main Users, related Accounts and related Meals info.
    """

    meals = MealSerializer(source='user.meal_set', many=True, read_only=True)
