# Generated by Django 5.0 on 2024-01-17 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_setup_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Var_Note',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('note_title', models.CharField(max_length=200)),
                ('note_body', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.variation')),
            ],
        ),
    ]
