from django.urls import path, include
from rest_framework import routers
from .views import home, TierViewSet

router = routers.DefaultRouter()
router.register(r'tiers', TierViewSet)

urlpatterns = [
    # path('', home, name='home'),

    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]
