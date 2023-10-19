# -*- coding: utf-8 -*-

from odoo import models, fields, api


class su_sir_module(models.Model):
    _name = 'su_sir_module.su_sir_module'
    _description = 'su_sir_module.su_sir_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
