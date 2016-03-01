# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('acronym', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=500, null=True, blank=True)),
                ('type', models.IntegerField(choices=[(0, b'Management Group'), (1, b'Working Group'), (2, b'Ad-Hoc Group')])),
                ('status', models.IntegerField(default=0, choices=[(0, b'active'), (1, b'standby'), (2, b'archived')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='affiliation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='affiliation',
            unique_together=set([('user', 'group')]),
        ),
    ]
