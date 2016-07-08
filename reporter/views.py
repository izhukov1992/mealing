from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Reporter
from .serializers import UserSerializer, ReporterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    View set of User API
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReporterViewSet(viewsets.ModelViewSet):
    """
    View set of Reporter API
    """

    queryset = Reporter.objects.all()
    serializer_class = ReporterSerializer

 
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
        return Response(status=401)
 
    def delete(self, request):
        logout(request)
        return Response()
