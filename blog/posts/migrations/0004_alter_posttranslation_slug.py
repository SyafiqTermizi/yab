# Generated by Django 3.2.9 on 2021-12-24 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_posttranslationimage_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttranslation',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
