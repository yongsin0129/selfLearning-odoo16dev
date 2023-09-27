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
    out_of_print = fields.Boolean("Out of Print?")

    # 3 使用可配置精度的浮点字段
    cost_price = fields.Float("Book Cost", digits="Book Price")

    # 4 向模型添加货币字段
    currency_id = fields.Many2one("res.currency", string="Currency")
    retail_price = fields.Monetary(
        "Retail Price",
        # optional: currency_field='currency_id' (default),
    )
    # 同一頁面雙貨幣
    currency_id1 = fields.Many2one("res.currency", string="Currency1")
    currency_id2 = fields.Many2one("res.currency", string="Currency2")
    retail_price1 = fields.Monetary("Retail Price1", currency_field="currency_id1")
    retail_price2 = fields.Monetary("Retail Price2", currency_field="currency_id2")

    """本方法用于自定义记录的显示名称"""

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result
