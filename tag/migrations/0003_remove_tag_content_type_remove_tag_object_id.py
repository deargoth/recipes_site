# Generated by Django 4.1.7 on 2023-05-12 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_alter_tag_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='object_id',
        ),
    ]
