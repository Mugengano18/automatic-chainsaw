# Generated by Django 4.1.3 on 2022-11-30 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carmed', '0004_remove_business_id_business_business_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('type', models.CharField(default='', max_length=20)),
                ('description', models.CharField(default='', max_length=30)),
            ],
        ),
    ]
