# Generated by Django 5.1.4 on 2024-12-16 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraria', '0017_alter_review_user_reviewee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('category_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=20)),
                ('desc', models.TextField()),
            ],
        ),
    ]
