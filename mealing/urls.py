"""mealing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from account.views import UserViewSet, UserAuthView, AccountUserViewSet, AccountUserMealsViewSet
from meal.views import MealViewSet

from .views import MealingIndexView


user_router = routers.DefaultRouter()
user_router.register(r'', UserViewSet)

account_router = routers.DefaultRouter()
account_router.register(r'partial', AccountUserViewSet)
account_router.register(r'full', AccountUserMealsViewSet)

meal_router = routers.DefaultRouter()
meal_router.register(r'', MealViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/meal/', include(meal_router.urls)),
    path('api/v1/account/', include(account_router.urls)),
    path('api/v1/user/', include(user_router.urls)),
    path('api/v1/token/', obtain_jwt_token),
    path('api/v1/auth/', UserAuthView.as_view()),
    path('', MealingIndexView.as_view()),
]
