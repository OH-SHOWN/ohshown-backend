# Generated by Django 2.2.13 on 2023-02-08 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20230208_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traceform',
            old_name='age_days',
            new_name='age_number',
        ),
    ]
