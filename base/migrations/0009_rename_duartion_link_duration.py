# Generated by Django 4.1.6 on 2023-02-13 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_link_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='duartion',
            new_name='duration',
        ),
    ]
