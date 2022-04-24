import pytest
from django.db.models.functions.math import Radians, Cos, ACos, Sin

from api.models import OhshownEvent
from conftest import Unordered


@pytest.mark.django_db
def test_migration_seed_data_correctly():
    longitude = 120.092
    latitude = 23.090
    radius_km = 1

    distance = 6371 * ACos(
        Cos(Radians(latitude)) * Cos(Radians("lat")) * Cos(Radians("lng") - Radians(longitude))
        + Sin(Radians(latitude)) * Sin(Radians("lat"))
    )

    factories = OhshownEvent.objects.annotate(distance=distance).filter(
        distance__lt=radius_km,
    )

    assert (
        list(factories.values_list('name', flat=True))
        == Unordered([
            "遭遇事件 No.1",
            "遭遇事件 No.2",
            "遭遇事件 No.3",
        ])
    )
