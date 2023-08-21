## 架構說明

ODOO 是一個以 MVC(Model、View、Controller)架構為主體的服務

```
Addons
├─ __init__.py
├─ __manifest__.py
├─ controllers
│  ├─ __init__.py
│  └─ controllers.py
├─ data
├─ demo
├─ i18n
├─ models
│  ├─ __init__.py
│  └─ models.py
├─ security
├─ static
└─ views
   └─ views.xml
```

- **manifest ** : 敘述你這個 addons 的詳細資訊與相關設定
- Model : ODOO 的 model 即是用自己一套 ORM 去操作 postgreSQL
- View : 用來定義在 ODOO 上的使用者介面，全都採用 XML 定義，而許多元件與畫面 ODOO 都有 templete 可以引用，如果需要加上或修改屬性可以透過 Xpath 去尋找原本 Model 的參數位置進行修改，唯一要注意的是當寫好一份 xml 要記得加進**manifest**內，否則 ODOO 搜尋不到
- Controllers : 透過繼承 Controller 建立，並以@route()裝飾器指定路徑，以 URL 路徑來控制請求，基本上常用到的就是跳轉頁面以及開發 API
- Reports : 存放關於報表的模型與報表的畫面
- static : 保存靜態資源，如 css、js、image...等等
- Security : 放置權限設定，保存不同 group 內對模型的 CURD 權限
- data : 初始化資料儲存處
- demo : 初始化資料儲存處
- i18n : 存放翻譯文件檔案。 ( PO 檔)

## Model 說明

[官網手冊 - ORM](https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html)

在 **init**.py 內引入 res_student.py

```
from . import res_student
```

在 models 底下建立一個 res_student.py

```python
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class ResStudent(models.Model):
    _name = 'res.student'
    _inherit = 'res.partner'
    _description = 'Student'

    nickname = fields.Char(string='綽號')
    math_score = fields.Float(string='數學成績')
    chinese_score = fields.Float(string='國文成績')
    avg_score = fields.Float(string='學期平均', compute='_compute_score')
    birthday = fields.Date(string='生日', required=True)
    school_id = fields.Many2one('res.company', string='所屬學校')
    school_city = fields.Char(string='所在城市', related='school_id.city')
    senior_id = fields.Many2one('res.student', string='直屬學長姐')
    junior_ids = fields.One2many('res.student', 'senior_id', string='直屬學弟妹')
    teacher_ids = fields.Many2many('res.partner', string='指導老師', domain=[('is_company', '!=', True)])
    gender = fields.Selection([("male", "男"), ("female", "女"), ("other", "其他")], string='性別')
    is_leadership = fields.Boolean(default=False)
    is_active = fields.Boolean(default=True)
    channel_ids = fields.Many2many('mail.channel', 'mail_channel_profile_partner', 'partner_id', 'channel_id', copy=False)

    @api.depends('math_score', 'chinese_score')
    def _compute_score(self):
        for record in self:
            record.avg_score = (record.math_score + record.chinese_score) / 2

    @api.onchange('school_id')
    def _onchange_shcool(self):
        for record in self:
            record.school_city = record.school_id.city

    @api.constrains('math_score', 'chinese_score')
    def _validate_score(self):
        for record in self:
            if record.math_score < 0 or record.chinese_score < 0:
                raise ValidationError(_("分數必須大於零"))

    @api.model
    def create(self, values):
        if values.get('is_active') is False:
            values.update({
                'is_leadership': False
            })
        return super(ResStudent, self).create(values)
```

用 pg4 or Dbeaver 就可以看到 database 中已經創建一個 res.student table 了

## view 說明

[官網手冊-view](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html)

- 修改 views.xml 就可以在主選單看到 "學生模組" ，並且點擊後有跳轉的動作
- 跳轉後的 tree view 可以用 <record model="ir.ui.view"></record> 來控制
- 點擊新增後需要顯示 form view ，<form><group></group></form>    P.S. 不加 <group> 會無法顯示 column title
- id="my_module.menu_1" 這邊的 my_module 要改成自已 module 的名字

```python
<odoo>
  <data>
    <!-- explicit list view definition -->

    <record id="view_res_student_list" model="ir.ui.view">
      <field name="name">res.student.list</field>
      <field name="model">res.student</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
          <field name="nickname" />
          <field name="birthday" />
          <field name="avg_score" />
          <field name="gender" />
          <field name="senior_id" />
          <field name="school_id" />
          <field name="is_leadership" />
          <field name="is_active" />
        </tree>
      </field>
    </record>

    <record id="view_res_student_form" model="ir.ui.view">
      <field name="name">res.student.form</field>
      <field name="model">res.student</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="name" />
              <field name="nickname" />
              <field name="birthday" />
              <field name="math_score" />
              <field name="chinese_score" />
              <field name="avg_score" />
              <field name="gender" />
              <field name="school_id" />
              <field name="is_leadership" />
              <field name="is_active" />
              <field name="senior_id" />
              <field name="junior_ids" />
              <field name="teacher_ids" widget="many2many_tags" />
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <!-- actions opening views on models -->

    <record model="ir.actions.act_window" id="student_action">
      <field name="name">Student</field>
      <field name="res_model">res.student</field>
      <field name="view_mode">tree,form</field>
    </record>


    <!-- server action to the one above -->
    <!--
    <record model="ir.actions.server" id="my_module.action_server">
      <field name="name">my_module server</field>
      <field name="model_id" ref="model_my_module_my_module"/>
      <field name="state">code</field>
      <field name="code">
        action = {
          "type": "ir.actions.act_window",
          "view_mode": "tree,form",
          "res_model": model._name,
        }
      </field>
    </record>
-->

    <!-- Top menu item -->
    <!-- action="student_action" 可加可不加，app 預設連結到上面的 action : model="ir.actions.act_window"-->
    <menuitem name="學生模組" id="menu_student_view" />

    <!-- menu categories -->

    <menuitem name="Menu 1" id="my_module.menu_1" parent="menu_student_view" />
    <menuitem name="Menu 2" id="my_module.menu_2" parent="menu_student_view" />

    <!-- actions -->

    <menuitem name="List" id="my_module.menu_1_list" parent="my_module.menu_1"
      action="student_action" />
    <!-- <menuitem name="Server to list" id="my_module" parent="my_module.menu_2"
    action="my_module.action_server"/> -->

  </data>
</odoo>
```

## security

- 記得權限要去 __manifest__ 檔案中打開，才能讓 view 讀取 model

## 參考資料
[Let's ODOO 開發與應用 30 天挑戰系列 By Gary](https://ithelp.ithome.com.tw/users/20130896/ironman/3979)