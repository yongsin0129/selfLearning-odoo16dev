# -*- coding: utf-8 -*-

from odoo import api, fields, models


class twturbiks_first_demo(models.Model):
    _name = "twturbiks_first_demo.twturbiks_first_demo"
    _description = "twturbiks_first_demo.twturbiks_first_demo"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # 集成消息模型 增加消息记录通知功能

    name = fields.Char(tracking=True)
    value = fields.Integer(string="數字", tracking=True)
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    # track_visibility='always' 和 track_visibility='onchange'
    is_done_track_onchange = fields.Boolean(
        string="Is Done?", default=False, track_visibility="onchange"
    )
    name_track_always = fields.Char(string="track_name", track_visibility="always")

    @api.depends("value")
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
