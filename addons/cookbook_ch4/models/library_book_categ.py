from odoo import api, fields, models
from odoo.exceptions import ValidationError


# 6 向模型添加等级
class BookCategory(models.Model):
    _name = "library.book.category"
    _description = "Library Book Category"
    name = fields.Char("Category")

    ### 特别的等级支持
    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'
    parent_path = fields.Char(index=True)

    parent_id = fields.Many2one(
        "library.book.category",
        string="Parent Category",
        ondelete="restrict",
        index=True,
    )
    child_ids = fields.One2many(
        "library.book.category", "parent_id", string="Child Categories"
    )

    # 模型中添加如下行来新增一个防止循环关联的检查
    @api.constrains("parent_id")
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                "Error! You cannot create recursive categories."
            )
