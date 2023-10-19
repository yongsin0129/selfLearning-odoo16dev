# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models
from odoo.exceptions import ValidationError


class twturbiks_first_demo(models.Model):
    _name = "twturbiks_first_demo.twturbiks_first_demo"
    _description = "twturbiks_first_demo.twturbiks_first_demo"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # 集成消息模型 增加消息记录通知功能

    name = fields.Char()
    value = fields.Integer(string="數字")
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    # track_visibility='always' 和 track_visibility='onchange'
    # odoo14 之後可以直接簡寫成 tracking="true"
    is_done_track_onchange = fields.Boolean("Is Done?", default=False, tracking=True)
    name_track_always = fields.Char("track_name", tracking=True)

    # default, 設定為當天的時間,當建立一筆資料時, 會顯示當下的時間,
    start_datetime = fields.Datetime("Start DateTime", default=fields.Datetime.now())
    stop_datetime = fields.Datetime("End Datetime")

    # field_onchange_demo_set field 中的 readonly=True,你可以發現是無法修改的 (可能是根據其他欄位透過 code 改變它的值)
    field_onchange_demo = fields.Char("onchange_demo")
    field_onchange_demo_set = fields.Char("onchange_demo_set", readonly=True)

    # float digits
    # field tutorial , input_number Float field 中的 digits 為設定進位以及小數點, 像這邊是算到小數點第3位並使用10進位
    input_number = fields.Float(string="input number", digits=(10, 3))

    # compute (str) – name of a method that computes the field
    # inverse (str) – name of a method that inverses the field (optional)
    # search (str) – name of a method that implement search on the field (optional)
    # computed_field 1. 預設是 readonly, 2.不存在 db中 (store=False), 3.搜尋 field_compute_demo 時, 會發現錯誤,
    # 透過 search 定義後就可以搜尋到
    # 透過 invers 定義後就可以對它做修改，任意改 input_number 或 field_compute_demo 都可以互相 trigger.
    field_compute_demo = fields.Integer(
        compute="_get_field_compute",
        inverse="_set_input_number",
        search="_search_upper",
    )

    # 使用 sql 限制 name 必需為唯一值
    _sql_constraints = [
        ("name_uniq", "unique(name)", "name must be unique"),
    ]

    # ORM API 功能 : depends , constrains
    # https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/backend/orm.html?highlight=api%20depend#module-odoo.api

    # 使用 api 的功能來讓欄位有相依性
    @api.depends("value")
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

    @api.depends("input_number")
    def _get_field_compute(self):
        for data in self:
            data.field_compute_demo = data.input_number * 1000

    # 不掛 decorator 也可以 : invers 定義後就可以對它做修改，任意改 input_number 或 field_compute_demo 都可以互相 trigger.
    def _set_input_number(self):
        for data in self:
            data.input_number = data.field_compute_demo / 1000

    # 不掛 decorator 也可以 : 過 search 定義後就可以使用搜尋功能
    def _search_upper(self, operator, value):
        return [("input_number", operator, value)]

    # 使用 api 的功能來限制欄位輸入值 , 並拋出 error message
    @api.constrains("start_datetime", "stop_datetime")
    def _check_date(self):
        for data in self:
            if data.start_datetime > data.stop_datetime:
                raise ValidationError("data.stop_datetime  > data.start_datetime")

    # 比較 onchange , depends 的差異
    # 補充說明 :  onchange 也可以 return 一個 dict. ，細節可看 twturbiks 筆記 , keyword = "result = dict()"
    # "set {}".format(self.field_onchange_demo) e.g : 輸入 "hello" => "set hello"
    @api.onchange("field_onchange_demo")
    def onchange_demo(self):
        if self.field_onchange_demo:
            self.field_onchange_demo_set = "set {}".format(self.field_onchange_demo)

    # 測試 report 的 template (q-web) 呼叫自定義 field 功能用的 def
    def print_hello(self):
        return "hello"


# ==============================================================================

# onchange , depends 差異補充說明

# 主要區分兩個比較容易的方法, 就是 @api.depends 可以使用在 related 欄位,
# 像是之後會介紹的 Many2one Many2many One2many 之類的.
# 而 @api.onchange 只能使用在同一個 model 上.
