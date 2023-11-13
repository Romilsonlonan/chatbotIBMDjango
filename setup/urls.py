from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.viewsets import RegisterViewSet

router = routers.DefaultRouter()
router.register(r'registers', RegisterViewSet)  # Substitua pelo seu viewset


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('register.urls')),
    path('auth/', include('chatbot.urls')),  
    path('api/', include('api.urls')),
]
