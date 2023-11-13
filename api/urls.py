from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import RegisterViewSet

router = DefaultRouter()
router.register(r'registers', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
