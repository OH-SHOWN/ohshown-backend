import datetime
from freezegun import freeze_time

from ...models import Image, OhshownEvent


# TODO: should be renamed to ohshown_event
def create_factory(cli):
    lat = 23.234
    lng = 120.1
    others = "這個工廠實在太臭啦，趕緊檢舉吧"
    nickname = "路過的家庭主婦"
    contact = "07-7533967"
    ohshown_event_type = "2-3"

    im1 = Image.objects.create(image_path="https://i.imgur.com/RxArJUc.png")
    im2 = Image.objects.create(image_path="https://imgur.dcard.tw/BB2L2LT.jpg")

    request_body = {
        "name": "a new factory",
        "type": ohshown_event_type,
        "images": [str(im1.id), str(im2.id)],
        "others": others,
        "lat": lat,
        "lng": lng,
        "nickname": nickname,
        "contact": contact,
        "datetime": datetime.datetime(2019, 10, 10, 10, 10, 10, tzinfo=datetime.timezone.utc).isoformat(),
    }

    test_time = datetime.datetime(2019, 11, 11, 11, 11, 11, tzinfo=datetime.timezone.utc)
    with freeze_time(test_time):
        resp = cli.post(
            "/api/ohshown-events", data=request_body, content_type="application/json"
        )
        data = resp.json()
        update_landcode_with_custom_factory_model(data["id"])
        return data["id"]



def update_landcode_with_custom_factory_model(factory_id):
    OhshownEvent.objects.filter(pk=factory_id).update(
        landcode="853-2",
        sectcode="5404",
        sectname="溪底寮段三寮灣小段",
        towncode="D24",
        townname="臺北市中山區",
    )