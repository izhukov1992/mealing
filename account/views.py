from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

from .constants import TRAINER, CLIENT
from .models import Account, Moderator, Trainer, Client
from .serializers import UserReadOnlySerializer, UserCreateSerializer, UserCreateModeratorSerializer, UserSignInSerializer, UserSerializer, UserTrainerReadOnlySerializer, TrainerClientsReadOnlySerializer, UserClientReadOnlySerializer, ClientTrainersReadOnlySerializer
from .permissions import UserOwnerPermissions, AnonymousPermissions, ModeratorPermissions, TrainerPermissions, ClientPermissions


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """View set of Users creating API.
    Used for creating (signing up) Users and related Accounts.
    Authentication token is returned after creating of User and related Account.
    Allowed only for anonymous users.
    """

    permission_classes = [AnonymousPermissions]
    queryset = User.objects.none()
    serializer_class = UserCreateSerializer

    def create(self, request):
        super(UserCreateViewSet, self).create(request)

        payload = api_settings.JWT_PAYLOAD_HANDLER(self.request.user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)

        return Response({'token': token}, status=201)


class UserCreateModeratorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """View set of Users creating API.
    Used for creating Users and related Accounts with type Moderator.
    Authentication token is returned after creating of User and related Account.
    Allowed only for users with moderator type Account.
    """

    permission_classes = [IsAuthenticated, ModeratorPermissions]
    queryset = User.objects.none()
    serializer_class = UserCreateModeratorSerializer


class UserAuthView(APIView):
    """View of authentication API.
    Used for signing in native interface.
    Allowed for everyone.
    """

    serializer_class = UserSignInSerializer
 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(UserReadOnlySerializer(user).data)

            return Response({'details': ["Oops! User is banned.",]}, status=400)

        return Response({'details': ["Oops! Our system does not recognize that username or password.",]}, status=400)
 
    def delete(self, request):
        logout(request)
        return Response()


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """View set of Users API.
    Used for listing, viewing, updating and destroying Users and related Accounts.
    Allowed only for owners.
    """

    permission_classes = [IsAuthenticated, UserOwnerPermissions]
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, user)
        return user


class TrainerClientsViewSet(viewsets.ReadOnlyModelViewSet):
    """View set of Account API.
    Used for listing and viewing Clients of Trainers.
    Allowed only for authenticated users.
    """

    permission_classes = [IsAuthenticated]
    queryset = Trainer.objects.all()
    serializer_class = TrainerClientsReadOnlySerializer


class UserTrainerViewSet(viewsets.ReadOnlyModelViewSet):
    """View set of Account API.
    Used for listing and viewing User, related Account and related Trainer.
    Allowed only for owners.
    """

    permission_classes = [IsAuthenticated, TrainerPermissions, UserOwnerPermissions]
    queryset = User.objects.none()
    serializer_class = UserTrainerReadOnlySerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, user)
        return user


class UserTrainersViewSet(viewsets.ReadOnlyModelViewSet):
    """View set of Account API.
    Used for listing and viewing Users, related Accounts and related Trainers.
    Allowed only for authenticated users.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.none()
    serializer_class = UserTrainerReadOnlySerializer

    def get_queryset(self):
        return User.objects.filter(account__role=TRAINER)


class ClientTrainersViewSet(viewsets.ReadOnlyModelViewSet):
    """View set of Account API.
    Used for listing and viewing Trainers of Clients.
    Allowed only for authenticated users.
    """

    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()
    serializer_class = ClientTrainersReadOnlySerializer


class UserClientViewSet(viewsets.ReadOnlyModelViewSet):
    """View set of Account API.
    Used for listing and viewing User, related Account and related Client.
    Allowed only for owners.
    """

    permission_classes = [IsAuthenticated, ClientPermissions, UserOwnerPermissions]
    queryset = User.objects.none()
    serializer_class = UserClientReadOnlySerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, user)
        return user


class UserClientsViewSet(viewsets.ReadOnlyModelViewSet):
    """View set of Account API.
    Used for listing and viewing Users, related Accounts and related Clients.
    Allowed only for authenticated users.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserClientReadOnlySerializer

    def get_queryset(self):
        return User.objects.filter(account__role=CLIENT)
