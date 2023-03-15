import logging
from typing import List
import datetime

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction
from django_q.tasks import async_task
from rest_framework.decorators import api_view
from django.db.models import Max, Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .utils import _get_nearby_factories, _get_client_ip
from ..models import OhshownEvent, Image, ReportRecord, Creature, Reporter, ShownForm, TraceForm
from ..serializers import FactorySerializer

LOGGER = logging.getLogger("django")
FactoryDoesNotExist = OhshownEvent.DoesNotExist


def _in_taiwan(lat, lng):
    return (
        settings.TAIWAN_MIN_LATITUDE <= lat <= settings.TAIWAN_MAX_LATITUDE
        and settings.TAIWAN_MIN_LONGITUDE <= lng <= settings.TAIWAN_MAX_LONGITUDE
    )


def _in_reasonable_radius_range(radius):
    # NOTE: need discussion about it
    return 0.01 <= radius <= 100

def _all_image_id_exist(image_ids: List[str]) -> bool:
    images = Image.objects.only("id").filter(id__in=image_ids)
    return len(images) == len(image_ids)


def _handle_get_ohshown_events(request):
    try:
        latitude = request.GET["lat"]  # 緯度: y
        longitude = request.GET["lng"]  # 經度: x
        radius = request.GET["range"]  # km
    except MultiValueDictKeyError:
        missing_params = [p for p in ("lat", "lng", "range") if p not in request.GET]
        missing_params = ", ".join(missing_params)
        return HttpResponse(
            f"Missing query parameter: {missing_params}.",
            status=400,
        )

    latitude, longitude = float(latitude), float(longitude)
    if not _in_taiwan(latitude, longitude):
        return HttpResponse(
            "The query position is not in the range of Taiwan."
            "Valid query parameters should be: "
            f"{settings.TAIWAN_MIN_LONGITUDE} < lng < {settings.TAIWAN_MAX_LONGITUDE}, "
            f"{settings.TAIWAN_MIN_LATITUDE} < lat < {settings.TAIWAN_MAX_LATITUDE}.",
            status=400,
        )

    radius = float(radius)
    if not _in_reasonable_radius_range(radius):
        return HttpResponse(
            f"`range` should be within 0.01 to 100 km, but got {radius}",
            status=400,
        )

    nearby_factories = _get_nearby_factories(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )

    serializer = FactorySerializer(nearby_factories, many=True)
    return JsonResponse(serializer.data, safe=False)

