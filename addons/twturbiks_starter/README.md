## odoo 入門篇 - twturbiks

參考 : 沈弘哲大大的 [odoo 入門篇](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_expense_tutorial_v1)

## Many2one

### model
```python title="models/models.py"
class DemoMain(models.Model):
    _name = "twturbiks_starter.main"
    _description = "this is main model of this module "

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
```
### security
```csv title="security/ir.model.access.csv"
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_twturbiks_starter_main,twturbiks_starter main,model_twturbiks_starter_main,base.group_user,1,1,1,1
```
### view
```xml title="views/views.xml"
    <!-- main model list -->
    <record model="ir.ui.view" id="twturbiks_starter.list">
      <field name="name">twturbiks_starter list</field>
      <field name="model">twturbiks_starter.main</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
          <field name="value" />
          <field name="value2" />
          <field name="user_id" />
          <field name="employee_id" />
          <field name="tag_ids" widget="many2many_tags" />
          <field name="gender" />
          <field name="sheet_id" />
        </tree>
      </field>
    </record>

    <!-- main model form -->
    <record model="ir.ui.view" id="twturbiks_starter.form">
      <field name="name">twturbiks_starter form</field>
      <field name="model">twturbiks_starter.main</field>
      <field name="arch" type="xml">
        <form>
          <group>
            <field name="name" />
            <field name="value" />
            <field name="value2" />
            <field name="user_id" />
            <field name="employee_id" />
            <field name="tag_ids" widget="many2many_tags" /> <!-- widget -->
            <field name="gender" />
            <field name="sheet_id" />
          </group>
        </form>
      </field>
    </record>
```
### menu
```xml title="views/menu.xml"
  <!-- menu 慣例 : -->
  <!-- 1. 先寫 action , 定義 ID -->
  <!-- 2. 再寫 menu ， 套用上面的 ID-->

  <!-- APP menu region -->
  <!-- 主選單 : 不需要寫 action-->
  <menuitem name="twturbiks_starter" id="twturbiks_starter.menu_root" />

  <!--  -->
  <!-- menu 1     main model-->
  <!--  -->
  <!-- action for open main model -->
  <record model="ir.actions.act_window" id="twturbiks_starter.open_main">
    <field name="name">twturbiks_starter main model</field>
    <field name="res_model">twturbiks_starter.main</field>
    <field name="view_mode">tree,form,kanban</field>
  </record>

  <!-- 單層 Menu for open main model -->
  <menuitem name="Menu 1" id="twturbiks_starter.menu_1" action="twturbiks_starter.open_main"
    parent="twturbiks_starter.menu_root" sequence="1" />
```

## many2many

### model

```python title="models/models.py"
    """
    tutorial 3 Many2Many

    1. 建立 Many2many 之前, 一定要先定義一個 model !! (本例子使用 DemoTag )
    2. security/ir.model.access.csv 記得要設定

    https://www.odoo.com/documentation/master/developer/reference/backend/orm.html#odoo.fields.Many2many

    參數說明 : 
    comodel_name : 就是這個欄位的 model 是跟那一個 model 做 Many2many 的關係

    relation (str) : <可選> 因為 Many2many 會在 db 建立一個表，我們可以自定義它的名字

    column1 (str) : <可選> 自定義第二欄位 relation table 中 column 1 的名字

    column2 (str) : <可選> 自定義第二欄位 relation table 中 column 2 的名字
    """

    tag_ids = fields.Many2many("twturbiks_starter.tag", "", "", "", string="Tags")

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
    Many2Many 使用到的 model

    注意 : Many2Many 會在 DB 產生一個新的表來關連兩個 model
    """


class DemoTag(models.Model):
    _name = "twturbiks_starter.tag"
    _description = "Demo Tags"

    name = fields.Char(string="Tag Name", index=True, required=True)
    active = fields.Boolean(default=True, help="Set active.")
```

### security

```csv title="security/ir.model.access.csv"
access_twturbiks_starter_tag,twturbiks_starter Tag,model_twturbiks_starter_tag,base.group_user,1,1,1,1
```

### view

沒有寫單獨寫 tag 的 view , tag field 應用在 main model 之中

### menu 

沒有單獨 view , 就不需要用到 menu

## one2many

