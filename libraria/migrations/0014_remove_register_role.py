# Generated by Django 5.1.4 on 2024-12-15 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraria', '0013_register_signup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='role',
        ),
    ]
