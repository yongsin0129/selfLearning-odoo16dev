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
- 定義 group，model 固定為 res.groups
- category_id : 設定的 category record

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

### Security Record rules

如果說 Access right 是針對 model 的 CURD，那麼 Record rules 就是針對每筆資料去設定權限，例如我們不想讓志工層級的人看到休學學生的資料，即使他擁有讀的權限，透過 domain，我們便可以設定規則。

```xml
<record model="ir.rule" id="volunteer_rule">
    <field name="name">Volunteer Rule</field>
    <field name="model_id" ref="model_res_student"/>
    <field name="domain_force">[('is_active', '=', True)]</field>
    <field name="groups" eval="[(4, ref('group_school_volunteer'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_create" eval="False"/>
    <field name="perm_write" eval="False"/>
    <field name="perm_unlink" eval="False"/>
</record>
```

- model：固定是 ir.rule

- id：規則 id，不重複即可

- name：規則名稱，自定義即可

- model*id：關聯之 model，同之前設定 access right，規則為 "model*"+ Model Name

- domain_force：對 model 內資料的過濾條件，我們只希望還在學的學生出現在志工觀看名單上，另外可以用'|'或"&"去過濾複數條件

- groups：此規則套用的 group，這裡填入我們昨天設定的志工 group id

- perm_read：讀取資料權限

- perm_create：建立資料權限

- perm_write：修改資料權限

- perm_unlink：刪除資料權限

P.S. 注意 CURD 權限必須至少有一個是 True，不能以全否定的方式設定權限

重啟，我們便會看到新增的 Record rules
開發者模式 > 設定 > 技術 > 安全 - 記錄規則

## Menu

完成 Model、View、Controller(非必須)、Security 設定後，接下來我們要做的是讓主選單有我們的模組和連結到裡面。

增加一個 views/menu.xml

```xml
<odoo>
  <!-- actions opening views on models -->

  <record model="ir.actions.act_window" id="student_action">
    <field name="name">Student</field>
    <field name="res_model">res.student</field>
    <field name="view_mode">tree,form,kanban</field>
  </record>

  <!-- Top menu item -->
  <!-- action="student_action" 可加可不加，app 預設連結到上面的 action : model="ir.actions.act_window"-->
  <menuitem name="學生模組" id="menu_student_view" />

  <!-- menu categories -->

  <menuitem name="Menu 1" id="gary_module.menu_1" parent="menu_student_view" />
  <menuitem name="Menu 2" id="gary_module.menu_2" parent="menu_student_view" />

  <!-- actions -->

  <menuitem name="List" id="gary_module.menu_1_list" parent="gary_module.menu_1"
    action="student_action" />
  <!-- <menuitem name="Server to list" id="gary_module" parent="gary_module.menu_2"
    action="gary_module.action_server"/> -->
</odoo>
```
### Action
- act_window為odoo中action之一，此動作顧名思義就是單純開一個視窗，我們只要設定好相關屬性，便會依照設定執行

- model：固定為ir.actions.act_window

- id ：自定義，不重複即可

- name ：跳轉頁面名稱

- res_model：對應model

- view_mode：所需要的view類型

### Menu
- `<menuitem>` ：主選單標籤

- id ：自定義的menu id，不重複即可

- name ：在選單顯示的名稱

- action ：對應上述action id，表示執行此action

如此一來我們便把Menu與windows action做連結，別忘了要將此路徑加到__manifest__.py中:
```py
'data': [
        'views/menu.xml',      
         ....
    ],
```

另外新增一個 kanban view

```xml
 <record id="view_res_student_kanban" model="ir.ui.view">
      <field name="name">res.student.kanban</field>
      <field name="model">res.student</field>
      <field name="arch" type="xml">
        <!-- 以卡片方式呈現，以標籤包覆，而內部template以qweb撰寫。 -->
        <kanban>
          <field name="name" />
          <templates>
            <t t-name="kanban-box">
              <div t-attf-class="oe_kanban_global_click">
                <div class="oe_kanban_details">
                  <strong class="o_kanban_record_title">
                    <span>大名:<field name="name" />
                    </span>
                    <br />
                    <span>綽號:<field name="nickname" />
                    </span>
                  </strong>
                </div>
              </div>
            </t>
          </templates>
        </kanban>
      </field>
    </record>
```

## Report

Odoo提供建立report的功能，透過wkhtmltopdf來輸出pdf

