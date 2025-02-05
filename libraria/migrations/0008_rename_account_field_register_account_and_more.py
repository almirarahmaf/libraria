# Generated by Django 5.1.4 on 2024-12-15 09:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraria', '0007_delete_signup'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='account_field',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='address_field',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='bio_field',
            new_name='bio',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='file_field',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='name_field',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='phone_field',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='role_field',
            new_name='role',
        ),
        migrations.RemoveField(
            model_name='register',
            name='email_field',
        ),
        migrations.RemoveField(
            model_name='register',
            name='join_date',
        ),
        migrations.AddField(
            model_name='register',
            name='signup_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
