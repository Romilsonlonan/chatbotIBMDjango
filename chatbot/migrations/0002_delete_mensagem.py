# Generated by Django 4.2.7 on 2023-11-06 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Mensagem",),
    ]