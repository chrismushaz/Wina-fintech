# Generated by Django 5.1.1 on 2024-09-13 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wina', '0002_rename_service_institution_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='services',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wina.institution'),
            preserve_default=False,
        ),
    ]
