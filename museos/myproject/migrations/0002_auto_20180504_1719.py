# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='fax',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='museo',
            name='accesibilidad',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='museo',
            name='telefono',
            field=models.TextField(),
        ),
    ]
