from datetime import datetime, timedelta

from odoo import fields, models


class EstateProperty(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property"
    _description = "房屋信息数据"
    _order = "id desc"

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(string="名称", required=True)
    description = fields.Text(string="描述")
    postcode = fields.Char(string="邮编")
    date_availability = fields.Date(
        string="到期时间", default=lambda self: fields.Datetime.now() + timedelta(days=90), copy=False)
    expected_price = fields.Float(string="期望价格", required=True)
    selling_price = fields.Float(string="销售价格", copy=False, readonly=True)
    bedrooms = fields.Integer(string="房间数量", default=2)
    living_area = fields.Text(string="居住面积")
    facades = fields.Integer(string="朝向")
    garage = fields.Boolean(string="是否带车库")
    garden = fields.Boolean(string="是否带花园")
    garden_area = fields.Integer(string="花园面积")
    garden_orientation = fields.Selection(
        string="花园朝向", selection=[("N", "North"),
                                  ("S", "South"),
                                  ("E", "East"),
                                  ("W", "West"),])
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="狀態",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=False)
