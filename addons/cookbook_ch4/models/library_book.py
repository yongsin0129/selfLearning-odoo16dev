from odoo import api, fields, models


class LibraryBook(models.Model):
    # 1 模型
    _name = "library.book"
    _description = "Library Book"

    name = fields.Char("Name", required=True)
    date_release = fields.Date("Date_Release")
