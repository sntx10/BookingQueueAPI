# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from api.views import ResourceViewSet, BookingViewSet

router = DefaultRouter()
router.register('resource', ResourceViewSet)
router.register('booking', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
