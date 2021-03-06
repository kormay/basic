# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 15:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('secu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('entry_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cms_category', to='secu.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Category')),
                ('entry_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cms_content', to='secu.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentKeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Content')),
                ('entry_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cms_contentkeyword', to='secu.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now=True)),
                ('word', models.CharField(max_length=100)),
                ('entry_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cms_keyword', to='secu.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contentkeyword',
            name='key_word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.KeyWord'),
        ),
    ]
