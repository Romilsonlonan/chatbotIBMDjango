# api/serializers.py
from rest_framework import serializers
from register.models import Register
from chatbot.models import Chatbot

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class ChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatbot
        fields = '__all__'