def _handle_create_ohshown_events(request):
    post_body = request.data
    user_ip = _get_client_ip(request)

    LOGGER.debug(f"Received request body: {post_body} to create factory")

    serializer = FactorySerializer(data=post_body)
    if not serializer.is_valid():
        LOGGER.warning(f"{user_ip} : <serializer errors> ")
        return JsonResponse(
            serializer.errors,
            status=400,
        )

    image_ids = post_body.get("images", [])
    if not _all_image_id_exist(image_ids):
        LOGGER.warning(f"{user_ip} : <please check if every image id exist> ")
        return HttpResponse(
            "please check if every image id exist",
            status=400,
        )

    num = OhshownEvent.raw_objects.aggregate(Max("display_number"))

    sight_see_timestamp_to_datetime = post_body["datetime"] / 1e3

    new_ohshown_event_field = {
        "name": post_body["name"],
        "lat": post_body["lat"],
        "lng": post_body["lng"],
        "sight_see_date_time": datetime.datetime.fromtimestamp(sight_see_timestamp_to_datetime),
        "ohshown_event_type": post_body.get("type"),
        "status_time": datetime.datetime.now(),
        "display_number": num["display_number__max"] + 1,
        "ground_type": post_body.get("groundTypes"),
        "vegetation": post_body.get("vegetations"),
        "bear_attractor": post_body.get("bearAttractors"),
        "ohshown_again": post_body.get("ohshownAgain"),
        "ohshown_again_reason": post_body.get("ohshownAgainReason"),
        "prevent_ohshown_methods": post_body.get("preventOhshownMethods"),
        "prevent_ohshown_methods_text_object": post_body.get("preventOhshownMethodsTextObject"),
        "survey_if_bear_exist": post_body.get("surveyIfBearExist"),
    }

    new_creatures_field = []
    if "bearNumber" in post_body:
        num_creature = Creature.raw_objects.aggregate(Max("display_number"))
        # corner case when nothing in the db at the very beginning
        if num_creature["display_number__max"] is None:
            num_creature_max = -1
        else:
            num_creature_max = num_creature["display_number__max"]
        cnt = 1
        for creature in post_body["bears"]:
            new_creature_field = {
                "maturity": creature["bearType"],
                "size": creature["bearSize"],
                "gender": creature["bearSex"],
                "display_number": num_creature_max + cnt,
            }
            new_creatures_field.append(new_creature_field)
            cnt = cnt + 1

    new_report_record_field = {
        "action_type": "POST",
        "action_body": post_body,
        "nickname": post_body.get("nickname"),
        "contact": post_body.get("contact"),
        "others": post_body.get("others", ""),
    }

    new_reporter_field = {
        "contact_name": post_body.get("contactName"),
        "contact_phone": post_body.get("contactPhone"),
        "contact_mail": post_body.get("contactMail"),
    }

    new_shown_form_field = {
        "ohshown_feeling": post_body.get("ohshownFeeling"),
        "human_number": post_body.get("humanNumber"),
        "human_behavior": post_body.get("humanBehavior"),
        "human_behavior_text_object": post_body.get("humanBehaviorTextObject"),
        "distance": post_body.get("distance"),
        "bear_behavior": post_body.get("bearBehavior"),
        "bear_behavior_text_object": post_body.get("bearBehaviorTextObject"),
        "food": post_body.get("food"),
        "food_text_object": post_body.get("foodTextObject"),
        "bear_notice": post_body.get("bearNotice"),
        "bear_notice_minutes": post_body.get("bearNoticeMinutes"),
        "human_reaction": post_body.get("humanReaction"),
        "human_reaction_text_object": post_body.get("humanReactionTextObject"),
        "bear_reaction": post_body.get("bearReaction"),
        "bear_reaction_text_object": post_body.get("bearReactionTextObject"),
        "human_hurt": post_body.get("humanHurt"),
        "human_hurt_text": post_body.get("humanHurtDescription"),
    }

    new_trace_form_field = {
        "trace_type": post_body.get("traceType"),
        "trace_type_text_object": post_body.get("traceTypeTextObject"),
        "age_type": post_body.get("ageType"),
        "age_number": post_body.get("ageNumber"),
        "other_info": post_body.get("otherInfo"),
    }
    if post_body.get("imageAvailable"):
        new_trace_form_field.image_available = post_body.imageAvailable 

    with transaction.atomic():
        new_ohshown_event = OhshownEvent.objects.create(**new_ohshown_event_field)
        if "bearNumber" in post_body:
            for creature_field in new_creatures_field:
                Creature.objects.create(
                    ohshown_event=new_ohshown_event,
                    **creature_field,
                )
        report_record = ReportRecord.objects.create(
            factory=new_ohshown_event,
            **new_report_record_field,
        )
        Image.objects.filter(id__in=image_ids).update(
            factory=new_ohshown_event, report_record=report_record
        )
        Reporter.objects.create(**new_reporter_field)
        if post_body.get("type") == '2-1':
            ShownForm.objects.create(**new_shown_form_field)
        elif post_body.get("type") == '2-2':
            TraceForm.objects.create(**new_trace_form_field)

    serializer = FactorySerializer(new_ohshown_event)
    LOGGER.info(
        f"{user_ip}: <Create new factory> at {(post_body['lng'], post_body['lat'])} "
        f"id:{new_ohshown_event.id} {new_ohshown_event_field['name']} {new_ohshown_event_field['ohshown_event_type']}",
    )
    async_task("api.tasks.update_landcode", new_ohshown_event.id)
    return JsonResponse(serializer.data, safe=False)


