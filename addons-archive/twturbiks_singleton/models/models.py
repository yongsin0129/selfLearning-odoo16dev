# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DemoActionsSingleton(models.Model):
    _name = "demo.actions.singleton"
    _description = "Demo Actions Singleton"

    name = fields.Char("Description", required=True)

    def action_demo(self):
        # 這邊的 self 會是選中的 record , 如果選中的 records 數量不為 0 或 1 則會報錯。
        self.ensure_one()
        _logger.warning("=== CALL action_demo ===")
