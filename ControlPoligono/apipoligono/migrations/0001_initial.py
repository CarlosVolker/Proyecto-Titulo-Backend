# Generated by Django 5.1.3 on 2024-12-29 02:47

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arma',
            fields=[
                ('id_arma', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_arma', models.IntegerField()),
                ('modelo_arma', models.CharField(max_length=50)),
                ('numero_serie', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FraccionTiro',
            fields=[
                ('id_fraccion', models.AutoField(primary_key=True, serialize=False)),
                ('numero_fraccion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LeccionTiro',
            fields=[
                ('id_leccion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_tiro', models.DateField()),
                ('numero_orden', models.CharField(blank=True, max_length=15, null=True)),
                ('fecha_orden', models.DateField(blank=True, null=True)),
                ('tipo_tiro', models.CharField(blank=True, choices=[('evaluacion', 'Evaluación'), ('entrenamiento', 'Entrenamiento')], max_length=20, null=True)),
                ('cant_tiros_cereo', models.IntegerField()),
                ('cant_tiros_leccion', models.IntegerField()),
                ('distancia', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PoligonoTiro',
            fields=[
                ('id_poligono', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('ciudad', models.CharField(max_length=30)),
                ('carriles_maximos', models.IntegerField()),
                ('distancia_maxima', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rut', models.CharField(max_length=20)),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('limitado', 'Limitado'), ('tirador', 'Tirador')], max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('unidad_regimental', models.CharField(blank=True, max_length=100, null=True)),
                ('unidad_combate', models.CharField(blank=True, max_length=100, null=True)),
                ('unidad_fundamental', models.CharField(blank=True, max_length=100, null=True)),
                ('correo', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Carril',
            fields=[
                ('id_carril', models.AutoField(primary_key=True, serialize=False)),
                ('numero_carril', models.IntegerField()),
                ('id_arma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.arma')),
                ('id_fraccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.fracciontiro')),
            ],
        ),
        migrations.AddField(
            model_name='fracciontiro',
            name='id_leccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.lecciontiro'),
        ),
        migrations.AddField(
            model_name='lecciontiro',
            name='id_poligono',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.poligonotiro'),
        ),
        migrations.CreateModel(
            name='Tirador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grado', models.CharField(blank=True, max_length=50, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_tirador', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoTiro',
            fields=[
                ('id_resultado', models.AutoField(primary_key=True, serialize=False)),
                ('tiros_acertados', models.IntegerField()),
                ('total_tiros', models.IntegerField()),
                ('id_arma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.arma')),
                ('id_carril', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.carril')),
                ('id_tirador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.tirador')),
            ],
        ),
        migrations.AddField(
            model_name='carril',
            name='id_tirador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.tirador'),
        ),
        migrations.CreateModel(
            name='TiradorArma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_arma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.arma')),
                ('id_tirador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apipoligono.tirador')),
            ],
            options={
                'unique_together': {('id_tirador', 'id_arma')},
            },
        ),
    ]
