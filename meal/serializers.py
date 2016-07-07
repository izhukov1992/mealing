from rest_framework import serializers
from .models import Reporter, Meal


class ReporterSerializer(serializers.ModelSerializer):
    """
    Model serializer of Reporter model
    """

    class Meta:
        model = Reporter


class MealSerializer(serializers.ModelSerializer):
    """
    Model serializer of Meal model
    """
    
    reporter = ReporterSerializer()

    class Meta:
        model = Meal
