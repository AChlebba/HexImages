# Generated by Django 4.1.6 on 2023-02-13 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_duartion_link_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['duration']},
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('image', 'duration')},
        ),
    ]
