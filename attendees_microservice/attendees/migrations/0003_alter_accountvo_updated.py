# Generated by Django 4.0.3 on 2022-11-17 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_accountvo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountvo',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
