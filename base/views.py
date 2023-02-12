from .models import CustomUser, Tier, Image
from rest_framework import viewsets
from .serializers import TierSerializer, ImageSerializerBasic, ImageSerializerPremium, ImageSerializerEnterprise, ImageSerializerCustom


class TierViewSet(viewsets.ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    
    def get_serializer_class(self):
        print(self.request.user.tier)
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
            return Image.objects.filter(owner=user)
        else:
            return Image.objects.all()
        

