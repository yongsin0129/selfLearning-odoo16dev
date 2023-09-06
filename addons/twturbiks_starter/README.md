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

## ORM method : name_get , name_search

[odoo系统中 name_search 和 name_get 用法](https://blog.51cto.com/melon0809/5389459)
[odoo name_get](https://www.cnblogs.com/smarttony/p/11910963.html)

### name_get

透過 重写 name_get 方法, 返回 更多資料給畫面 (自定義組合的名稱)

e.g. 

- 每一個 record 想要增加流水號 or 日期時間與 name 結合使用 ( 2023-09-01-foo )

```python title="models/models.py"
    # 當頁面要看到 many2one 的時候就會觸發
    # 注意 : db 只會存 name (也就是 foo)，組合文字不會存入，所以想要搜尋時是看不到的 !!
    # Tip : 如果使用現有 field 來做組合文字，可以透過重寫 name_search 來做到 search 組合文字
    def name_get(self):
        names = []
        for record in self:
            # 兩種寫法都行
            # name = "%s-%s" % (record.create_date.date(), record.name)
            name = "{}_{}".format(record.create_date.date(), record.name)
            names.append((record.id, name))
        return names
```

### name_search

原始的 name_search 只會 search name field , 可以透過 重写 name_get 方法, 增加搜尋的彈性

e.g. 上面建立的 sheet 頁面顯示是 2023-09-01-foo , 但輸入 09-01 確找不到，因為 model 沒有這個 name 

所以我們 overwrite 原有 orm 的 name_search method , 在 domain 中新增想查找的條件

```python title="models/models.py"
    # 查看 many2one 的時候就會觸發
    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []

        domain = args + [
            "|", # 這邊記得
            "|", # 這邊記得 有第三個條件時就需要加第二個 | 
            ("id", operator, name),
            ("name", operator, name),
            ("create_date", operator, name),
        ]
        # domain = args + [("create_date", operator, name)]
        # domain = args + [("id", operator, name)]
        return self.search(domain, limit=limit).name_get()
        # return self.search(domain, limit=limit).name_get() # 原作用繼承寫法，不過直接使用 self 看起來一樣 ？
```
補充 : "|" 符号是用于组合搜索条件的逻辑运算符。它的作用是将多个搜索条件组合在一起，并且只要满足其中一个条件即可返回结果。

#### domain 設定補充

[[SOLVED] What does "=ilike" in domain operator used for?](https://www.odoo.com/zh_TW/forum/bang-zhu-1/solved-what-does-ilike-in-domain-operator-used-for-58261)

- [('name', 'like', 'dog')]

    This will find recods with name 'dog', 'dogs', 'bulldog', ... but not 'Dog'.

- [('name', '=like', 'dog')]

    This will find records with name 'dog' (it's almost exactly like the '=' operator).

- [('name', 'ilike', 'dog')]

    This is the most universal search. It will find records with name 'dog', 'DOGS', 'Bulldog', etc..

- ['name', '=ilike', 'dog')]

    This will find records with name 'dog', 'DOG', 'Dog', 'DOg', DoG', 'dOG', 'doG' and 'dOg'.


#### 原碼補充

ref : https://blog.csdn.net/qq_29654325/article/details/119797528 => name_search 的结果，其实是 name_get() 的返回值

1. call name_search 在原碼中就是 call _name_search
```
        ids = self._name_search(name, args, operator, limit=limit)
        return self.browse(ids).sudo().name_get()
```
2. _name_search 會 call _search 後返回 ids
3. 最後 name_search 再利用 browse(ids) call name_get()


``` 
    def browse(self, ids=None):
        """ browse([ids]) -> records

        Returns a recordset for the ids provided as parameter in the current
        environment.

        .. code-block:: python

            self.browse([7, 18, 12])
            res.partner(7, 18, 12)

        :param ids: id(s)
        :type ids: int or iterable(int) or None
        :return: recordset
        """
        if not ids:
            ids = ()
        elif ids.__class__ is int:
            ids = (ids,)
        else:
            ids = tuple(ids)
        return self.__class__(self.env, ids, ids)
```

## 使用 ORM 對 One2many M2X 欄位做 CRUD

### view

先把四個 button 都先寫好

```xml title="views/views.xml"
          ...
      <field name="arch" type="xml">
        <form string="main object Sheet Tutorial">
          <header>
            # 新增一筆 main obj 並與 sheet 做關連
            <button name="add_demo_main_obj_record" string="add demo main obj record" type="object" />
            # 關連一筆已經實例化的 main obj
            <button name="link_demo_main_obj_record" string="link demo main obj record"
              type="object" />
            # 將 sheet 的關連表　取代為　新的關連表
            <button name="replace_demo_main_obj_record" string="replace main obj record"
              type="object" />
            # 將 sheet 的關連表全部洗掉，變為空
            <button name="unlink_demo_main_obj_record" string="unlink main obj record"
              type="object" />
          </header>
          <sheet>
          ...
```

### model method

```python 
class DemoExpenseSheetTutorial(models.Model):
    _name = "twturbiks_starter.sheet"
    _description = "Demo Sheet Tutorial"

    name = fields.Char("Sheet Report", required=True)

    main_object_ids = fields.One2many(
        "twturbiks_starter.main",  # 代表關連的 model (必填)
        "sheet_id",  # 代表所關連 model 的 field (必填)
        string="Main Object Lines",
    )

    ...

    # 透過 button 來新建一筆 main obj 資料
    def add_demo_main_obj_record(self):
        # (0, _ , {'field': value}) creates a new record and links it to this one.

        # ref 會使用外部連結，找到 record XML ID
        # 補充 :　並不是對應到 demo or data folder 內 record 的 XML ID，而是對應到已經被　ORM 創造出來，有 XML ID 的 RECORD
        data_1 = self.env.ref("twturbiks_starter.object14")

        tag_data_1 = self.env.ref("twturbiks_starter.tag12")
        tag_data_2 = self.env.ref("twturbiks_starter.tag13")

        # 將 ref 抓到的資料放入 dict.
        for record in self:
            # creates a new record
            val = {
                "name": data_1.name,
                "value": data_1.value,
                "employee_id": data_1.employee_id,
                "tag_ids": [(6, 0, [tag_data_1.id, tag_data_2.id])],
            }

            # 讓自已 sheet 的 one2many 新增一筆 record , 並有自已的 ID ，此 ID 非 XML ID
            # main_object_ids 對應的是 twturbiks_starter.main model
            self.main_object_ids = [(0, 0, val)]

    def link_demo_main_obj_record(self):
        # (4, id, _) links an already existing record.

        #  必需 link 已經存在的 record (已經創造出來有 XML ID 的 record)
        data_1 = self.env.ref("twturbiks_starter.object14")

        for record in self:
            # link already existing record
            self.main_object_ids = [(4, data_1.id, 0)]

    def replace_demo_main_obj_record(self):
        # (6, _, [ids]) replaces the list of linked records with the provided list.

        data_1 = self.env.ref("twturbiks_starter.object11")
        data_2 = self.env.ref("twturbiks_starter.object13")

        for record in self:
            # replace multi record
            self.main_object_ids = [(6, 0, [data_1.id, data_2.id])]

    def unlink_demo_main_obj_record(self):
        # (5, , ) removes all the links, without deleting the linked records.

        for record in self:
            # unlink multi record but without deleting
            self.main_object_ids = [(5, 0, 0)]
```

筆記 : 

- 新增會實例化一筆新的 main obj record , 而 link 不會。
- self.env.ref("外部連結") 外部連結對應到的是已經實例化的 XML ID

## view : tree view 上做 CRUD 的限制

### menu
```xml title="views/menu.xml"
  <!--  -->
  <!-- menu 3     main model but no create-->
  <!--  -->

  <!-- action for open main model -->
  <record model="ir.actions.act_window" id="twturbiks_starter.open_main_no_create">
    <field name="name">twturbiks_starter main model no create</field>
    <field name="res_model">twturbiks_starter.main</field>
    <field name="view_mode">tree</field>
    <!-- ref="twturbiks_starter.list_no_create" : 這個 action 要連結 view id 
      id 的寫法 : twturbiks_starter.list_no_create or list_no_create 都可以
      最多一個 "點" , 這個點的前面必需是一個已經安裝的 module name ,如果沒有點，則會 search 此 module 內的 id
    -->
    <field name="view_id" ref="twturbiks_starter.list_no_create" />
  </record>

  <!-- 單層 Menu for open main model no create -->
  <menuitem name="Menu 3 no create" id="twturbiks_starter.menu_3"
    action="twturbiks_starter.open_main_no_create"
    parent="twturbiks_starter.menu_root" sequence="3" />
```

- view_id
specific view added to the views list in case its type is part of the view_mode list and not already filled by one of the views in view_ids

These are mostly used when defining actions from Data Files:

```xml
<record model="ir.actions.act_window" id="test_action">
    <field name="name">A Test Action</field>
    <field name="res_model">some.model</field>
    <field name="view_mode">graph</field>
    <field name="view_id" ref="my_specific_view"/>
</record>
```
will use the “my_specific_view” view even if that’s not the default view for the model.

The server-side composition of the views sequence is the following:

1. get each (id, type) from view_ids (ordered by sequence)

2. if view_id is defined and its type isn’t already filled, append its (id, type)

3. for each unfilled type in view_mode, append (False, type)

參考資料

- ir.actions.act_window 的文檔
    https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/backend/actions.html?highlight=act_window#window-actions-ir-actions-act-window
    
- view_id 的文檔 :
    https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/backend/views.html#methods

### view

```xml title="views/views.xml"

    <!-- main model list no create-->
    <record model="ir.ui.view" id="twturbiks_starter.list_no_create">
      <field name="name">twturbiks_starter list no create</field>
      <field name="model">twturbiks_starter.main</field>
      <field name="arch" type="xml">
        <!-- 重點在這段
        0 false
        1 true 
        可以混寫 ，目前的寫法表示 : 不能新增、刪除，可以修改        
        -->
        <tree string="no_create_tree" create="0" delete="false" edit="1" editable="top"> 
          <field name="name" />
          <field name="value" />
          <field name="value2" />
          <field name="user_id" />
          <field name="employee_id" />
          <field name="tag_ids" widget="many2many_tags" />
          <field name="gender" />
          <field name="sheet_id" />
          <field name="description" />
        </tree>
      </field>
    </record>

```

## Active Archive Ribbon

### model
```python title="models/models.py"
class DemoMain(models.Model):
    _name = "twturbiks_starter.main"
    _description = "this is main model of this module "

    ...
    active = fields.Boolean("Active", default=True)
    ...

```

[What Is Automatic & Reserved Fields in Odoo 16](https://www.cybrosys.com/blog/what-is-automatic-and-reserved-fields-in-odoo-16)

保留 fields : id

- View fields 

create_date,write_date,create_uid,write_uid

- Access Log Fields

name,active,State,company_id,

### view

```xml title="views/views.xml"
    <!-- main model form -->
    <record model="ir.ui.view" id="twturbiks_starter.form">
      <field name="name">twturbiks_starter form</field>
      <field name="model">twturbiks_starter.main</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <widget name="web_ribbon" title="封存" bg_color="bg-danger"
              attrs="{'invisible': [('active', '=', True)]}" />
              ...
            <group>
              ...
              <field name="active" invisible="0" />
            </group>
          </sheet>
        </form>
      </field>
    </record>
```

就算 model 有 active 的 field , 但 form 如果沒有寫進去，一樣不會出現封存的動作 button

## search panel

search panel 只支援 many2one 跟 selection fields.

```xml title="views/views.xml"
    <!-- search view -->
    <record id="view_filter_twturbiks_starter_main" model="ir.ui.view">
      <field name="name">twturbiks_starter main Filter</field>
      <field name="model">twturbiks_starter.main</field>
      <field name="arch" type="xml">
        <search string="twturbiks_starter main model Filter">
          ...

          <searchpanel>
            <field name="user_id" select="multi" icon="fa-address-card" enable_counters="1"
              color="#fc03d7" />
            <field name="employee_id" select="multi" icon="fa-building" enable_counters="1" />
            <field name="sheet_id" icon="fa-users" enable_counters="1" />

            <!-- error example 只有 store=true (一般或多對多) 對 "groupby" 參數有效 -->
            <field name="gender" icon="fa-cutlery" enable_counters="1" color="#d10202" />

            <!-- error example 僅支援類別多對一選擇的類型 , but (found type 整數) -->
            <!-- <field name="value" icon="fa-users" enable_counters="1" /> -->

            <!-- error example 僅支援 m2one , not m2x-->
            <!-- <field name="tag_ids" icon="fa-users" /> -->
          </searchpanel>
        </search>
      </field>
    </record>

```

- select="multi" 是否可以多選.

- enable_counters="1" 是否顯示數量.

- icon="fa-building" icon 圖示顯示.
    [fontawesome v4](https://fontawesome.com/v4/icons/)

    因為 odoo16 原生只支援 V4 ，如果需要用到 v5 icon ，使用下面的升級 module
    [odoo module : Web Font Awesome 5.3](https://apps.odoo.com/apps/modules/16.0/exaly_font_awesome/)
    [fontawesome v5](https://fontawesome.com/icons)

- color="#d10202" color 顯示.
    [hexcolor seletor](https://g.co/kgs/ksx4DS)

## odoo shell

Odoo shell，也被稱為Odoo命令行界面（CLI），是由Odoo提供的一個命令行工具，允許您使用Python命令與Odoo實例進行交互。它提供了一種執行Python代碼並與Odoo環境進行交互的方式，包括訪問和操作數據庫中的數據，運行查詢以及執行各種管理任務。

### 指令

簡化版
`python3 odoo-bin shell -d twturbiks_starter -c config/odoo.conf`

完整版
`python3 odoo-bin shell -d twturbiks -w odoo -r odoo --db_port=5432 --db_host=localhost --addons-path='/home/twtrubiks/odoo/addons`



-d : 讀取的 db 名字
-c : 裡面已經設定帳號密碼 host port addons 所以可以用簡化版
--log-level=debug_sql : 開啟 raw sql 

以下只介紹簡單的 CRUD

#### search (R)

```shell
>>> self.env['res.partner'].search([])
res.partner(65, 66, 44, 45, 51, 52, 14, 26, 33, 27, 61, 62, 10, 35, 18, 19, 58, 59, 64, 63, 11, 20, 22, 31, 23, 54, 48, 50, 15, 34, 49, 42, 41, 57, 60, 47, 12, 21, 25, 37, 24, 36, 30, 38, 43, 46, 13, 29, 28, 55, 53, 56, 9, 17, 32, 16, 1, 39, 40, 8, 7, 3)

>>> self.env['res.partner'].search([('id','in',[11,20])])
res.partner(11, 20)

>>> self.env['res.partner'].browse([11, 20])
res.partner(11, 20)

>>> recordsets = self.env['res.partner'].browse([11, 20])
>>> recordsets
res.partner(11, 20)

>>> recordsets.ids
[11, 20]
```

#### create (C)

```shell
>>> partner = self.env['res.partner']
>>> partner.search([])
res.partner(65, 66, 44, 45, 51, 52, 14, 26, 33, 27, 61, 62, 10, 35, 18, 19, 58, 59, 64, 63, 11, 20, 22, 31, 23, 54, 48, 50, 15, 34, 49, 42, 41, 57, 60, 47, 12, 21, 25, 37, 24, 36, 30, 38, 43, 46, 13, 29, 28, 55, 53, 56, 9, 17, 32, 16, 1, 39, 40, 8, 7, 3)

>>> partner.create({'name': 'yongsin0129', 'is_company': True})
res.partner(67,)

>>> partner.browse(67).name
'yongsin0129'
```

#### write (U)

```shell
>>> partner.browse(67).write({'name':'yongsin0130'})
True
>>> partner.browse(67).name
'yongsin0130'
```
#### delete (D)

```shell
>>> partner.browse(67).unlink()
2023-09-06 06:27:53,855 81197 INFO twturbiks_starter odoo.models.unlink: User #1 deleted mail.message records with IDs: [209] 
2023-09-06 06:27:53,898 81197 INFO twturbiks_starter odoo.models.unlink: User #1 deleted res.partner records with IDs: [67] 
True

raise MissingError("\n".join([
odoo.exceptions.MissingError: Record does not exist or has been deleted.
(Record: res.partner(67,), User: 1)
```

注意 : 當更新 One2many 和 Many2many 時, 要使用比較特別的語言 0-6 的那個指令

### 參考資料

[What is Odoo Shell & How to Access It in Odoo 16](https://www.cybrosys.com/blog/what-is-odoo-shell-and-how-to-access-it-in-odoo-16)

[沈沈弘哲大大-odoo shell](https://github.com/twtrubiks/odoo-demo-addons-tutorial#shell)

## auto_join

### 單 table 查詢
```shell
>>> self.env['twturbiks_starter.main'].search([('sheet_id','in',[2])])
twturbiks_starter.main(8, 9)
```
```sql
select
	"twturbiks_starter_main".id
from
	"twturbiks_starter_main"
where
	(("twturbiks_starter_main"."active" = true)
		and ("twturbiks_starter_main"."sheet_id" in (2)))
order by
	"twturbiks_starter_main"."id"
```

### 跳第二個 table 查詢

目前的 auto_join 為預設的 false

使用子查詢，先到  twturbiks_starter_sheet 裡面查 id = 2 

```shell
>>> self.env['twturbiks_starter.main'].search([('sheet_id.id','=','2')])
twturbiks_starter.main(8, 9)
```
```sql
select
	"twturbiks_starter_main".id
from
	"twturbiks_starter_main"

-- 這邊的 where 使用子查詢，先到  twturbiks_starter_sheet 裡面查一遍
where
	(("twturbiks_starter_main"."active" = true)
		and ("twturbiks_starter_main"."sheet_id" in (
		select
			"twturbiks_starter_sheet".id
		from
			"twturbiks_starter_sheet"
		where
			("twturbiks_starter_sheet"."id" = '2'))))
order by
	"twturbiks_starter_main"."id"
```

### 跳第二個 table 查詢 (auto_join=True)

使用 left join 先把 table 組合起來，再查 sheet_id = 2

```shell
>>> self.env['twturbiks_starter.main'].search([('sheet_id.id','=','2')])
twturbiks_starter.main(8, 9)
```
```sql
select
	"twturbiks_starter_main".id
from
	"twturbiks_starter_main"
left join "twturbiks_starter_sheet" as "twturbiks_starter_main__sheet_id" on
	("twturbiks_starter_main"."sheet_id" = "twturbiks_starter_main__sheet_id"."id")
where
	(("twturbiks_starter_main"."active" = true)
		and ("twturbiks_starter_main__sheet_id"."id" = '2'))
order by
	"twturbiks_starter_main"."id"
```