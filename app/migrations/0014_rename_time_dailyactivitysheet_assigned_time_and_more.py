# Generated by Django 5.0.1 on 2024-03-26 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_dailyactivitysheet_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailyactivitysheet',
            old_name='time',
            new_name='assigned_time',
        ),
        migrations.AddField(
            model_name='dailyactivitysheet',
            name='estimated_completed_time',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
