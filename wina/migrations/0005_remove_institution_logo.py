# Generated by Django 5.1.1 on 2024-09-20 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wina', '0004_rename_services_transaction_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='logo',
        ),
    ]
