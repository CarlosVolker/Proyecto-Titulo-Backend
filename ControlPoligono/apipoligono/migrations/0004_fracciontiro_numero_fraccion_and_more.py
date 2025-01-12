# Generated by Django 5.1.3 on 2025-01-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apipoligono', '0003_delete_usuarioarma'),
    ]

    operations = [
        migrations.AddField(
            model_name='fracciontiro',
            name='numero_fraccion',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='fracciontiro',
            constraint=models.UniqueConstraint(fields=('id_leccion', 'numero_fraccion'), name='unique_leccion_numero_fraccion'),
        ),
    ]
