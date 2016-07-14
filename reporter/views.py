from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Reporter
from .serializers import UserSerializer, ReporterSerializer
from .permissions import UserPermissions, ReporterUserPermissions


class UserViewSet(viewsets.ModelViewSet):
    """
    View set of User API
    """

    permission_classes = [UserPermissions,]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return [self.request.user]
 
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            reporter = Reporter.objects.create(user=user)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return Response(ReporterSerializer(reporter).data)
        return Response(serializer.errors, status=400)


class ReporterViewSet(viewsets.ModelViewSet):
    """
    View set of Reporter API
    """

    permission_classes = [ReporterUserPermissions,]
    queryset = Reporter.objects.all()
    serializer_class = ReporterSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reporter.objects.all()
        return Reporter.objects.filter(user=self.request.user)

 
class AuthView(APIView):
    """
    View of authentication API
    """

    serializer_class = UserSerializer
 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                reporter = Reporter.objects.get(user=user)
                return Response(ReporterSerializer(reporter).data)
        return Response(status=400)
 
    def delete(self, request):
        logout(request)
        return Response()
