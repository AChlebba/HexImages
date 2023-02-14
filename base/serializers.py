
from .models import CustomUser, Tier, Image, Link
from rest_framework import serializers


class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model   = Tier
        fields  = ['name']



class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model   = Link
        read_only_fields = ['url']
        fields  = ['image', 'duration', 'url']
        extra_kwargs = {
            'image': {'write_only': True}
        }

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        fields['image'].queryset = Image.objects.filter(owner_id = request.user.id)
        return fields

    

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
    links = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='link-detail',
    )
    class Meta:
        model = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400', 'links']

class ImageSerializerCustom(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400']
        
