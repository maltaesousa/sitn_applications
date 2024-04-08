# Generated by Django 4.0.5 on 2024-03-27 15:04

import django.contrib.gis.db.models.fields
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cadastre',
            fields=[
                ('idobj', models.UUIDField(primary_key=True, serialize=False)),
                ('numcad', models.BigIntegerField()),
                ('cadnom', models.CharField(max_length=50)),
                ('numcom', models.BigIntegerField()),
                ('nufeco', models.BigIntegerField()),
                ('comnom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'general"."la02_cadastres',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('idobj', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('comnom', models.CharField(max_length=100)),
                ('numcom', models.BigIntegerField()),
                ('nufeco', models.BigIntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2056)),
            ],
            options={
                'db_table': 'general"."la3_limites_communales',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImmeublesAdressesSearch',
            fields=[
                ('noobj', models.IntegerField(primary_key=True, serialize=False)),
                ('cadnum', models.IntegerField()),
                ('cadnom', models.CharField(max_length=100)),
                ('nummai', models.CharField(max_length=7)),
                ('idemai', models.CharField(max_length=50)),
                ('typimm', models.CharField(max_length=17)),
                ('comnum', models.IntegerField()),
                ('comnom', models.CharField(max_length=80)),
                ('adresse_partielle', models.CharField(max_length=250)),
                ('adresse', models.CharField(max_length=500)),
                ('nom_localite', models.CharField(max_length=250)),
                ('label', models.CharField(max_length=250)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=2056)),
                ('_ts', django.contrib.postgres.search.SearchVectorField()),
            ],
            options={
                'db_table': 'searchtables"."search_immeubles_adresses_new',
                'managed': False,
            },
        ),
    ]
