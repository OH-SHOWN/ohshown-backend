import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

from .mixins import SoftDeleteMixin
from ..utils import format_multiple_choice_options

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

    ohshown_again_list = [
        (0, "是"),
        (1, "否"),
        (2, "沒意見"),
    ]

    prevent_ohshown_methods_list = [
        (0, "盡量結伴同行"),
        (1, "輕聲走路"),
        (2, "必要時，沿途製造些聲響，如吹口哨、講話"),
        (3, "避免走夜路"),
        (4, "妥善收存食物、垃圾與廚餘"),
        (5, "看到熊在遠方時，人要輕聲離開現場"),
        (6, "單獨行動"),
        (7, "隨身攜帶哨子或鈴鐺"),
        (8, "攜帶防熊噴霧"),
        (9, "其他"),
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
    ohshown_again = models.IntegerField(
        blank=True, 
        null=True, 
        choices=ohshown_again_list,  
        help_text='您是否希望以後有機會，或能再次看到野外的黑熊'
    )
    ohshown_again_reason = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text='您是否希望以後有機會，或能再次看到野外的黑熊-為什麼'
    )
    prevent_ohshown_methods = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=prevent_ohshown_methods_list, 
            help_text='您知道以下哪些做法有助於減少遇到熊的機會，或避免不愉快地與熊相遇充'
        ),
        blank=True, 
        null=True, 
    )
    prevent_ohshown_methods_text_object = JSONField(
        blank=True, 
        null=True, 
        help_text='您知道以下哪些做法有助於減少遇到熊的機會，或避免不愉快地與熊相遇充-文字補充'
    )
    survey_if_bear_exist = models.BooleanField(
        blank=True, 
        null=True, 
        help_text='您是否會先了解您預計前往的地點有無黑熊出沒'
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

    def formated_ground_type(self):
        return format_multiple_choice_options(dict(self.ground_type_list), self.ground_type)
    def formated_vegetation(self):
        return format_multiple_choice_options(dict(self.vegetation_list), self.vegetation)
    def formated_bear_attractor(self):
        return format_multiple_choice_options(dict(self.bear_attractor_list), self.bear_attractor)
    def formated_ohshown_again(self):
        return dict(self.ohshown_again_list).get(self.ohshown_again, "") + ("(%s)" % self.ohshown_again_reason if self.ohshown_again_reason else "")
    def formated_prevent_ohshown_methods(self):
        return format_multiple_choice_options(dict(self.prevent_ohshown_methods_list), self.prevent_ohshown_methods, self.prevent_ohshown_methods_text_object)

    class Meta:
        verbose_name = "Ohshown Event"
        verbose_name_plural = "Ohshown Events"


class RecycledOhshownEvent(OhshownEvent):
    class Meta:
        proxy = True

    objects = OhshownEvent.recycle_objects
