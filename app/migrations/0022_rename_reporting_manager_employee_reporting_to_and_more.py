# Generated by Django 5.0.1 on 2024-03-30 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_employee_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='reporting_manager',
            new_name='reporting_to',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='team_leader',
        ),
    ]
