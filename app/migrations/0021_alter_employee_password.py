# Generated by Django 5.0.1 on 2024-03-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_employee_reporting_manager_employee_team_leader_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(max_length=2000000),
        ),
    ]
