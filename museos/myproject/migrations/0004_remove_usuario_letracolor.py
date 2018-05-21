# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0003_comentario_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='letracolor',
        ),
    ]
