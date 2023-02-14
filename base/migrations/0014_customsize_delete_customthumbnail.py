# Generated by Django 4.1.6 on 2023-02-14 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_link_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
                ('tier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='base.tier')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomThumbnail',
        ),
    ]