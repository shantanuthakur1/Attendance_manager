# Generated by Django 3.2.3 on 2021-06-08 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='user',
            new_name='employee',
        ),
    ]
