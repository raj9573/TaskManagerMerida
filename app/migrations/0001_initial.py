# Generated by Django 5.0.1 on 2024-03-13 09:06

import app.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(default=app.models.generate_employee_id, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('registered_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('logged_in', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.department')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.position')),
            ],
        ),
        migrations.CreateModel(
            name='DailyActivitySheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('action_planned', models.TextField()),
                ('action_acheived', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('over_due', 'Overdue'), ('completed_on_time', 'Completed On Time'), ('completed_after_time', 'Completed After Time')], default='pending', max_length=100)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.date')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('reporting_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
                ('group_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.taskgroup')),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('priority', models.IntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('over_due', 'Overdue'), ('completed_on_time', 'Completed On Time'), ('completed_after_time', 'Completed After Time')], default='pending', max_length=100)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAssignToGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('over_due', 'Overdue'), ('completed_on_time', 'Completed On Time'), ('completed_after_time', 'Completed After Time')], default='pending', max_length=100)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('group_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.taskgroup')),
                ('task_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tasklist')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAssignToEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('over_due', 'Overdue'), ('completed_on_time', 'Completed On Time'), ('completed_after_time', 'Completed After Time')], default='pending', max_length=100)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
                ('task_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tasklist')),
            ],
        ),
        migrations.CreateModel(
            name='TasksUnderTaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=1000)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('over_due', 'Overdue'), ('completed_on_time', 'Completed On Time'), ('completed_after_time', 'Completed After Time')], default='pending', max_length=100)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('priority', models.IntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
                ('task_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tasklist')),
            ],
        ),
    ]