### model
```python title="models/models.py"
    """
    tutorial 5 One2Many

    為了下方的 model "demo.sheet" , 一定要建立一個 Many2one    

    """

    sheet_id = fields.Many2one("twturbiks_starter.sheet", string="sheet id")


"""
One2Many 使用到的 model

一個 sheet 會對應到很多個 twturbiks_starter.main 的資料

舉例 : 很多張出差單，都屬於同一張 sheet 來展示

本例 : 多個 main object ， 都屬於同一張 sheet

注意 : 新開一個 model 就記得要設定 security

注意 : One2Many 是一個虛擬欄位，在 twturbiks_starter.sheet table 中是看不到 main_object_ids 的欄位

補充: 程式先寫 Many2one，再寫 One2many 這樣才知道One2many 的 inverse_name 要寫誰。
"""


class DemoExpenseSheetTutorial(models.Model):
    _name = "twturbiks_starter.sheet"
    _description = "Demo Sheet Tutorial"

    name = fields.Char("Sheet Report", required=True)

    # 也就是說如果你要建立 One2many, 一定也要有一個 Many2one,
    # 但如果建立 Many2one 則不一定要建立 One2many.
    # One2many 是一個虛擬的欄位, 你在資料庫中是看不到 main_object_ids 的存在, 只能在 Many2One 看到 sheet_id

    main_object_ids = fields.One2many(
        "twturbiks_starter.main",  # 代表關連的 model (必填)
        "sheet_id",  # 代表所關連 model 的 field (必填)
        string="Main Object Lines",
    )

```

### security

```csv
access_twturbiks_starter_sheet,twturbiks_starter sheet,model_twturbiks_starter_sheet,base.group_user,1,1,1,1
```

### view

```xml title="views/views.xml"
    <!-- sheet model list -->
    <record model="ir.ui.view" id="demo_sheet_list">
      <field name="name">demo_sheet list</field>
      <field name="model">twturbiks_starter.sheet</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
        </tree>
      </field>
    </record>

    <!-- sheet model form -->
    <record id="view_form_demo_expense_sheet_tutorial" model="ir.ui.view">
      <field name="name">Demo Expense Sheet Tutorial Form</field>
      <field name="model">twturbiks_starter.sheet</field>
      <field name="arch" type="xml">
        <form string="main object Sheet Tutorial">
          <sheet>
            <group>
              <!-- sheet model 的第一個欄位 -->
              <field name="name" />
            </group>

            <!-- 這邊用 notebook tag -->
            <notebook>
              <!-- notebook tag 的顯示名字 -->
              <page string="main object page1">
                <!-- sheet model 的第二個欄位 -->
                <field name="main_object_ids">
                  <!-- tree 的 editable 也可以寫 bottom ，這樣新增的資料就會加到最下面 -->
                  <tree editable="top">
                    <field name="name" />
                    <field name="value" />
                    <field name="employee_id" />
                    <field name="tag_ids" widget="many2many_tags" />
                  </tree>
                </field>
              </page>
            </notebook>

          </sheet>
        </form>
      </field>
    </record>
```

### menu

```xml title="views/menu.xml"
  <!--  -->
  <!-- menu 2     sheet model-->
  <!--  -->
  <!-- action for open sheet model -->
  <record model="ir.actions.act_window" id="twturbiks_starter.open_sheet">
    <field name="name">twturbiks_starter sheet model</field>
    <field name="res_model">twturbiks_starter.sheet</field>
    <field name="view_mode">kanban,tree,form</field>
  </record>

  <!-- 多層 Menu for open sheet model-->
  <menuitem name="Menu 2" id="twturbiks_starter.menu_2" parent="twturbiks_starter.menu_root"
    sequence="2" />
  <menuitem name="open_sheet" id="twturbiks_starter.menu_2_open_sheet"
    parent="twturbiks_starter.menu_2"
    action="twturbiks_starter.open_sheet" />
```
## demo and data

### noupdate and forcecreate

noupdate="1" data 可以被更動，每次 update 不會將 data 還原成 底下的預設值

noupdate="0" data 不可以被更動，每次 update 都會將 data 還原成 底下的預設值

forcecreate="0" 每一個 record data 預設是不能被刪除，如果 update 的時候發現 data 被刪掉，就會直接加回來，如果不希望這個預設行為
則需要在 record tag 後面加上 forcecreate="0"

ref : https://www.odoo.com/zh_TW/forum/bang-zhu-1/data-noupdate-0-1-in-security-xml-13546

```xml title="demo/demo.xml"
<odoo>
  <data noupdate="1">

    ...

    <record id="object12" model="twturbiks_starter.main" forcecreate="0">
      <field name="name">Object 12</field>
      <field name="value">20</field>
    </record>

    ...

  </data>
</odoo>

```

## XML Button

使用 xml button 呼叫 model method ( ex : form view ...) 

### model method 定義 

