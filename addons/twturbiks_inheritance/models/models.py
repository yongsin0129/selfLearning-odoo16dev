# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassInheritance(models.Model):
    _name = "hr.expense"  # 可寫可不寫，若 _name 跟 _inherit 不同時，則為 prototype inheritance
    _inherit = ["hr.expense"]

    test_field = fields.Char("test_field")


class PrototypeInheritance(models.Model):
    _name = "demo.prototype"
    _description = "PrototypeInheritance"
    _inherit = ["mail.thread"]

    # 'demo.prototype' 擁有 'mail.thread'(父類別) 的所有特性,
    #  mail.thread 提供 message_follower_ids ,message_ids 等 fields 可使用
    # 在這裡面的修改, 都不會去影響到 'mail.thread'(父類別).

    test_field = fields.Char("test_field")
