from rest_framework import serializers

from .models import historical, interest_per_region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = interest_per_region
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = historical
        fields = '__all__'