from django.shortcuts import redirect
from django.core.signing import TimestampSigner
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Tier, Image, Link, CustomSize, CustomThumbnail
from .serializers import TierSerializer, LinkSerializer, BasicImageSerializer, PremiumImageSerializer, EnterpriseImageSerializer, CustomImageSerializer, CustomSizeSerializer, CustomThumbnailSerializer

class CustomThumbnailViewSet(viewsets.ModelViewSet):
    queryset = CustomThumbnail.objects.all()
    serializer_class = CustomThumbnailSerializer

class CustomSizeViewSet(viewsets.ModelViewSet):
    queryset = CustomSize.objects.all()
    serializer_class = CustomSizeSerializer

class TierViewSet(viewsets.ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.tier.links:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response = {'message': 'Link function is not offered.'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
            signer = TimestampSigner()
            duration = serializer.validated_data['duration']
            value = 'http://127.0.0.1:8000/link/' + signer.sign(duration)
            serializer.validated_data['owner'] = self.request.user
            serializer.save(url=value)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Link.objects.filter(owner_id=user.id)
        else:
            response = {'message': 'User not authenticated.'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
            return BasicImageSerializer
        if self.request.user.tier.name == "Premium":
            return PremiumImageSerializer 
        if self.request.user.tier.name == "Enterprise":
            return EnterpriseImageSerializer
        return CustomImageSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Image.objects.filter(owner_id=user.id)
        else:
            response = {'message': 'User not authenticated.'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
        response = {'message': 'Link expired.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
        

