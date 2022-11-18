import uuid

from django.db import models

from .mixins import SoftDeleteMixin


class Creature(SoftDeleteMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    display_number = models.IntegerField(unique=True)

    gender_list = [
        (0, "male"),
        (1, "female"),
        (2, "unknown"),
    ]
    maturity_list = [
        (0, "adult"),
        (1, "juvenile"),
    ]
    size_list = [
        (0, "10-30cm"),
        (1, "30-50cm"),
        (2, "50-70cm"),
        (3, "70-100cm"),
        (4, "100-150cm"),
        (5, ">150cm"),
        (6, "unknown"),
    ]
    gender = models.IntegerField(
        choices=gender_list,
        help_text="Gender of the creature"
    )
    maturity = models.IntegerField(
        choices=maturity_list,
        help_text="Maturity of the creature"
    )
    size = models.IntegerField(
        choices=size_list,
        help_text="Size of the creature"
    )
    misc_feature_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Feature description of the creature"
    )


class RecycledCreature(Creature):
    class Meta:
        proxy = True

    objects = Creature.recycle_objects
