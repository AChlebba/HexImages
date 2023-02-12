
from .models import CustomUser, Tier, Image
from rest_framework import serializers

class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model   = Tier
        fields  = ['name']

    
class ImageSerializerBasic(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(write_only=True)

    class Meta:
        model       = Image
        read_only_fields = ['thumb200']
        fields      = ['image','thumb200']

class ImageSerializerPremium(serializers.HyperlinkedModelSerializer):

    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400']

class ImageSerializerEnterprise(serializers.HyperlinkedModelSerializer):

    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400']

class ImageSerializerCustom(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['owner', 'image', 'thumb200', 'thumb400']
        
