# Generated by Django 4.1.3 on 2022-12-01 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carmed', '0002_alter_service_detail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_detail',
            name='status',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='carmed.statuses'),
        ),
    ]
