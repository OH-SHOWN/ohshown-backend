import uuid

from django.db import models
from django.contrib.auth import get_user_model

from .mixins import SoftDeleteMixin

CustomUser = get_user_model()


class OhshownEvent(SoftDeleteMixin):
    """Ohshown events that are observed potentially."""

    # List of fact_type & status
    ohshown_event_type_list = [
        ("2-1", "目擊黑熊"),
        ("2-2", "發現痕跡"),
        ("2-3", "其他"),
    ]

    # All Features
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    display_number = models.IntegerField(unique=True)

    lat = models.FloatField()
    lng = models.FloatField()
    
    name = models.CharField(max_length=50, blank=True, null=True)
    ohshown_event_type = models.CharField(
        max_length=3,
        choices=ohshown_event_type_list,
        blank=True,
        null=True,
    )

    sight_see_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ohshown Event"
        verbose_name_plural = "Ohshown Events"


class RecycledOhshownEvent(OhshownEvent):
    class Meta:
        proxy = True

    objects = OhshownEvent.recycle_objects
