import datetime
from freezegun import freeze_time

from ...models import Image, OhshownEvent


LAT = 23.234
LNG = 120.1
OTHERS = "這個工廠實在太臭啦，趕緊檢舉吧"
NICKNAME = "路過的家庭主婦"
CONTACT = "07-7533967"
OHSHOWN_EVENT_TYPE = "2-3"
TEST_TIME = datetime.datetime(2019, 11, 11, 11, 11, 11, tzinfo=datetime.timezone.utc)

# TODO: should be renamed to ohshown_event
def create_factory(cli, im2_str=None, no_contact=False, empty_type=False, lat=None, lng=None,
                   ohshown_event_type=None):
    if not lat:
        lat = LAT
    if not lng:
        lng = LNG
    others = OTHERS
    nickname = NICKNAME
    contact = CONTACT
    if not ohshown_event_type:
        ohshown_event_type = OHSHOWN_EVENT_TYPE

    im1 = Image.objects.create(image_path="https://i.imgur.com/RxArJUc.png")
    im1_str = str(im1.id)
    im2 = Image.objects.create(image_path="https://imgur.dcard.tw/BB2L2LT.jpg")
    if not im2_str:
        im2_str = str(im2.id)

    request_body = {
        "name": "a new factory",
        "type": ohshown_event_type,
        "images": [im1_str, im2_str],
        "others": others,
        "lat": lat,
        "lng": lng,
        "nickname": nickname,
        "contact": contact,
        "datetime": datetime.datetime(2019, 10, 10, 10, 10, 10, tzinfo=datetime.timezone.utc).isoformat(),
    }

    if no_contact:
        del request_body["contact"]
    if empty_type:
        del request_body["type"]


    test_time = TEST_TIME
    with freeze_time(test_time):
        resp = cli.post(
            "/api/ohshown-events", data=request_body, content_type="application/json"
        )
        if resp.status_code == 200:
            data = resp.json()
            update_landcode_with_custom_factory_model(data["id"])
        else:
            data = {"id": None}

        return data["id"], resp, request_body, im1, im2


def update_landcode_with_custom_factory_model(factory_id):
    return OhshownEvent.objects.filter(pk=factory_id).update(
        landcode="853-2",
        sectcode="5404",
        sectname="溪底寮段三寮灣小段",
        towncode="D24",
        townname="臺北市中山區",
    )