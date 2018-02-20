from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

from .models import Account
from .serializers import UserReadOnlySerializer, UserCreateSerializer, UserSignInSerializer, UserClientSerializer, UserClientStaffSerializer, UserStaffSerializer
from .permissions import UserOwnerPermissions, StaffPermissions, AnonymousPermissions


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


class UserClientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """View set of Users API.
    Used for listing, viewing, updating and destroying Users and related Accounts.
    Allowed only for owners.
    Users with staff type Account are able to change Account role, other users are unable.
    """

    permission_classes = [IsAuthenticated, UserOwnerPermissions]
    queryset = User.objects.none()

    def get_serializer_class(self):
        if self.request.user.account.is_staff:
            return UserClientStaffSerializer

        return UserClientSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, user)
        return user


class UserStaffViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """View set of Account API.
    Used for listing and viewing Users and related Accounts and updating Account settings.
    Allowed only for users with staff type Account.
    """

    permission_classes = [IsAuthenticated, StaffPermissions]
    queryset = User.objects.all()
    serializer_class = UserStaffSerializer
