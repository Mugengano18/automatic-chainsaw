# Generated by Django 4.1.3 on 2022-11-18 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carmed', '0002_rename_cell_business_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]