# 開發 addons 筆記 By-Gary

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
- 點擊新增後需要顯示 form view ，<form><group></group></form> P.S. 不加 <group> 會無法顯示 column title
- id="my_module.menu_1" 這邊的 my_module 要改成自已 module 的名字

```xml
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

## Search View

```xml
    <!-- search view -->

    <record id="view_res_student_search" model="ir.ui.view">
      <field name="name">res.student.search</field>
      <field name="model">res.student</field>
      <field name="arch" type="xml">
        <search string="Student Search">
          <!-- <field> 對應搜尋邏輯，此處我們將name與nickname兩個作為搜尋field -->
          <field name="name" filter_domain="[('name', 'like', self)]" />

          <field name="nickname" filter_domain="[('nickname', 'like', self)]" />

          <!-- <filter>對應過濾邏輯，我們將is_active欄位作為過濾欄位，domain內是過濾邏輯，string則是顯示的字串 -->
          <filter name='is_active' string="IsActive" domain="[('is_active', '=', True)]" />

            <!-- <group>對應分類邏輯，我們將性別作為分類依據 -->
          <group string="Group By">
            <filter name='gender' string='Gender' context="{'group_by':'gender'}" />
          </group>
        </search>
      </field>
    </record>
```

## security

- 記得權限要去 **manifest** 檔案中打開，才能讓 view 讀取 model

| id                 | name        | model_id:id       | group_id:id     | perm_read | perm_write | perm_create | perm_unlink |
| ------------------ | ----------- | ----------------- | --------------- | --------- | ---------- | ----------- | ----------- |
| access_res_student | res.student | model_res_student | base.group_user | 1         | 1          | 1           | 1           |

- id : 權限 id，不重複即可

- name : 權限名稱

- model*id:id :規則為 "model*" + Model name，意指對哪個 model 設定權限

- group_id:id : 對哪個 group 設定權限，為設定的 XML ID，現在是設定給所有人都能讀取，此 group 在 base/security/base_group 內。

- 權限設定 1 代表給予權限，反之 0 代表無法操作此命令

- perm_read ：讀取 model 的權限

- perm_create ：增加 model 資料的權限

- perm_write：更改 model 資料的權限

- perm_unlink：刪除 model 資料的權限

設定完之後我們可以在 ODOO 的 Access right 內找到，我們的設定檔，記得開啟開發者模式。

開發者模式 > 設定 > 技術 > 安全 - 存取權

### security groups

目標 : 設定主任、老師、志工三個群組

在 security 底下增加 res_student_group.xml，記得**mainfest**內要填入 path

```xml title="security/res_student_group.xml"
<odoo>
    <data>
        <record model="ir.module.category" id="module_category_education">
            <field name="name">Education</field>
            <field name="description">About education</field>
        </record>

        <record model="res.groups" id="group_school_teacher">
            <field name="name">Teacher</field>
            <field name="category_id" ref="module_category_education"/>
        </record>

        <record model="res.groups" id="group_school_director">
            <field name="name">Director</field>
            <field name="category_id" ref="module_category_education"/>
        </record>

        <record model="res.groups" id="group_school_volunteer">
            <field name="name">Volunteer</field>
            <field name="category_id" ref="module_category_education"/>
        </record>

    </data>
</odoo>

```

- category 的 model 為 ir.module.category 
- id 不重複即可
- 定義group，model固定為 res.groups
- category_id : 設定的category record

記得**mainfest**內要填入 path

重新啟動後，在 Settings/Users & Companies/Groups 內便能看到三個 group

重寫 ir.model.access.csv

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

access_res_student_director,access_res_student,res.student,model_res_student,group_school_director,1,1,1,1,

access_res_student_teacher,access_res_student_teacher,model_res_student,group_school_teacher,1,1,1,0

access_res_student_volunteer,access_res_student_volunteer,model_res_student,group_school_volunteer,1,0,0,0
```

- 這邊的 group_id:id 綁定 security/res_student_group.xml 的 record id
- 現在三個 group 已經生效，可以根據不同的角色給於不同 group 的權限

## 參考資料

[Let's ODOO 開發與應用 30 天挑戰系列 By Gary](https://ithelp.ithome.com.tw/users/20130896/ironman/3979)
