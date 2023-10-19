# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DemoHierarchyTutorial(models.Model):
    _name = "demo.hierarchy"
    _description = "Demo Hierarchy Tutorial"

    name = fields.Char(string="name", index=True)
    # Many2one : 這個 one 就是 parent Id , 本身類有很多個，都指向同一個 parent
    parent_id = fields.Many2one("demo.hierarchy", string="Related Partner", index=True)
    # 因為只會有一個，所以 related 指向就是 parent
    parent_name = fields.Char(
        related="parent_id.name", readonly=True, string="Parent name"
    )
    # one2many : 這個 one 就是自已
    # "demo.hierarchy", "parent_id"　： 到這個 model 中找 parent_id　等於自已本身 id 的所有物件。
    child_ids = fields.One2many(
        "demo.hierarchy", "parent_id", string="Contacts", domain=[("active", "=", True)]
    )
    active = fields.Boolean(default=True)


# python orm ：　說明 child_of 和 parent_of
# https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_hierarchy_tutorial#%E8%AA%AA%E6%98%8E-child_of-%E5%92%8C-parent_of
