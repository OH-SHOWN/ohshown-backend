# Generated by Django 2.2.8 on 2020-01-03 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0032_add_index_to_factory_townname_field"),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE api_factory DROP COLUMN IF EXISTS point",
        )
    ]