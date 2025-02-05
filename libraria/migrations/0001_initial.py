# Generated by Django 5.1.4 on 2024-12-14 10:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('signup_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('username_field', models.CharField(max_length=20)),
                ('password_field', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('user_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name_field', models.CharField(max_length=50)),
                ('email_field', models.EmailField(max_length=254, unique=True)),
                ('bio_field', models.CharField(max_length=20)),
                ('file_field', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('address_field', models.TextField()),
                ('phone_field', models.CharField(max_length=20)),
                ('account_field', models.CharField(max_length=20)),
                ('join_date', models.DateField(default=django.utils.timezone.now)),
                ('role_field', models.CharField(choices=[('personal', 'personal'), ('company', 'company')], max_length=8)),
                ('signup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='libraria.signup')),
            ],
        ),
    ]