先增加檔案 /reports/res_student_report.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <template id="report_student_id_card">
    <t t-call="web.html_container">
      <t t-foreach="docs" t-as="o">
        <t t-call="web.external_layout">
          <div class="page">
            <h2>Student Report</h2>
            <div>
              <p>Name: <span t-field="o.name" /></p>
            </div>
            <div>
              <p>Nickname: <span t-field="o.nickname" /></p>
            </div>
            <div>
              <p>School: <span t-field="o.school_id.name" /></p>
            </div>
          </div>
        </t>
      </t>
    </t>
  </template>

  <record id="report_student" model="ir.actions.report">
    <!-- button 的名字 -->
    <field name="name">列印資料</field>
    <!-- 從什麼資料庫取得資料 -->
    <field name="model">res.student</field>
    <field name="report_type">qweb-pdf</field>
    <!-- report_name　的格式 : module name + 上面 template 的 ID -->
    <!-- 邏輯　：　report action 將資料丟入 templete 做 render -->
    <field name="report_name">gary_module.report_student_id_card</field> 
    <!-- 輸出的 pdf 檔名 -->
    <field name="print_report_name">'學生資訊 %s' % (object.name) +'.pdf'</field>
  </record>

</odoo>
```

### Template

- Odoo 的Template代表畫面，是用Qweb撰寫，將xml轉譯成html

- id：自定義，不重複即可，會跟　actions.report 做 binding

- t：以t開頭的為Qweb寫法，基本上一開始寫的是一樣的

- t-call="web.external_layout ：提供我們基本的header與footer <t t-foreach="docs" t-as="o"> ：代表遍歷整個records，像是python的 for o in records:

- t-as 是幫你的model的名稱

- t-field :配上之前設定的model object可以拿到底下的field

只要知道Qweb代表的意義，可以寫出基本的畫面，另外也有t-if 等邏輯判斷幫助report更加完善

### Report
report就是匯出檔案的設定

- id：自定義，不重複即可

- model="ir.actions.report" : report action 的寫法

- model：關聯的model name

- name：顯示的Action button name

- report_type ：輸出模式，預設為qweb-pdf ，另外還有qweb-html ，會以網頁的方式呈現

- name：串連template的設定，格式為 module.template_id

- print_report_name ：輸出 pdf 檔案名稱

設定好之後我們將reports加入__manifest__.py裡

```
'data': [
        'reports/student_report.xml'
		...
    ],
```
## 製作假資料 Data Files

>通常我們在寫module的時候，會需要一些初始資料或是固定需要的資料，我們可以定義資料在創立Model的時候一併創立資料，就不需要一項一項新增或匯入，我們來寫一個範例。 By gary

odoo 提供兩種方式匯入假資料

- xml
- csv

### xml

新增檔案 /data/res_student.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
          <record id="student_gary" model="res.student">
            <field name="name">GaryWu</field>
            <field name="nickname">Gary</field>
            <field name="birthday">1991-07-30</field>
            <field name="gender">male</field>
            <field name="is_active">True</field>
          </record>
        
          <record id="student_flynn" model="res.student">
            <field name="name">FlynnSun</field>
            <field name="nickname">Flynn</field>
            <field name="birthday">1991-06-19</field>
            <field name="gender">male</field>
            <field name="is_active">False</field>
          </record>
    </data>
</odoo>
```
- `<data noupdate='1'>` ： 設成1的時候，當我們在安裝module時便會自動把這些資料帶入，

- id ：自定義id，不重複即可

- model：關聯model，填入model name

- field ：填入model field name，並填入對應的值。

### csv

透過CSV增加，要注意的是檔名必須為model name.csv

data/res.student.csv

```csv
"id","name","nickname","gender","birthday","is_active"
student_peter,"Peter Chen","Peter","male","1999-09-09",True
student_westing,"Westing Ting","Westing","male","2000-01-01",False
```

依照慣例記得把檔案加入__manifest__.py中

```py
'data': [
        'data/res_student.xml'
        'data/res.student.csv'
		...
    ],
```

>同樣的寫法還有Demo Data，不過在寫Demo data要注意的是，必須把Demo data的選項打勾，這樣安裝的時候才會匯入並且__manifest__.py內要寫在demo裡而不是data裡。

## Paper Format - A4 B5 or other

>生成report時候想要自己自定義的紙張格式，如直橫向、上下左右間距...等等，Odoo可以透過設定paper format來達到需求

增加/data/student_paperformat.xml

```xml
<odoo>
    <data>
        <record id="paperformat_gary" model="report.paperformat">
            <field name="name">GARY PAPER</field>
            <field name="default" eval="True" />
            <field name="format">A4</field>
            <field name="page_height">0</field>
            <field name="page_width">0</field>
            <field name="orientation">Portrait</field>
            <field name="margin_top">50</field>
            <field name="margin_bottom">65</field>
            <field name="margin_left">7</field>
            <field name="margin_right">7</field>
            <field name="header_line" eval="False"/>
            <field name="header_spacing">45</field>
            <field name="dpi">90</field>
        </record>
    </data>
</odoo>
```
- id：自定義，不重複即可

- model：固定為 report.paperformat

- format：預定格式，預設為A4也可以填入A0 to A9, B0 to B10, Legal, Letter, Tabloid,…等等

- dpi：輸出解析度，預設為90

