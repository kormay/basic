# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 15:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ConditionTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=1)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=4, null=True)),
                ('form_source', models.CharField(max_length=200)),
                ('data_source', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ProcessCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('parent_code', models.CharField(max_length=20, null=True)),
                ('level', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=4, null=True)),
                ('form_source', models.CharField(max_length=200)),
                ('data_source', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.UUIDField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelationTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.UUIDField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('detail', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('coordinate_x', models.CharField(max_length=10, null=True)),
                ('coordinate_y', models.CharField(max_length=10, null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Process')),
            ],
        ),
        migrations.CreateModel(
            name='StepTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('coordinate_x', models.CharField(max_length=10, null=True)),
                ('coordinate_y', models.CharField(max_length=10, null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.ProcessTemplate')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='current_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Step'),
        ),
        migrations.AddField(
            model_name='route',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Process'),
        ),
        migrations.AddField(
            model_name='relationtemplate',
            name='from_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_step', to='workflow.StepTemplate'),
        ),
        migrations.AddField(
            model_name='relationtemplate',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.ProcessTemplate'),
        ),
        migrations.AddField(
            model_name='relationtemplate',
            name='to_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_step', to='workflow.StepTemplate'),
        ),
        migrations.AddField(
            model_name='relation',
            name='from_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_step', to='workflow.Step'),
        ),
        migrations.AddField(
            model_name='relation',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Process'),
        ),
        migrations.AddField(
            model_name='relation',
            name='to_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_step', to='workflow.Step'),
        ),
        migrations.AddField(
            model_name='node',
            name='step',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow.Step'),
        ),
        migrations.AddField(
            model_name='authortemplate',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.ProcessTemplate'),
        ),
        migrations.AddField(
            model_name='authortemplate',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.StepTemplate'),
        ),
        migrations.AddField(
            model_name='author',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Step'),
        ),
    ]
