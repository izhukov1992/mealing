from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .constants import CLIENT, TRAINER, MODERATOR
from .models import Account
from .serializers import UserSerializer, AccountSerializer
from .permissions import UserPermissions, AccountUserPermissions


class UserViewSet(viewsets.ModelViewSet):
    """View set of User API
    """

    permission_classes = [UserPermissions,]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        if self.request.user.is_staff or account.role == MODERATOR:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
 
    def create(self, request):
        username = request.data.get('username')
        if username and User.objects.filter(username=username):
            return Response({'username': ["Oops! That username is not available. Try a different username.",]}, status=400)
        email = request.data.get('email')
        role = request.data.get('role')
        password_confirm = request.data.get('password_confirm')
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        password = serializer.validated_data.get('password')
        if request.user.is_anonymous:
            if not password == password_confirm:
                return Response({'details': ["Password confirmation doesn\'t match.",]}, status=400)
        username = serializer.validated_data.get('username')
        if email:
            user = User.objects.create(username=username, email=email)
        else:
            user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        if role:
            account = Account.objects.create(user=user, role=role)
        else:
            account = Account.objects.create(user=user)
        if request.user.is_anonymous:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return Response(AccountSerializer(account).data)
        account = Account.objects.get(user=self.request.user)
        if request.user.is_staff or account.role == MODERATOR:
            return Response(self.serializer_class(user).data)
        return Response(status=400)

    def perform_update(self, instance):
        email = self.request.data.get('email')
        role = self.request.data.get('role')
        password = self.request.data.get('password')
        user = instance.save(email=email)
        user.set_password(password)
        user.save()
        if user == self.request.user:
            user = authenticate(username=user.username, password=password)
            login(self.request, user)
        account = Account.objects.get(user=user)
        account.role = role
        account.save()

    def perform_destroy(self, instance):
        account = Account.objects.get(user=instance).delete()
        super(UserViewSet, self).perform_destroy(instance)


class AccountViewSet(viewsets.ModelViewSet):
    """View set of Account API
    """

    permission_classes = [AccountUserPermissions,]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        if self.request.user.account.is_staff:
            return Account.objects.all()

        return Account.objects.get_by_user(self.request.user)

    def perform_create(self, serializer):
        user = serializer.validated_data.get('user')

        if self.request.user.account.is_staff and user:
            meal = serializer.save(user=user)
        else:
            meal = serializer.save(user=self.request.user)


class AuthView(APIView):
    """View of authentication API
    """

    serializer_class = UserSerializer
 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            account = Account.objects.get_or_create(user=user, role=(MODERATOR if user.is_staff else CLIENT))
            account = user.account
            return Response(AccountSerializer(account).data)
        return Response({'details': ["Oops! Our system does not recognize that username or password.",]}, status=400)
 
    def delete(self, request):
        logout(request)
        return Response()
