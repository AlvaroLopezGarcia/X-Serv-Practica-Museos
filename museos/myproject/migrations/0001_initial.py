# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=256)),
                ('distrito', models.CharField(max_length=256)),
                ('barrio', models.CharField(max_length=256)),
                ('descripcion', models.TextField()),
                ('enlace', models.TextField()),
                ('email', models.TextField()),
                ('telefono', models.IntegerField()),
                ('accesibilidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seleccion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('museo', models.ForeignKey(to='myproject.Museo')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('titulo', models.CharField(max_length=256)),
                ('letracolor', models.CharField(max_length=256)),
                ('tamaño', models.CharField(max_length=256)),
                ('fondocolor', models.CharField(max_length=256)),
                ('nombre', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='seleccion',
            name='usuario',
            field=models.ForeignKey(to='myproject.Usuario'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='myproject.Museo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(to='myproject.Usuario'),
        ),
    ]
