# api/viewsets.py
from rest_framework import viewsets
from register.models import Register
from chatbot.models import Chatbot
from .serializers import RegisterSerializer, ChatbotSerializer  

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

class ChatbotViewSet(viewsets.ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotSerializer


