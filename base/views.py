from django.shortcuts import redirect
from django.core.signing import TimestampSigner
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Tier, Image, Link
from .serializers import TierSerializer, LinkSerializer, ImageSerializerBasic, ImageSerializerPremium, ImageSerializerEnterprise, ImageSerializerCustom


class TierViewSet(viewsets.ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        signer = TimestampSigner()
        duration = serializer.validated_data['duration']
        value = 'http://127.0.0.1:8000/link/' + signer.sign(duration)
        serializer.save(url=value)

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    
    def get_serializer_class(self):
        if self.request.user.tier.name == "Basic":
            return ImageSerializerBasic
        if self.request.user.tier.name == "Premium":
            return ImageSerializerPremium 
        if self.request.user.tier.name == "Enterprise":
            return ImageSerializerEnterprise
        return ImageSerializerCustom

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Image.objects.filter(owner_id=user.id)
        else:
            return Image.objects.all()

def EncodeLink(request, sig):
    signer = TimestampSigner()
    duration = int(signer.unsign(sig))
    path = 'http://127.0.0.1:8000' + request.path
    link = Link.objects.get(url=path, duration=duration)
    try:
        signer.unsign(sig, duration)
        return redirect(link.image.binary.url)
    except:
        link.delete()
        return redirect("/")
        

