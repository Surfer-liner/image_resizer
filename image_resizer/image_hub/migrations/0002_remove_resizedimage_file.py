# Generated by Django 4.2.3 on 2023-07-13 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_hub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resizedimage',
            name='file',
        ),
    ]