@swagger_auto_schema(
    method="get",
    operation_summary="得到中心座標往外指定範圍的已有工廠資料",
    responses={200: openapi.Response("工廠資料", FactorySerializer), 400: "request failed"},
    manual_parameters=[
        openapi.Parameter(
            name="lng",
            in_=openapi.IN_QUERY,
            description=f"{settings.TAIWAN_MIN_LONGITUDE} < lng < {settings.TAIWAN_MAX_LONGITUDE}",
            type=openapi.TYPE_NUMBER,
            required=True,
            example="Custom Example Data",
        ),
        openapi.Parameter(
            name="lat",
            in_=openapi.IN_QUERY,
            description=f"{settings.TAIWAN_MIN_LATITUDE} < lat < {settings.TAIWAN_MAX_LATITUDE}",
            type=openapi.TYPE_NUMBER,
            required=True,
        ),
        openapi.Parameter(
            name="range",
            in_=openapi.IN_QUERY,
            description="km",
            type=openapi.TYPE_NUMBER,
            required=True,
        ),
    ],
)
@swagger_auto_schema(
    method="post",
    operation_summary="新增指定 id 的工廠欄位資料",
    request_body=FactorySerializer,
    responses={200: openapi.Response("新增的工廠資料", FactorySerializer), 400: "request failed"},
    auto_schema=None,
)
@api_view(["GET", "POST"])
def get_nearby_or_create_ohshown_events(request):
    if request.method == "GET":
        return _handle_get_ohshown_events(request)
    elif request.method == "POST":
        return _handle_create_ohshown_events(request)

@swagger_auto_schema(
    method="get",
    operation_summary="使用地段號取得工廠資料",
    responses={200: openapi.Response("工廠資料", FactorySerializer), 400: "request failed"},
    manual_parameters=[
        openapi.Parameter(
            name="sectcode",
            in_=openapi.IN_QUERY,
            description="地號可以到 https://easymap.land.moi.gov.tw/ 查詢, 例如新莊區海山頭段石龜小段的段號就是 0308",
            type=openapi.TYPE_NUMBER,
            required=True,
            example="0308",
        ),
        openapi.Parameter(
            name="landcode",
            in_=openapi.IN_QUERY,
            description="段號, 目前只接受八碼的格式, 例如 82號之18 (82-18) 請使用 00820018 來搜尋",
            type=openapi.TYPE_NUMBER,
            required=True,
            example="00820018"
        )
    ],
)
@api_view(["GET"])
def get_factory_by_sectcode(request):
    try:
        sectcode:str = request.GET["sectcode"]
        landcode:str = request.GET["landcode"]
    except MultiValueDictKeyError:
        missing_params = [p for p in ("sectcode", "landcode") if p not in request.GET]
        missing_params = ", ".join(missing_params)
        return HttpResponse(
            f"Missing query parameter: {missing_params}.",
            status=400,
        )

    # landcode length should be 8
    if len(landcode) != 8 and not landcode.isnumeric():
        return HttpResponse(
            f"The landcode should be number and length is 8 (e.g. landcode 82-18 should be 00820018)",
            status=400
        )

    # 因為在資料庫裡面， landcode 有多種儲存格式 82-18, 00820018 所以需要將 landcode 轉成這兩種格式來搜尋
    landcode_1 = f"{int(landcode[:4])}-{int(landcode[4:])}"
    try:
        factory = OhshownEvent.objects.filter(Q(sectcode=sectcode), Q(landcode=landcode) | Q(landcode=landcode_1)).get()
        serializer = FactorySerializer(factory)
        return JsonResponse(serializer.data, safe=False)
    except FactoryDoesNotExist as e:
        return HttpResponse(
            f"Does not exist",
            status=404
        )

