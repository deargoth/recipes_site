# Generated by Django 4.1.7 on 2023-05-12 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0003_remove_tag_content_type_remove_tag_object_id'),
        ('recipes', '0003_rename_category_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='tag.tag'),
        ),
    ]
