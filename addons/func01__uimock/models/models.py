# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class func01__uimock(models.Model):
#     _name = 'func01__uimock.func01__uimock'
#     _description = 'func01__uimock.func01__uimock'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
