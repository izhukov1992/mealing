from rest_framework import serializers

from .models import Meal


class MealClientSerializer(serializers.ModelSerializer):
    """Model serializer of Meal model.
    Editable fields: date, time, description, calories.
    Read only fields: id, client.
    """

    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ('id', 'client')


class MealModeratorSerializer(serializers.ModelSerializer):
    """Model serializer of Meal model.
    Editable fields: date, time, description, calories, client.
    Read only field: id.
    """

    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ('id', )
