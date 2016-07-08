from rest_framework import serializers
from .models import Meal


class MealSerializer(serializers.ModelSerializer):
    """
    Model serializer of Meal model
    """

    class Meta:
        model = Meal
