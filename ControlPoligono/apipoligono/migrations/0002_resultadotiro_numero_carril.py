# Generated by Django 5.1.3 on 2025-01-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apipoligono', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadotiro',
            name='numero_carril',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]