# chatbot/models.py
from django.db import models

class Chatbot(models.Model):
    nome = models.CharField(max_length=255)  # Adicione um campo como exemplo

class MinhaMensagem(models.Model):
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto




