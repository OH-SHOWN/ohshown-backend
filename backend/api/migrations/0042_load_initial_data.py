import csv
import itertools
import os
import sys
from datetime import datetime

from django.db import migrations
from django.conf import settings


# TODO: This migration is based on 0002_load_initial_data.py and some of the
# following migrations like 0009_modify_old_data_value.py to help me the
# compatibility of csv format. When we deliver the expected format and content
# of seed-data-ohshown-event.csv, this migration is expected to be updated (or
# updated by the subsequent migrations).
SEED_DATA_PATH = os.path.join(settings.BASE_DIR, "fixtures/seed-data-ohshown-event.csv")


def forward_func(apps, schema_editor):
    Ohshown_event = apps.get_model("api", "OhshownEvent")

    with open(SEED_DATA_PATH, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        # HACK: when testing the code, do not import the seed data to speed up testing
        # ref: commit 7f8317942649483ff3ef16f2ffdf1e6911887229
        if any("test" in arg for arg in sys.argv):
            reader = itertools.islice(reader, 0, 101)

        seed_ohshown_events = []
        for idx, datum in enumerate(reader):
            try:
                lng = float(datum["經度"])
                lat = float(datum["緯度"])
            except ValueError:
                continue
            ohshown_event = Ohshown_event(
                lng=lng,
                lat=lat,
                landcode=datum["地號"],
                status_time=datetime.now(),
                name=f"遭遇事件 No.{idx}",
                display_number=idx,
            )
            seed_ohshown_events.append(ohshown_event)

    Ohshown_event.objects.bulk_create(seed_ohshown_events)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0041_rename_factory_model"),
    ]

    operations = [
        migrations.RunPython(
            code=forward_func,
            reverse_code=None,
        ),
    ]
