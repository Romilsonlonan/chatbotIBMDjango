from django.contrib import admin
from .models import Register

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'contatos']  # Campos a serem exibidos na lista de registros

admin.site.register(Register, RegisterAdmin)
