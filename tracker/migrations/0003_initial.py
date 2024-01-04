# Generated by Django 5.0 on 2023-12-22 19:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracker', '0002_delete_bike_remove_variations_fork_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fork',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('damper', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fork_Setting',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('psi', models.DecimalField(decimal_places=1, max_digits=4)),
                ('hsc', models.IntegerField()),
                ('lsc', models.IntegerField()),
                ('hsr', models.IntegerField()),
                ('lsr', models.IntegerField()),
                ('tokens', models.IntegerField()),
                ('ramp_up', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Shock',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('tier', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Shock_Setting',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('psi', models.DecimalField(decimal_places=1, max_digits=4)),
                ('hsc', models.IntegerField()),
                ('lsc', models.IntegerField()),
                ('hsr', models.IntegerField()),
                ('lsr', models.IntegerField()),
                ('tokens', models.IntegerField()),
                ('hbo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('brand', models.CharField(max_length=30)),
                ('front_travel', models.IntegerField()),
                ('rear_travel', models.IntegerField()),
                ('progression', models.DecimalField(decimal_places=2, max_digits=2)),
                ('eye_to_eye', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stroke', models.DecimalField(decimal_places=2, max_digits=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.bike')),
            ],
        ),
        migrations.CreateModel(
            name='Variations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('change_desc', models.TextField()),
                ('fork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.fork')),
                ('fork_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.fork_setting')),
                ('setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.setup')),
                ('shock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.shock')),
                ('shock_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.shock_setting')),
            ],
        ),
    ]