# -*- coding: utf-8 -*-

from odoo import api, fields, models


class twturbiks_starter(models.Model):
    _name = "twturbiks_starter.twturbiks_starter"
    _description = "twturbiks_starter.twturbiks_starter"

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    """
    tutorial 1

    default=lambda self: self.env.user
    這行會在 obj 建立的時候，預設是現在的 user 身份
    """
    user_id = fields.Many2one("res.users", default=lambda self: self.env.user)

    """
    tutorial 2

    做關連之前需要先確認 table 是否存在
    manifest 的 depends 中要加入 hr_contract 
    """
    employee_id = fields.Many2one("hr.employee", string="Employee")

    @api.depends("value")
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
