# Generated by Django 5.1.4 on 2024-12-16 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraria', '0015_rename_register_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='review_user',
            fields=[
                ('reviewuser_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('rating', models.PositiveSmallIntegerField()),
                ('reviewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_received', to='libraria.profile')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_given', to='libraria.profile')),
            ],
        ),
    ]
