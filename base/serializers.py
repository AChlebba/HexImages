
from .models import CustomUser, Tier, Image, Link, CustomSize, CustomThumbnail
from rest_framework import serializers


class CustomThumbnailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomThumbnail
        read_only_fields = ['image', 'thumbnail']
        fields = ['image', 'thumbnail']


class CustomSizeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomSize
        read_only_fields = ['tier', 'size']
        fields = ['tier', 'size']


class TierSerializer(serializers.HyperlinkedModelSerializer):
    sizes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='customsize-detail')

    class Meta:
        model   = Tier
        read_only_fields = ['name', 'original', 'thumb200', 'thumb400', 'links', 'sizes']
        fields  = ['name', 'original', 'thumb200', 'thumb400', 'links', 'sizes']


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

    
class BasicImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(write_only=True)
    class Meta:
        model       = Image
        read_only_fields = ['thumb200']
        fields      = ['image','thumb200']

class PremiumImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400']

class EnterpriseImageSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='link-detail')

    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400', 'links']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        fields['links'].queryset = Link.objects.filter(owner_id = request.user.id)
        return fields

class CustomImageSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='link-detail')
    customs = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='customthumbnail-detail')

    class Meta:
        model       = Image
        read_only_fields = ('thumb200', 'thumb400')
        fields      = ['image', 'thumb200', 'thumb400', 'customs', 'links']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        fields['links'].queryset = Link.objects.filter(owner_id = request.user.id)
        return fields

    def to_representation(self, instance):
        rep = super(CustomImageSerializer, self).to_representation(instance)
        request = self.context['request']
        if not request.user.tier.original:
            rep.pop('image', None)
        if not request.user.tier.thumb200:
            rep.pop('thumb200', None)
        if not request.user.tier.thumb400:
            rep.pop('thumb400', None)
        return rep
        
