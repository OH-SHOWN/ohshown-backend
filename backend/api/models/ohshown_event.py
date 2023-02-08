import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from .mixins import SoftDeleteMixin
from ..utils import translate_array_of_integer

CustomUser = get_user_model()


class OhshownEvent(SoftDeleteMixin):
    """Ohshown events that are observed potentially."""

    # List of fact_type & status
    ohshown_event_type_list = [
        ("2-1", "目擊黑熊"),
        ("2-2", "發現痕跡"),
        ("2-3", "其他"),
    ]
    cet_review_status_list = [
        ("A", "尚未審查"),
        ("O", "已審查-非遭遇事件"),
        ("P", "已審查-需補資訊"),
        ("Q", "已審查-待調查"),
        ("X", "已審查-已生成報告"),
    ]
    cet_report_status_list = [
        ("A", "未回報"),
        ("O", "第一次電子郵件回報待回覆"),
        ("P", "第一次電子郵件回報已播電話追蹤"),
        ("Q", "第一次回電子郵件"),
        ("X", "第二次發電子郵件待回覆"),
        ("Y", "第二次發電子郵件已播電話追蹤"),
        ("Z", "第二次回電子郵件"),
        ("B", "已結案"),
    ]
    source_list = [
        ("G", "政府"),
        ("U", "使用者"),
    ]

    # https://github.com/Disfactory/Disfactory/issues/527
    building_status_list = [
        ("A", "既有"),
        ("B", "新增"),
        ("C", "調查中"),
        ("D", "難以判定"),
    ]
    usage_status_list = [
        ("A", "目擊"),
        ("B", "活動痕跡"),
        ("C", "其他遭遇"),
        ("D", "難以判定"),
    ]
    highlight_category_list = [
        ("A", "新物種移入"),
        ("B", "已知物種"),
        ("C", "不明物種移入"),
    ]

    ground_type_list = [
      (0, "森林(天然林)"),
      (1, "森林(人工林)"),
      (2, "森林(次生林)"),
      (3, "溪流或河床"),
      (4, "住宅房舍附近"),
      (5, "遊憩區(包括山屋 / 營地週遭)"),
      (6, "道路(步道)"),
      (7, "道路(馬路)"),
      (8, "道路(林道)"),
      (9, "道路(產業道路)"),
      (10, "農牧用地(果園)"),
      (11, "農牧用地(菜園)"),
      (12, "農牧用地(休耕地)"),
      (13, "農牧用地(養蜂場)"),
      (14, "農牧用地(禽舍)"),
      (15, "農牧用地(豬舍)"),
      (16, "農牧用地(工寮或倉庫)"),
      (17, "其他"),
    ];
    vegetation_list = [
      (0, "闊葉林"),
      (1, "針葉林"),
      (2, "混合林"),
      (3, "灌叢"),
      (4, "草原"),
      (5, "竹林/箭竹林"),
      (6, "裸露地"),
      (7, "其他"),
    ];
    bear_attractor_list = [
      (0, "無"),
      (1, "自然食物資源"),
      (2, "動物屍體"),
      (3, "農作物"),
      (4, "家禽/畜"),
      (5, "蜂蜜"),
      (6, "垃圾/廚餘"),
      (7, "動物飼料"),
      (8, "人類食物"),
      (9, "其他"),
    ];

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
    landcode = models.CharField(max_length=50, blank=True, null=True)
    towncode = models.CharField(max_length=50, blank=True, null=True)
    townname = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    sectcode = models.CharField(max_length=50, blank=True, null=True)
    sectname = models.CharField(max_length=50, blank=True, null=True)

    name = models.CharField(max_length=50, blank=True, null=True)
    ohshown_event_type = models.CharField(
        max_length=3,
        choices=ohshown_event_type_list,
        blank=True,
        null=True,
    )
    ground_type = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=ground_type_list, 
            help_text='土地類型'
        ),
        blank=True, 
        null=True, 
    )
    vegetation = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=vegetation_list, 
            help_text='植被'
        ),
        blank=True, 
        null=True, 
    )
    bear_attractor = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=bear_attractor_list, 
            help_text='附近可能吸引熊接近的物品'
        ),
        blank=True, 
        null=True, 
    )

    before_release = models.BooleanField(
        default=False
    )  # 從 full-info.csv 匯入的那些都是 True ，使用者新增的通通是 False
    source = models.CharField(
        max_length=1,
        choices=source_list,
        default="U",
    )
    cet_review_status = models.CharField(
        max_length=1,
        choices=cet_review_status_list,
        default="A",
    )  # 地球公民基金會的審閱狀態（舉報前）
    cet_report_status = models.CharField(
        max_length=1,
        choices=cet_report_status_list,
        default="A",
    )  # 地球公民基金會的舉報狀態
    building_status = models.CharField(
        max_length=1,
        choices=building_status_list,
        blank=True,
        null=True,
    )  # 廠房
    usage_status = models.CharField(
        max_length=1,
        choices=usage_status_list,
        blank=True,
        null=True,
    )  # 使用狀況
    highlight_category = models.CharField(
        max_length=1,
        choices=highlight_category_list,
        blank=True,
        null=True,
    )  # 需注意類別

    cet_reviewer = models.ForeignKey(
        to=CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )  # 審查人

    sight_see_date_time = models.DateTimeField()
    status_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def translated_ground_type(self):
        return translate_array_of_integer(dict(self.ground_type_list), self.ground_type)
    def translated_vegetation(self):
        return translate_array_of_integer(dict(self.vegetation_list), self.vegetation)
    def translated_bear_attractor(self):
        return translate_array_of_integer(dict(self.bear_attractor_list), self.bear_attractor)

    class Meta:
        verbose_name = "Ohshown Event"
        verbose_name_plural = "Ohshown Events"


class RecycledOhshownEvent(OhshownEvent):
    class Meta:
        proxy = True

    objects = OhshownEvent.recycle_objects
