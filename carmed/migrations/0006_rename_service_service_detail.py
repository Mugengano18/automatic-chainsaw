# Generated by Django 4.1.3 on 2022-11-30 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carmed', '0005_service'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='service',
            new_name='service_detail',
        ),
    ]
