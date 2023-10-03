from odoo import api, fields, models


# 12 使用继承拷贝模型定义
class LibraryBookCopy(models.Model):
    _name = "library.book.copy"
    _inherit = "library.book"
    _description = "Library Book's Copy"
