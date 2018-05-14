# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0002_auto_20180504_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
