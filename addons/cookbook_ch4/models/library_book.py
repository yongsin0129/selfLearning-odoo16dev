from datetime import timedelta

from odoo import api, fields, models

# 14 使用抽象模型实现可复用模型功能
"""
必須放最上放，下面需要繼承的 class，才能成功執行 
"""


class BaseArchive(models.AbstractModel):
    _name = "base.archive"
    _description = "AbstractModel"
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):
    # 1 定义模型表示及排序
    _name = "library.book"
    _inherit = ["base.archive"]  # 14
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

    ###本方法用于自定义记录的显示名称
    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result

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
    ##### 同一頁面雙貨幣
    currency_id1 = fields.Many2one("res.currency", string="Currency1")
    currency_id2 = fields.Many2one("res.currency", string="Currency2")
    retail_price1 = fields.Monetary("Retail Price1", currency_field="currency_id1")
    retail_price2 = fields.Monetary("Retail Price2", currency_field="currency_id2")

    # 5 向模型添加关联字段

    ### 出版社
    publisher_id = fields.Many2one(
        "res.partner",
        string="Publisher",
        # optional:
        ondelete="set null",
        context={},
        domain=[],
    )

    # 6 向模型添加等级
    ### 向图书分配一个分类
    category_id = fields.Many2one("library.book.category")

    # 7 向模型添加约束验证
    ### 数据库约束
    _sql_constraints = [
        ("name_uniq", "UNIQUE(name)", "Book title must be unique."),
        (
            "positive_page",
            "CHECK(pages = 0 OR pages>0)",
            "No. of pages must be positive",
        ),
    ]

    ### Python代码约束
    @api.constrains("date_release")
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError("Release date must be in the past")

    # 8 向模型添加计算字段
    age_days = fields.Float(
        string="Days Since Release",
        compute="_compute_age",
        inverse="_inverse_age",
        search="_search_age",
        store=False,  # optional
        compute_sudo=False,  # optional
    )

    ### 计算逻辑
    @api.depends("date_release")
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    ### 写入计算字段的逻辑
    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered("date_release"):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    ### 进行搜索的逻辑
    ### 有定義才可以在 shell 中用這段 : self.env['library.book'].search([('age_days','>=',0)])
    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # 运算符转换：
        # age_days > value -> date < value_date
        operator_map = {
            ">": "<",
            ">=": "<=",
            "<": ">",
            "<=": ">=",
        }
        new_op = operator_map.get(operator, operator)
        return [("date_release", new_op, value_date)]

    # 9 暴露存储在其它模型中的关联字段
    publisher_city = fields.Char(
        "Publisher City", related="publisher_id.city", readonly=True
    )

    # 10 使用引用字段添加动态关联
    ref_doc_id = fields.Reference(
        selection="_referencable_models", string="Reference Document"
    )

    # 10 使用引用字段添加动态关联
    @api.model
    def _referencable_models(self):
        models = self.env["ir.model"].search([("field_id.name", "=", "message_ids")])
        return [(x.model, x.name) for x in models]


# 5 向模型添加关联字段 - 新增一個 class
class ResPartner(models.Model):
    _inherit = "res.partner"
    published_book_ids = fields.One2many(
        "library.book", "publisher_id", string="Published Books"
    )

    authored_book_ids = fields.Many2many(
        "library.book",
        string="Authored Books",
        # relation='library_book_res_partner_rel' # optional
    )

    # 11 使用继承向模型添加功能
    ### <!-- views 要新增欄位到 res.partner -->
    count_books = fields.Integer(
        "Number of Authored Books", compute="_compute_count_books"
    )

    @api.depends("authored_book_ids")
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


# 13 使用代理继承将功能拷贝至另一个模型
class LibraryMember(models.Model):
    _name = "library.member"
    _inherits = {"res.partner": "partner_id"}
    _description = "library.member"
    partner_id = fields.Many2one("res.partner", required=1, ondelete="cascade")

    date_start = fields.Date("Member Since")
    date_end = fields.Date("Termination Date")
    member_number = fields.Char()
    date_of_birth = fields.Date("Date of birth")


### 使用 delegate=True 取代 _inherits 的寫法
"""
class LibraryMember(models.Model):
    _name = 'library.member'
    partner_id = fields.Many2one('res.partner', ondelete='cascade', delegate=True)

    ...
"""
