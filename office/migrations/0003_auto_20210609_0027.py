# Generated by Django 3.2.3 on 2021-06-08 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0002_rename_user_entry_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='joinDate',
        ),
        migrations.AlterField(
            model_name='employee',
            name='isAdmin',
            field=models.BooleanField(default=False, verbose_name='Admin'),
        ),
    ]
