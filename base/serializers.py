from .models import CustomUser, Tier
from rest_framework import serializers

class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tier
        fields = ['name']
