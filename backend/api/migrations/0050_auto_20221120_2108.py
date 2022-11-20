# Generated by Django 2.2.13 on 2022-11-20 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_auto_20221119_0334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creature',
            options={'verbose_name': 'Creature', 'verbose_name_plural': 'Creatures'},
        ),
        migrations.AddField(
            model_name='creature',
            name='ohshown_event',
            field=models.ForeignKey(default='cd3fcaca-e1be-4673-a73f-3d40c8a58025', on_delete=django.db.models.deletion.CASCADE, to='api.OhshownEvent'),
            preserve_default=False,
        ),
    ]
