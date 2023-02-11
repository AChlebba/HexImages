from django.shortcuts import render
from .models import CustomUser, Tier
from rest_framework import viewsets
from .serializers import TierSerializer

def home(request):
    return render(request, 'home.html')


class TierViewSet(viewsets.ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializer