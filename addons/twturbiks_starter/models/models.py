# -*- coding: utf-8 -*-

from odoo import api, fields, models


class twturbiks_starter(models.Model):
    _name = "twturbiks_starter.twturbiks_starter"
    _description = "twturbiks_starter.twturbiks_starter"

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    """
    tutorial 1 Many2one

    default=lambda self: self.env.user
    這行會在 obj 建立的時候，預設是現在的 user 身份
    """

    user_id = fields.Many2one("res.users", default=lambda self: self.env.user)

    """
    tutorial 2 Many2one

    做關連之前需要先確認 table 是否存在
    manifest 的 depends 中要加入 hr_contract 
    """

    employee_id = fields.Many2one("hr.employee", string="Employee")

    """
    tutorial 3 Many2Many

    1. 建立 Many2many 之前, 一定要先定義一個 model !! (本例子使用 DemoTag )
    2. security/ir.model.access.csv 記得要設定

    https://www.odoo.com/documentation/master/developer/reference/backend/orm.html#odoo.fields.Many2many
    參數說明 : 
    Parameters
    comodel_name : 就是這個欄位的 model 是跟那一個 model 做 Many2many 的關係


    relation (str) : <可選> 因為 Many2many 會在 db 建立一個表，我們可以自定義它的名字

    column1 (str) : <可選> 自定義第二欄位 relation table 中 column 1 的名字

    column2 (str) : <可選> 自定義第二欄位 relation table 中 column 2 的名字
    """

    tag_ids = fields.Many2many("demo.tag", "", "", "", string="Tags")

    """
    tutorial 4 Many2Many
    
    使用 Selection 對應上方的 employee_id

    1. fields.Selection 下拉選單 :
    e.g. gender = fields.Selection(string="Gender", selection=[("a", "A"), ("b", "B")])

    2. 特別的是 related : employee_id 從上面的 Mayn2one 對應到  "hr.employee" , 所以會去找裡面的 gender field
    note : hr.employee 的 gender 欄位，屬性就是 Selection , 所以用 char 會報格式不對的 error

    """

    gender = fields.Selection(string="Gender", related="employee_id.gender")

    """
    tutorial 5 One2Many

    為了下方的 model "demo.sheet" , 一定要建立一個 Many2one

    """

    sheet_id = fields.Many2one("demo.sheet", string="sheet id")

    """

    API
    """

    @api.depends("value")
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


"""
Many2Many2 使用到的 model
"""


class DemoTag(models.Model):
    _name = "demo.tag"
    _description = "Demo Tags"

    name = fields.Char(string="Tag Name", index=True, required=True)
    active = fields.Boolean(default=True, help="Set active.")


"""
One2Many 使用到的 model

一個 sheet 會對應到很多個 twturbiks_starter.twturbiks_starter 的資料

概念 : 很多張出差單，都屬於同一張 sheet 來展示

新開一個 model 就記得要設定 security

"""


class DemoExpenseSheetTutorial(models.Model):
    _name = "demo.sheet"
    _description = "Demo Sheet Tutorial"

    name = fields.Char("Expense Demo Report Summary", required=True)

    # 也就是說如果你要建立 One2many, 一定也要有一個 Many2one,
    # 但如果建立 Many2one 則不一定要建立 One2many.
    # One2many 是一個虛擬的欄位, 你在資料庫中是看不到它的存在

    expense_line_ids = fields.One2many(
        "twturbiks_starter.twturbiks_starter",  # 代表關連的 model (必填)
        "sheet_id",  # 代表所關連 model 的 field (必填)
        string="Expense Lines",
    )
