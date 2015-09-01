# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import purchases.models


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0007_auto_20150625_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('resource', models.FileField(null=True, upload_to=b'', blank=True)),
                ('downloads', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProductPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=purchases.models._create_key, unique=True, max_length=64)),
                ('downloads', models.IntegerField(default=10)),
                ('charge', models.ForeignKey(blank=True, to='djstripe.Charge', null=True)),
                ('product', models.ForeignKey(to='purchases.Product')),
            ],
        ),
    ]