- orientation：Landscape或Portrait，代表直向或橫向

- margin_top ：與上方邊距

- margin_bottom ：與下方邊距

- margin_left ：與左邊距

- margin_right ：與右邊距

- page_height ：紙張長度

- page_width：紙張寬度

- header_line ：布林值，要不要顯示header line

- header_spacing ：與header距離

```py title="__manifest__"
'data': [
        'data/student_paperformat.xml'
		...
    ],
```

>重新啟動以後我們在 Setting → 技術 -> 報表 -> 紙張格式 內可以看到我們設定的名字，點選後並儲存

## controller

>對URL endpoint處理，以下用兩支API來做範例：

```py
import json

from odoo import _
from odoo.http import Controller, Response, request, route
from odoo.tools import date_utils

class StudtentController(Controller):
    
    @route('/student/all', methods=['GET'], type='http', auth='public', cors='*', csrf=False)
    def get_student_list(self):
        data = []
        students = request.env['res.student'].sudo().search([])
        for student in students:
            val = {
                'id': student.id,
                'name': student.name,
                'nickname': student.nickname,
                'gender': student.gender
            }
            data.append(val)
        result = {'data': data}
        body = json.dumps(result, default=date_utils.json_default)
        return Response(
            body, status=200,
            headers=[('Content-Type', 'application/json'), ('Content-Length', len(body))]
        )   

    @route('/student', methods=['POST'], type='json', auth='public', cors='*', csrf=False)
    def create_student(self):
        student_data = json.loads(request.httprequest.data)
        val = {
            'name': student_data.get('name'),
            'nickname': student_data.get('nickname'),
            'gender': student_data.get('gender'),
            'birthday': student_data.get('birthday')
        }

        student_obj = request.env['res.student'].sudo()
        student_obj.create(val)
        result = {'code': 200, 'message': 'Created Successfully'}
        body = json.dumps(result, default=date_utils.json_default)
        return Response(
            body, status=200,
            headers=[('Content-Type', 'application/json'), ('Content-Length', len(body))]
        )
```
### @route 裝飾器 (端點、參數)

- 第一個參數代表指定的endpoint，所以request url 就是 `http://<localhost:8069>/student/all`
- methods：代表requests method，這裡是陣列也可以寫入多個requests method，透過ODOO內的request.httprequest.method 分辨後再做想要做的事，以第一隻API為例我們只限定於GET method。
- type: 只有json和http兩種，差別在於content type是不是application/json，來限制使用者請求，若不符規定則會返回錯誤。
- auth: 有user、public、none三種，user限定需要使用者在登入狀態，常用在頁面引導，而這邊使用的API則是不需要經由登入認證故寫為public ，
- cors: 開通跨域的參數
- crsf: 預設為True ，也就是crsf token認證，這邊我們用API寫法時要改為False

### First API

>查詢學生資料，透過request.env['res.student'] ，尋找此model底下資料
>在search內沒有加上domain所以會找出所有資料
>另外我們可以控制return給使用者的參數，這裡只給id、名字、綽號、性別，性別是會給當初設定的Key值
>最後要注意的是，返回的值必須為JSON Object。

### Second API

- URL endpoint: `http://<localhost:8069>/student`
- request body
```json 
{
	"name": "黃小華",
	"nickname": "阿華",
	"gender": "male",
	"birthday": "2020-02-01"
}
```


## Logging

>於controllers/main.py 內匯入 logging，並增加log：

```py

# 初始化 logger
import logging
_logger = logging.getLogger(__name__)


class StudentController(Controller):

	@route('/student', methods=['POST'], type='json', auth='public', cors='*', csrf=False)
	    def create_student(self):

          # 印出自己想要的層級與字串
          # info、debug、error、warning、critical
	        _logger.info('---------> %s \n', request.httprequest.data)

          # 原本的 create_student 內容
	        student_data = json.loads(request.httprequest.data)
	        val = {
	            'name': student_data.get('name'),
	            'nickname': student_data.get('nickname'),
	            'gender': student_data.get('gender'),
	            'birthday': student_data.get('birthday')
	        }	
	
	        student_obj = request.env['res.student'].sudo()
	        student_obj.create(val)
	        result = {'code': 200, 'message': 'Created Successfully'}
	        body = json.dumps(result, default=date_utils.json_default)
	        return Response(
	            body, status=200,
	            headers=[('Content-Type', 'application/json'), ('Content-Length', len(body))]
	        )
```

>寫好以後別忘了在 odoo.conf 內設定路徑，否則只有在terminal才會看到

```
logfile = /var/log/odoo/odoo.log
...
```

>如此一來，當我們打API的時候便會顯示log，並會儲存於指定檔案位置:

## 參考資料

[Let's ODOO 開發與應用 30 天挑戰系列 By Gary](https://ithelp.ithome.com.tw/users/20130896/ironman/3979)
