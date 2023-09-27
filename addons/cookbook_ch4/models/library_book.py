from odoo import api, fields, models


class LibraryBook(models.Model):
    # 1 定义模型表示及排序
    _name = "library.book"
    _description = "Library Book"
    _order = "date_release desc, name"
    _rec_name = "short_name"

    name = fields.Char("Title", required=True)
    author_ids = fields.Many2many("res.partner", string="Authors")
    state = fields.Selection(
        [("draft", "Not Available"), ("available", "Available"), ("lost", "Lost")],
        "State",
    )
    pages = fields.Integer("Number of Pages")
    notes = fields.Text("Internal Notes")

    # 2 向模型添加数据字段
    short_name = fields.Char("Short Title", required=True)
    date_release = fields.Date("Release Date")
    date_updated = fields.Datetime("Last Updated")
    cover = fields.Binary("Book Cover")
    reader_rating = fields.Float(
        "Reader Average Rating",
        digits=(14, 4),  # Optional precision (total, decimals),
    )

    description = fields.Html("Description")

    # 3 使用可配置精度的浮点字段
    cost_price = fields.Float("Book Cost", digits="Book Price")

    out_of_print = fields.Boolean("Out of Print?")

    """本方法用于自定义记录的显示名称"""

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result
