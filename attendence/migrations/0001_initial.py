# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 15:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('secu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjustment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('adjustment_type', models.CharField(choices=[('L', 'Leave'), ('O', 'Over Time')], max_length=10)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdjustmentLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('operation', models.CharField(choices=[('1', 'Approved'), ('2', 'Denied')], max_length=10)),
                ('adjustment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendence.Adjustment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='secu.User')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('entry_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeIP',
            fields=[
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('IP', models.GenericIPAddressField(primary_key=True, protocol='IPv4', serialize=False, unique=True)),
                ('entry_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendence_employeeip', to='secu.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secu.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Punch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('punch_date', models.DateTimeField(default=datetime.datetime.now)),
                ('is_normal', models.BooleanField(default=True)),
                ('IP', models.GenericIPAddressField()),
                ('entry_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendence_punch', to='secu.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secu.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='adjustmentlog',
            name='entry_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendence_adjustmentlog', to='secu.User'),
        ),
        migrations.AddField(
            model_name='adjustment',
            name='entry_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendence_adjustment', to='secu.User'),
        ),
        migrations.AddField(
            model_name='adjustment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secu.User'),
        ),
    ]
