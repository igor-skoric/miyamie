# Generated by Django 5.1.7 on 2025-05-07 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='website.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Dress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('tag', models.CharField(blank=True, choices=[('new', 'New'), ('bestseller', 'Bestseller'), ('sale', 'Sale')], max_length=20, null=True)),
                ('main_image', models.ImageField(upload_to='dresses/main/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dresses', to='website.category')),
            ],
        ),
        migrations.CreateModel(
            name='DressImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='dresses/extra/')),
                ('dress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='website.dress')),
            ],
        ),
    ]
