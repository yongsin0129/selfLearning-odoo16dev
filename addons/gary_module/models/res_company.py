# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Company(models.Model):
    _inherit = 'res.company'

    budget = fields.Monetary(string="Budget")