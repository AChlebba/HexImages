# Generated by Django 4.1.6 on 2023-02-12 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='create_date',
            new_name='created_at',
        ),
    ]