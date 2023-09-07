# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassInheritance(models.Model):
    _name = "hr.expense"  # 可寫可不寫，若 _name 跟 _inherit 不同時，則為 prototype inheritance
    _inherit = ["hr.expense"]

    test_field = fields.Char("test_field")
