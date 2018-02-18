from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

from .constants import CLIENT, TRAINER, MODERATOR
from .models import Account
from .serializers import AccountSerializer, UserSerializer, UserSignInSerializer, AccountPartialSerializer, AccountFullSerializer
from .permissions import UserPermissions, AccountPermissions


class UserViewSet(viewsets.ModelViewSet):
    """View set of Users API.
    Used for creating (signing up) and updating Users and Accounts.
    Authentication token is returned after creating of User and related Account.
    """

    permission_classes = [UserPermissions, ]
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def create(self, request):
        super(UserViewSet, self).create(request)

        payload = api_settings.JWT_PAYLOAD_HANDLER(self.request.user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)

        return Response({'token': token}, status=201)


class UserAuthView(APIView):
    """View of authentication API.
    Used for signing in native interface.
    """

    serializer_class = UserSignInSerializer
 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(UserSerializer(user).data)

            return Response({'details': ["Oops! User is banned.",]}, status=400)

        return Response({'details': ["Oops! Our system does not recognize that username or password.",]}, status=400)
 
    def delete(self, request):
        logout(request)
        return Response()


class AccountViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """View set of Account API.
    Used for listing, viewing and updating main Account settings.
    """

    permission_classes = [IsAuthenticated, AccountPermissions]
    queryset = Account.objects.none()
    serializer_class = AccountSerializer

    def get_queryset(self):
        all = self.request.query_params.get('all')

        accounts = Account.objects.get_by_user(self.request.user)

        if self.request.user.account.is_staff and all:
            accounts = Account.objects.all()

        return accounts


class AccountPartialViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View set of Account API.
    Used for listing, viewing and updating main Account settings and related meals.
    """

    permission_classes = [IsAuthenticated, AccountPermissions]
    queryset = Account.objects.none()
    serializer_class = AccountPartialSerializer

    def get_queryset(self):
        all = self.request.query_params.get('all')

        accounts = Account.objects.get_by_user(self.request.user)

        if self.request.user.account.is_staff and all:
            accounts = Account.objects.all()

        return accounts


class AccountFullViewSet(AccountPartialViewSet):
    """View set of Account API
    """

    serializer_class = AccountFullSerializer
