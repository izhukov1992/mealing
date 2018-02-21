from django.contrib.auth.models import User
from rest_framework import serializers

from .constants import ACCOUNT_CREATE_TYPES, MODERATOR, TRAINER, CLIENT
from .models import Account, Moderator, Trainer, Client, ClientToTrainer


class AccountReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Read only fields: id, role, limit.
    """

    class Meta:
        model = Account
        fields = ('id', 'role', 'limit')
        read_only_fields = ('id', 'role', 'limit')


class AccountCreateSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Editable fields: role, limit.
    Field role has only 2 choices: CLIENT, TRAINER.
    """

    role = serializers.ChoiceField(ACCOUNT_CREATE_TYPES)

    class Meta:
        model = Account
        fields = ('role', 'limit')


class AccountPersonalSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Editable field: limit.
    Read only fields: id, role.
    """

    class Meta:
        model = Account
        fields = ('id', 'role', 'limit')
        read_only_fields = ('id', 'role')


class AccountStaffSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Editable fields: role, limit.
    Read only field: id.
    """

    class Meta:
        model = Account
        fields = ('id', 'role', 'limit')
        read_only_fields = ('id', )


class UserReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account model.
    Read only fields: id, username, email, password, first_name, last_name, account, account_id, account_role, account_limit.
    """

    account = AccountReadOnlySerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_role, account_limit.
    Field role has only 2 choices: CLIENT, TRAINER.
    """

    account = AccountCreateSerializer()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'account')

    def create(self, validated_data):
        account_data = validated_data.pop('account')

        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        Account.objects.update_or_create(user=user, defaults=account_data)

        return user


class UserSignInSerializer(serializers.ModelSerializer):
    """Serializer of User model.
    Editable fields: username, password.
    """

    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateBaseSerializer(serializers.ModelSerializer):
    """Base serializer.
    Implements update method of User model and related Account model.
    """

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)

        user = super(UserUpdateBaseSerializer, self).update(instance, validated_data)

        if validated_data.get('password'):
            user.set_password(validated_data.get('password'))
            user.save()

        if account_data is not None:
            role = account_data.get('role')

            Account.objects.update_or_create(user=user, defaults=account_data)

            if role is not None:
                account = Account.objects.get(user=user)

                if role == MODERATOR:
                    Moderator.objects.update_or_create(account=account)

                elif role == TRAINER:
                    Trainer.objects.update_or_create(account=account)

                elif role == CLIENT:
                    Client.objects.update_or_create(account=account)

        return user


class UserPersonalSerializer(UserUpdateBaseSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_limit.
    Read only field: id, account_id, account_role.
    """

    account = AccountPersonalSerializer()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', )


class UserPersonalStaffSerializer(UserPersonalSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_limit, account_role.
    Read only field: id, account_id.
    """

    account = AccountStaffSerializer()


class UserStaffSerializer(UserUpdateBaseSerializer):
    """Serializer of User model and related Account model.
    Editable fields: account_limit, account_role.
    Read only field: id, username, email, password, first_name, last_name, account_id.
    """

    account = AccountStaffSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'email', 'first_name', 'last_name')


        
        
        
        
        
        
        
        
        
        


class TrainerClientsReadOnlySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Trainer
        fields = ('id', 'clients')
        read_only_fields = ('id', 'clients')


class TrainerReadOnlySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Trainer
        fields = ('id', )
        read_only_fields = ('id', )


class AccountTrainerReadOnlySerializer(serializers.ModelSerializer):
    """
    """

    trainer = TrainerReadOnlySerializer()

    class Meta:
        model = Account
        fields = ('id', 'role', 'trainer')
        read_only_fields = ('id', 'role', 'trainer')
        
        
class UserTrainerReadOnlySerializer(UserUpdateBaseSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_limit.
    Read only field: id, account_id, account_role.
    """

    account = AccountTrainerReadOnlySerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'account')

        
        
        
        



class ClientTrainersReadOnlySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Client
        fields = ('id', 'trainers')
        read_only_fields = ('id', 'trainers')


class ClientReadOnlySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Client
        fields = ('id', 'limit')
        read_only_fields = ('id', 'limit')


class AccountClientReadOnlySerializer(serializers.ModelSerializer):
    """
    """

    client = ClientReadOnlySerializer()

    class Meta:
        model = Account
        fields = ('id', 'role', 'client')
        read_only_fields = ('id', 'role', 'client')
        
        
class UserClientReadOnlySerializer(UserUpdateBaseSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_limit.
    Read only field: id, account_id, account_role.
    """

    account = AccountClientReadOnlySerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'account')
