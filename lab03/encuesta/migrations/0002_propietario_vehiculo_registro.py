# Generated by Django 4.2.15 on 2024-09-03 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('numero_apartamento', models.CharField(max_length=10)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehiculos', to='encuesta.propietario')),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_entrada', models.DateTimeField(verbose_name='Fecha y hora de entrada')),
                ('fecha_hora_salida', models.DateTimeField(blank=True, null=True, verbose_name='Fecha y hora de salida')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros', to='encuesta.vehiculo')),
            ],
        ),
    ]
