# Generated by Django 5.1.7 on 2025-05-07 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_appointment_alter_brand_slug_alter_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_phone', models.CharField(blank=True, default='+381 60 111 111', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='contact@yacht.rs', max_length=254, null=True)),
                ('instagram_link', models.CharField(blank=True, default='www.instagram.com', max_length=255, null=True)),
                ('address', models.CharField(blank=True, default='defautl address', max_length=255, null=True)),
            ],
        ),
    ]
