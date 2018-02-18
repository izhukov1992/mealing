from rest_framework import serializers

from .models import Meal


class MealSerializer(serializers.ModelSerializer):
    """Model serializer of Meal model.
    Used for listing, viewing, creating, updating and deleting Meals.
    """

    class Meta:
        model = Meal
        fields = '__all__'
