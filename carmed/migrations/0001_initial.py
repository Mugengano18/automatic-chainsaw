# Generated by Django 4.1.3 on 2022-11-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('business_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=10)),
                ('business_type', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=200)),
                ('sector', models.CharField(max_length=200)),
                ('cell', models.CharField(max_length=200)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
        ),
    ]