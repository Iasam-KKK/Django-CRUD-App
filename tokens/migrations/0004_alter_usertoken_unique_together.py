# Generated by Django 5.0.6 on 2024-06-12 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0003_token_users_alter_token_symbol'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usertoken',
            unique_together=set(),
        ),
    ]
