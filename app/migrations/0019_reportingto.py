# Generated by Django 5.0.1 on 2024-03-28 12:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_delete_reportingto'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportingTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='app.department')),
                ('reporting_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_to', to='app.employee')),
            ],
        ),
    ]
