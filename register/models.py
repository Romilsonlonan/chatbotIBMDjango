from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    contatos = models.CharField(max_length=15)

    def __str__(self):
        return self.username

