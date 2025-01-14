# Generated by Django 5.0.1 on 2024-04-03 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_rename_assigned_by_project_created_by'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DailyActivitySheet',
            new_name='ActivitySheet',
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
            ],
        ),
    ]
