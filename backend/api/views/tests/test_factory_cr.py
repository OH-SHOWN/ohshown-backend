from unittest.mock import patch
from uuid import uuid4

import pytest

from conftest import Unordered

from ...models import OhshownEvent, ReportRecord, Image
from .helper import create_ohshown_event, LAT, LNG, OTHERS, NICKNAME, CONTACT, OHSHOWN_EVENT_TYPE, TEST_TIME


pytestmark = pytest.mark.django_db


def test_get_nearby_factory_wrong_params(client):
    # case 1: missing parameter
    resp = client.get("/api/ohshown-events?lat=23")
    assert resp.status_code == 400
    assert resp.content == b"Missing query parameter: lng, range."

    resp = client.get("/api/ohshown-events?lng=121&range=0.2")
    assert resp.status_code == 400
    assert resp.content == b"Missing query parameter: lat."

    # case 2: not querying Taiwan
    resp = client.get("/api/ohshown-events?lat=39.9046126&lng=116.3977254&range=1")
    assert resp.status_code == 400
    assert b"The query position is not in the range of Taiwan." in resp.content

    # case 3: wrong query radius
    resp = client.get("/api/ohshown-events?lat=23&lng=121&range=10000")
    assert resp.status_code == 400
    assert resp.content == b"`range` should be within 0.01 to 100 km, but got 10000.0"

    resp = client.get("/api/ohshown-events?lat=23&lng=121&range=0.001")
    assert resp.status_code == 400
    assert resp.content == b"`range` should be within 0.01 to 100 km, but got 0.001"


def test_get_nearby_factory_called_util_func_correctly(client):

    with patch("api.views.factories_cr._get_nearby_factories") as mock_func:
        lat = 23.12
        lng = 121.5566
        r = 0.5
        client.get(f"/api/ohshown-events?lat={lat}&lng={lng}&range={r}")

        mock_func.assert_called_once_with(
            latitude=lat,
            longitude=lng,
            radius=r,
        )


def test_get_nearby_factory_called_on_test_data(client):

    # in sync with api/tests/test_models.py
    lat = 23.090
    lng = 120.092
    r = 1
    resp = client.get(f"/api/ohshown-events?lat={lat}&lng={lng}&range={r}")
    assert resp.status_code == 200

    factories = resp.json()
    assert len(factories) == 3
    assert (
        [f["name"] for f in factories]
        == Unordered([
            "遭遇事件 No.1",
            "遭遇事件 No.2",
            "遭遇事件 No.3",
        ])
    )
    # See ./api/migrations/0011_change_old_data_source.py to see why it is U or G
    assert all(f["source"] == "U" for f in factories)


def test_create_new_factory_db_status_correct(client):
    im_not_related = Image.objects.create(image_path="https://i.imgur.com/T3pdEyR.jpg")

    data_id, resp, request_body, im1, im2 = create_ohshown_event(client)

    assert resp.status_code == 200

    new_factory_id = resp.json()["id"]
    new_factory = OhshownEvent.objects.get(pk=new_factory_id)

    assert new_factory.lat == LAT
    assert new_factory.lng == LNG
    assert new_factory.ohshown_event_type == OHSHOWN_EVENT_TYPE

    report_records = ReportRecord.objects.filter(factory_id=new_factory_id)
    assert len(report_records) == 1
    report_record = report_records[0]
    assert str(report_record.factory_id) == new_factory_id
    assert report_record.action_type == "POST"
    assert report_record.action_body == request_body
    assert report_record.nickname == NICKNAME
    assert report_record.contact == CONTACT
    assert report_record.others == OTHERS
    assert report_record.created_at == TEST_TIME

    related_images = Image.objects.only("factory_id").filter(id__in=[im1.id, im2.id])
    assert {str(img.factory_id) for img in related_images} == {new_factory_id}

    not_related_images = Image.objects.only("factory_id").filter(id__in=[im_not_related.id])
    assert {str(img.factory_id) for img in not_related_images} == {"None"}


def test_create_new_factory_raise_if_image_id_not_exist(client):
    data_id, resp, *others = create_ohshown_event(client, im2_str=str(uuid4()))

    assert resp.status_code == 400
    assert resp.content == b"please check if every image id exist"


def test_create_new_factory_allow_no_contact(client):
    data_id, resp, *others = create_ohshown_event(client, no_contact=True)

    assert resp.status_code == 200


def test_create_new_factory_allow_empty_type(client):
    data_id, resp, *others = create_ohshown_event(client, empty_type=True)

    assert resp.status_code == 200


def test_create_new_factory_raise_if_not_in_Taiwan(client):
    data_id, resp, *others = create_ohshown_event(client, lat=-23.234, lng=120.1)

    assert resp.status_code == 400
    assert "lat" in resp.json()


def test_create_new_factory_raise_if_type_is_not_invalid(client):
    data_id, resp, *others = create_ohshown_event(client, ohshown_event_type="aaaaa")

    assert resp.status_code == 400
    assert "type" in resp.json()

# TODO: two approaches 1) seed data is ready to resume this test 2) officially removed this api and then remove this
#  test
@pytest.mark.skip(reason="We do not need sectcodes.")
def test_query_factory_by_sectcode(client):
    resp = client.get("/api/sectcode?sectcode=5212&landcode=00190009")
    assert resp.status_code == 200

    data = resp.json()
    assert data["sectname"] == "新生段"

def test_create_factory_after_delete_the_latest_factory_with_maximum_display_number(client):
    factory_with_max_num = OhshownEvent.objects.order_by('-display_number')[0]
    factory_with_max_num.delete()

    assert OhshownEvent.objects.order_by('-display_number')[0].display_number < factory_with_max_num.display_number

    # Create a new factory
    data_id, resp, *others = create_ohshown_event(client)

    assert resp.status_code == 200

    new_factory_with_max_num = OhshownEvent.raw_objects.order_by('-display_number')[0]
    assert new_factory_with_max_num.display_number == factory_with_max_num.display_number + 1
