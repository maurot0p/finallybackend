# Generated by Django 4.0.5 on 2022-06-21 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_alter_account_current_balance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
    ]