[tutorial : odoo16 all actions list](https://www.cybrosys.com/blog/type-of-actions-in-odoo-16-erp)

在 main model 中新增一個方法 , 透過 main obj 可以查到自已所屬的 sheet

```python title="models/models.py"

    # 在 main obj 中，連結到歸屬的 sheet
    def show_sheet_of_thisObj(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "twturbiks_starter.sheet",
            "view_mode": "form",
            "res_id": self.sheet_id.id,
        }

```

在 sheet model 中新增一個方法 ，透過 sheet ID 找旗下所有的 objs

```python title="models/models.py"

    # 在 sheet 中，連結到歸屬於自已的 main objs
    def show_all_main_objs(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "twturbiks_starter.main",
            "view_mode": "tree,form",
            "view_id": False,
            "name": "all_main_objs",
            "domain": [("sheet_id", "=", self.id)],
        }

```

參數說明 : 

- type : 執行的 action
- view_mode : window 中可以顯示的 view 種類
- view_id : is an optional database ID or false
- domain :- It is used to filter the domain to implicitly add to all view search queries.
to open the form view of a specific product in a new dialog:

補充 : 文件中有一個參數 views :- It is the list of view_type and view_id pairs. 但使用上好像沒有 view_type 的作用

### view 

[official doc. odoo16-btn](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#list)

需要再往下拉一點才會看到 button tag 的說明

```xml title="views/views.xml"
    <!-- main model form -->
    <record model="ir.ui.view" id="twturbiks_starter.form">
      <field name="name">twturbiks_starter form</field>
      <field name="model">twturbiks_starter.main</field>
      <field name="arch" type="xml">

        <!-- button 會出現在 header 的位置 -->
        <!-- <xpath expr="//header" position="inside">
          <button
            class="btn btn-primary"
            name="open_form_view"
            string="SHEET ID" type="object"
            attrs="{'invisible':[('sheet_id','=', False)]}" />
        </xpath> -->

        <form>
          <sheet>

            <!-- button 出現在 sheet 的右上角位置 -->
            <div class="oe_button_box" name="button_box">
              <!-- 重要參數 1. name : 對應 model 的自定義 fn  2.type="object" 表示呼叫 model method-->
              <button
                type="object"
                name="show_sheet_of_thisObj"
                string="show SHEET"
                attrs="{'invisible':[('sheet_id','=', False)]}"
                class="oe_stat_button"
                icon="fa-bars" />
            </div>
            <group>
              <field name="name" />
              <field name="value" />
              <field name="value2" />
              <field name="user_id" />
              <field name="employee_id" />
              <field name="tag_ids" widget="many2many_tags" /> <!-- widget -->
              <field name="gender" />
              <field name="sheet_id" />
              <field name="description" />
            </group>
          </sheet>
        </form>
      </field>
    </record>


    <!-- sheet model form -->
    <record id="view_form_demo_expense_sheet_tutorial" model="ir.ui.view">
      <field name="name">Demo Expense Sheet Tutorial Form</field>
      <field name="model">twturbiks_starter.sheet</field>
      <field name="arch" type="xml">
        <form string="main object Sheet Tutorial">
          <sheet>
            <div class="oe_button_box" name="button_box">
              <!-- 參數 : 1. name: 對應 model 的自定義 fn 2. main_object_ids 對應下方 notebook 的 field 
              ，表示無資料時不顯示 btn 3.type="object" 表示呼叫 model method -->
              <button
                type="object"
                name="show_all_main_objs"
                string="show all main objs"
                attrs="{'invisible':[('main_object_ids','=', False)]}"
                class="oe_stat_button"
                icon="fa-bars" />
            </div>
            <group>
              <!-- sheet model 的第一個欄位 -->
              <field name="name" />
            </group>

            <!-- 這邊用 notebook tag -->
            <notebook>
              <!-- notebook tag 的顯示名字 -->
              <page string="main object page1">
                <!-- sheet model 的第二個欄位 -->
                <field name="main_object_ids">
                  <!-- tree 的 editable 也可以寫 bottom ，這樣新增的資料就會加到最下面 -->
                  <tree editable="top">
                    <field name="name" />
                    <field name="value" />
                    <field name="employee_id" />
                    <field name="tag_ids" widget="many2many_tags" />
                  </tree>
                </field>
              </page>
            </notebook>

          </sheet>
        </form>
      </field>
    </record>
```

重要參數說明 :

- type : indicates how it clicking it affects Odoo:
  - object : call a method on the list’s model. The button’s name is the method, which is called with the current row’s record id and the current context.
  - action : load an execute an ir.actions, the button’s name is the database id of the action. The context is expanded with the list’s model (as active_model), the current row’s record (active_id) and all the records currently loaded in the list (active_ids, may be just a subset of the database records matching the current search)

- name : see type
- args : see type
- attrs : dynamic attributes based on record values. A mapping of attributes to domains, domains are evaluated in the context of the current row’s record, if True the corresponding attribute is set on the cell. Possible attribute is invisible (hides the button).