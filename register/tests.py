from django.test import TestCase
from django.urls import reverse
from .models import Mensagem

class MensagemModelTest(TestCase):
    def setUp(self):
        Mensagem.objects.create(texto="Esta é uma mensagem de teste.")

    def test_texto_content(self):
        mensagem = Mensagem.objects.get(id=1)
        expected_object_name = f'{mensagem.texto}'
        self.assertEquals(expected_object_name, 'Esta é uma mensagem de teste.')

class ChatbotViewTest(TestCase):
    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('chatbot'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('chatbot'))
        self.assertTemplateUsed(response, 'bases/base.html')

