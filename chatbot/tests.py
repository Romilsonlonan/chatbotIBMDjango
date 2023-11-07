
from django.test import TestCase
from .models import Register
import pytest


class RegisterTestCase(TestCase):

    def test_create_register(self):
        # Cria um novo objeto Register
        register = Register(nome='Romilson', email='romilson@example.com', contatos='+5511999999999')

        # Salva o objeto Register
        register.save()

        # Verifica se o objeto Register foi salvo com sucesso
        self.assertTrue(Register.objects.filter(email='romilson@example.com').exists())

    def test_get_register_by_email(self):
        # Cria um novo objeto Register
        register = Register(nome='Romilson', email='romilson@example.com', contatos='+5511999999999')

        # Salva o objeto Register
        register.save()

        # Obtém o objeto Register pelo e-mail
        register_by_email = Register.objects.get(email='romilson@example.com')

        # Verifica se os dados do objeto Register são os mesmos do objeto criado
        self.assertEqual(register.nome, register_by_email.nome)
        self.assertEqual(register.email, register_by_email.email)
        self.assertEqual(register.contatos, register_by_email.contatos)

    def test_update_register(self):
        # Cria um novo objeto Register
        register = Register(nome='Romilson', email='romilson@example.com', contatos='+5511999999999')

        # Salva o objeto Register
        register.save()

        # Atualiza os dados do objeto Register
        register.nome = 'João'
        register.save()

        # Obtém o objeto Register pelo e-mail
        register_updated = Register.objects.get(email='romilson@example.com')

        # Verifica se os dados do objeto Register foram atualizados
        self.assertEqual(register_updated.nome, 'João')

    def test_delete_register(self):
        # Cria um novo objeto Register
        register = Register(nome='Romilson', email='romilson@example.com', contatos='+5511999999999')

        # Salva o objeto Register
        register.save()

        # Exclui o objeto Register
        register.delete()

        # Verifica se o objeto Register foi excluído
        self.assertFalse(Register.objects.filter(email='romilson@example.com').exists())
