# Generated by Django 4.1.6 on 2023-02-11 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_tier'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tier',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.tier'),
        ),
    ]
