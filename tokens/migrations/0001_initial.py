# Generated by Django 5.0.6 on 2024-06-11 18:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_id', models.IntegerField(default=0, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=20, unique=True)),
                ('quote', models.JSONField(blank=True, null=True)),
                ('last_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_online', models.DateTimeField(auto_now=True)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tokens.token')),
            ],
        ),
    ]
