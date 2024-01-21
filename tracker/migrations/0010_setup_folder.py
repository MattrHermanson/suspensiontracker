# Generated by Django 5.0 on 2024-01-21 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_var_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setup_Folder',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.bike')),
            ],
        ),
    ]