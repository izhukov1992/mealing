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
        if request.user.is_anonymous():
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
            reporter = Reporter.objects.create(user=user, role=role)
        else:
            reporter = Reporter.objects.create(user=user)
        if request.user.is_anonymous():
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return Response(ReporterSerializer(reporter).data)
        if request.user.is_staff:
            return Response(self.serializer_class(user).data)
        return Response(status=400)

    def perform_update(self, instance):
        email = self.request.data.get('email')
        role = self.request.data.get('role')
        password = self.request.data.get('password')
        user = instance.save(email=email)
        user.set_password(password)
        user.save()
        reporter = Reporter.objects.get(user=user)
        reporter.role = role
        reporter.save()

    def perform_destroy(self, instance):
        reporter = Reporter.objects.get(user=instance).delete()
        super(UserViewSet, self).perform_destroy(instance)


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
        if user:
            login(request, user)
            reporter = Reporter.objects.get(user=user)
            return Response(ReporterSerializer(reporter).data)
        return Response({'details': ["Oops! Our system does not recognize that username or password.",]}, status=400)
 
    def delete(self, request):
        logout(request)
        return Response()
