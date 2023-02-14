from django.urls import path, include
from rest_framework import routers
from .views import TierViewSet, ImageViewSet, LinkViewSet, CustomSizeViewSet, CustomThumbnailViewSet, EncodeLink
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'tiers', TierViewSet)
router.register(r'images', ImageViewSet)
router.register(r'links', LinkViewSet)
router.register(r'sizes', CustomSizeViewSet)
router.register(r'customs', CustomThumbnailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('link/<str:sig>', EncodeLink),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
