# Generated by Django 4.1.2 on 2022-10-14 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_trends', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest_per_region',
            name='first_keyword_data',
            field=models.TextField(default='test'),
        ),
        migrations.AddField(
            model_name='interest_per_region',
            name='second_keyword_data',
            field=models.TextField(default='test'),
        ),
    ]
