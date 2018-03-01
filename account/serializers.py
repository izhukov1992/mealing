from django.contrib.auth.models import User
from rest_framework import serializers

from .constants import ACCOUNT_CREATE_MODERATOR_TYPES
from .models import Account, Moderator, Trainer, Client


class AccountReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Read only fields: id, role, available.
    """

    class Meta:
        model = Account
        fields = ('id', 'role', 'available')
        read_only_fields = ('id', 'role', 'available')


class AccountCreateSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Editable field: role.
    Field role has only 2 choices: CLIENT, TRAINER.
    """

    class Meta:
        model = Account
        fields = ('role', )


class AccountCreateModeratorSerializer(AccountCreateSerializer):
    """Serializer of Account model.
    Editable fields: role.
    Field role has only 1 choice: MODERATOR.
    """

    role = serializers.ChoiceField(ACCOUNT_CREATE_MODERATOR_TYPES)


class AccountSerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Editable field: available.
    Read only fields: id, role.
    """

    class Meta:
        model = Account
        fields = ('id', 'role', 'available')
        read_only_fields = ('id', 'role')


class UserReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account model.
    Read only fields: id, username, email, password, first_name, last_name, account_id, account_role, account_available.
    """

    account = AccountReadOnlySerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_role.
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

        account = Account.objects.create(user=user, **account_data)

        if account.is_moderator:
            Moderator.objects.create(account=account)
        elif account.is_trainer:
            Trainer.objects.create(account=account)
        elif account.is_client:
            Client.objects.create(account=account)

        return user


class UserCreateModeratorSerializer(UserCreateSerializer):
    """Serializer of User model and related Account model.
    Editable fields: username, email, password, first_name, last_name, account_role.
    Field role has only 2 choices: CLIENT, TRAINER.
    """

    account = AccountCreateModeratorSerializer()


class UserSignInSerializer(serializers.ModelSerializer):
    """Serializer of User model.
    Editable fields: username, password.
    """

    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    """Serializer of User model.
    Editable fields: username, email, password, first_name, last_name, account_available.
    Read only fields: id, account_id, account_role.
    """

    account = AccountSerializer()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', )

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)

        user = super(UserSerializer, self).update(instance, validated_data)

        if validated_data.get('password'):
            user.set_password(validated_data.get('password'))
            user.save()

        if account_data is not None:
            account, created = Account.objects.update_or_create(user=user, defaults=account_data)

            if created:
                if account.is_moderator:
                    Moderator.objects.update_or_create(account=account)
                elif account.is_trainer:
                    Trainer.objects.update_or_create(account=account)
                elif account.is_client:
                    Client.objects.update_or_create(account=account)

        return user


class TrainerClientsReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Trainer model.
    Read only fields: id, clients.
    """

    class Meta:
        model = Trainer
        fields = ('id', 'clients')
        read_only_fields = ('id', 'clients')


class TrainerReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Trainer model.
    Read only field: id.
    """

    class Meta:
        model = Trainer
        fields = ('id', )
        read_only_fields = ('id', )


class AccountTrainerReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Read only fields: id, role, available, trainer_id.
    """

    trainer = TrainerReadOnlySerializer()

    class Meta:
        model = Account
        fields = ('id', 'role', 'available', 'trainer')
        read_only_fields = ('id', 'role', 'available', 'trainer')
        
        
class UserTrainerReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account model.
    Read only fields: id, username, first_name, last_name, account_id, account_role, account_available, account_trainer_id.
    """

    account = AccountTrainerReadOnlySerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'account')


class ClientTrainersReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Client model.
    Read only fields: id, trainers.
    """

    class Meta:
        model = Client
        fields = ('id', 'trainers')
        read_only_fields = ('id', 'trainers')


class ClientReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Client model.
    Read only fields: id, limit.
    """

    class Meta:
        model = Client
        fields = ('id', 'limit')
        read_only_fields = ('id', 'limit')


class AccountClientReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of Account model.
    Read only fields: id, role, available, client_id, client_limit.
    """

    client = ClientReadOnlySerializer()

    class Meta:
        model = Account
        fields = ('id', 'role', 'available', 'client')
        read_only_fields = ('id', 'role', 'available', 'client')
        
        
class UserClientReadOnlySerializer(serializers.ModelSerializer):
    """Serializer of User model and related Account model.
    Read only fields: id, username, first_name, last_name, account_id, account_role, account_available, account_client_id, account_client_limit.
    """

    account = AccountClientReadOnlySerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'account')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'account')
