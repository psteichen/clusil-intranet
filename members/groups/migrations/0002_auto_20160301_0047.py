# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'active'), (1, b'special'), (2, b'standby'), (3, b'archived')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='type',
            field=models.IntegerField(choices=[(0, b'Management Group'), (1, b'Working Group'), (2, b'Ad-Hoc Group'), (3, b'Tool')]),
            preserve_default=True,
        ),
    ]
