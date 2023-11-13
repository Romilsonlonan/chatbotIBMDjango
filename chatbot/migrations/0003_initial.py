# Generated by Django 4.2.7 on 2023-11-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("chatbot", "0002_delete_mensagem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mensagem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("texto", models.TextField()),
                ("data_envio", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
