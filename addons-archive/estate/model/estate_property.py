# 初始化 logger
import logging

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property"
    _description = "房屋信息数据"
    _order = "id desc"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)",
         "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)",
         "The offer price must be positive"),
    ]

    # ---------------------------------------- Default Methods ------------------------------------

    def default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(string="名称", required=True)
    description = fields.Text(string="描述")
    postcode = fields.Char(string="邮编")
    date_availability = fields.Date(
        string="到期时间", default=lambda self: self.default_date_availability(), copy=False)
    expected_price = fields.Float(string="期望价格", required=True)
    selling_price = fields.Float(string="销售价格", copy=False, readonly=True)
    bedrooms = fields.Integer(string="房间数量", default=2)
    living_area = fields.Integer(string="居住面积")
    facades = fields.Integer(string="朝向")
    garage = fields.Boolean(string="是否带车库")
    garden = fields.Boolean(string="是否带花园")
    garden_area = fields.Integer(string="花园面积")
    garden_orientation = fields.Selection(
        string="花园朝向", selection=[("N", "North"),
                                  ("S", "South"),
                                  ("E", "East"),
                                  ("W", "West"),])

    # Special
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
    active = fields.Boolean("Active", default=True)

    # Relational
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")

    # Computed
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )

    best_price = fields.Float(
        "Best Offer", compute="_compute_best_price", help="Best offer received")

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped(
                "price")) if prop.offer_ids else 0.0

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
            # onchanges方法可以返回一个非阻塞的警告信息 : 如下例子
            return {'warning': {
                    'title': _("Warning"),
                    'message': ('This option is not supported for Authorize.net')}}
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # ------------------------------------------ CRUD Methods -------------------------------------
    # 类继承自Model，Model提供了 create(), read(), write() and unlink()
    # Model api : Method decorators https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/backend/orm.html#module-odoo.api
    # Model ORM : Common ORM methods https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/backend/orm.html#common-orm-methods

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")

    @api.ondelete(at_uninstall=False)
    def foo(self):
        # info、debug、error、warning、critical
        _logger.critical('---- hello world----->  \n')

    # ---------------------------------------- Action Methods -------------------------------------

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})
