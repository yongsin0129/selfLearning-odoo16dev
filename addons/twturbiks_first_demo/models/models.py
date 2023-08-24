# -*- coding: utf-8 -*-

from odoo import models, fields, api


class twturbiks_first_demo(models.Model):
    _name = 'twturbiks_first_demo.twturbiks_first_demo'
    _description = 'twturbiks_first_demo.twturbiks_first_demo'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
