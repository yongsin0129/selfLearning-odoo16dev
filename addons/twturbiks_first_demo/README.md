odoo 手把手建立第一個 addons

參考 : 沈弘哲大大的 [odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

## model

odoo 中的 model 主要有幾個, 分別是 AbstractModel、Model、TransientModel,

[official - model](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#models)

### ===== field 介紹 =====


### track_visibility

1. manifest 的依賴要有　mail 

``` python
    'depends': ['base','mail'],
```

2. model 必需繼承　mail 的相關屬性

```python
_inherit = ["mail.thread", "mail.activity.mixin"]  # 集成消息模型 增加消息记录通知功能
```

3. model field attribute 要設定

```python
  name = fields.Char(tracking=True)
  
  # 以下兩種也可以
  # track_visibility="always"
  # track_visibility="onchange"
```

4. 視圖 form 需增加 chatter 欄位

```xml
    <div class="oe_chatter">
      <field name="message_follower_ids" widget="mail_followers"/>
      <field name="activity_ids" widget="mail_activity"/>
      <field name="message_ids" widget="mail_thread"/>
    </div>
```

[odoo14 mail.thread邮件消息机制（发送消息、字段变化跟踪记录）mail.activity.mixin安排活动](https://blog.csdn.net/weixin_44863237/article/details/123736932)

[official - Activities tracking](https://www.odoo.com/documentation/14.0/developer/reference/addons/mixins.html?highlight=mixins#activities-tracking)

### computed field

會搭配 api.depends() 一起使用

>computed_field 1. 預設是 readonly, 2.不存在 db中 (store=False), 3.搜尋 field_compute_demo 時, 會發現錯誤,

[official - computed field](https://www.odoo.com/documentation/12.0/developer/reference/orm.html#computed-fields)

Fields can be computed (instead of read straight from the database) using the compute parameter. It must assign the computed value to the field. If it uses the values of other fields, it should specify those fields using depends():

```python
    # float digits
    # field tutorial , input_number Float field 中的 digits 為設定進位以及小數點, 像這邊是算到小數點第3位並使用10進位
    input_number = fields.Float(string="input number", digits=(10, 3))

    # compute (str) – name of a method that computes the field
    # inverse (str) – name of a method that inverses the field (optional)
    # search (str) – name of a method that implement search on the field (optional)

    field_compute_demo = fields.Integer(
        compute="_get_field_compute",
        inverse="_set_input_number",
        search="_search_upper",
    )

    # 不掛 decorator 也可以 : invers 定義後就可以對它做修改，任意改 input_number 或 field_compute_demo 都可以互相 trigger.
    def _set_input_number(self):
        for data in self:
            data.input_number = data.field_compute_demo / 1000

    # 不掛 decorator 也可以 : 過 search 定義後就可以使用搜尋功能
    def _search_upper(self, operator, value):
        return [("input_number", operator, value)]
```

### ===== decorator 介紹 =====

[official - decorator doc](https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/backend/orm.html?highlight=api%20depend#module-odoo.api)

### api.constrains

```python
    from odoo.exceptions import ValidationError

    # default, 設定為當天的時間,當建立一筆資料時, 會顯示當下的時間,
    start_datetime = fields.Datetime("Start DateTime", default=fields.Datetime.now())
    stop_datetime = fields.Datetime("End Datetime")

    # 使用 api 的功能來限制欄位輸入值 , 並拋出 error message
    @api.constrains("start_datetime", "stop_datetime")
    def _check_date(self):
        for data in self:
            if data.start_datetime > data.stop_datetime:
                raise ValidationError("data.stop_datetime  > data.start_datetime")
```

### api.onchange

```python

    @api.onchange("field_onchange_demo")
    def onchange_demo(self):
        if self.field_onchange_demo:
            # "set {}".format(self.field_onchange_demo) e.g : 輸入 "hello" => "set hello"
            self.field_onchange_demo_set = "set {}".format(self.field_onchange_demo)

```
補充說明 :  onchange 也可以 return 一個 dict. ，細節可看 [twturbiks 筆記](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial) , keyword = "result = dict()"

### api.depends

```python

    # 監聽 input_number 欄位
    @api.depends("input_number")
    def _get_field_compute(self):
        for data in self:
            data.field_compute_demo = data.input_number * 1000
```

onchange , depends 差異補充說明

主要區分兩個比較容易的方法, 就是 @api.depends 可以使用在 related 欄位, 像是之後會介紹的 Many2one Many2many One2many 之類的. 而 @api.onchange 只能使用在同一個 model 上.

### _sql_constraints

用法 :

> _sql_constraints= []
> SQL constraints [(name, sql_def, message)]

```python
    # 使用 sql 限制 name 必需為唯一值
    _sql_constraints = [
        ("name_uniq", "unique(name)", "name must be unique"),
    ]
    
```

## view

### tree view

```xml
    <record model="ir.ui.view" id="twturbiks_first_demo.list">
      <field name="name">twturbiks_first_demo list</field>
      <field name="model">twturbiks_first_demo.twturbiks_first_demo</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name"/>
          <field name="name_track_always"/>
          <field name="value"/>
          <field name="value2"/>
          <field name="is_done_track_onchange"/>
          <field name="start_datetime"/>
          <field name="stop_datetime"/>
        </tree>
      </field>
    </record>
```

### form view

如果都沒寫, 系統會自己產生對應的 form view

```xml
    <record id="view_form_twturbiks_first_demo_list" model="ir.ui.view">
      <field name="name">twturbiks_first_demo list form</field>
      <field name="model">twturbiks_first_demo.twturbiks_first_demo</field>
      <field name="arch" type="xml">
        <form string="twturbiks_first_demo">
          <sheet>
            <group>
              <field name="name"/>
              <field name="name_track_always"/>
              <field name="is_done_track_onchange"/>
              <field name="value"/>
              <field name="value2"/>
              <field name="description"/>
              <field name="start_datetime"/>
              <field name="stop_datetime"/>
              <field name="field_onchange_demo"/>
              <field name="field_onchange_demo_set" force_save="1"/>
              <!-- <field name="input_number" widget="percentage"/> -->
              <field name="input_number"/>
              <field name="field_compute_demo"/>
            </group>
          </sheet>
          <div class="oe_chatter">
            <field name="message_follower_ids" widget="mail_followers"/>
            <field name="activity_ids" widget="mail_activity"/>
            <field name="message_ids" widget="mail_thread"/>
          </div>
        </form>
      </field>
    </record>
```

注意最後一段的 message_follower_ids activity_ids message_ids,

這並不是我們所建立的 field, 而是繼承 mail.thread mail.activity.mixin 所擁有的,

### search view

```xml
    <!-- search view -->

    <record id="view_res_student_search" model="ir.ui.view">
      <field name="name">res.student.search</field>
      <field name="model">twturbiks_first_demo.twturbiks_first_demo</field>
      <field name="arch" type="xml">
        <search string="object Search">
          <!-- <field> 對應搜尋邏輯，此處我們將 name 與 name_track_always 兩個作為搜尋field -->
          <field name="name" filter_domain="[('name', 'like', self)]" />

          <field name="name_track_always" filter_domain="[('name_track_always', 'like', self)]" />

          <!-- <filter>對應過濾邏輯，我們將 is_done_track_onchange 欄位作為過濾欄位，domain內是過濾邏輯，string則是顯示的字串 -->
          <filter name='is_done_track_onchange' string="is_done_track_onchange" domain="[('is_done_track_onchange', '=', True)]" />

          <!-- <group>對應分類邏輯，我們將 is_done_track_onchange 作為分類依據 -->
          <group string="Group By">
            <filter name='is_done_track_onchange' string='is_done_track_onchange' context="{'group_by':'is_done_track_onchange'}" />
          </group>
        </search>
      </field>
    </record>
```

### action

```xml
    <!-- actions opening views on models -->

    <record model="ir.actions.act_window" id="twturbiks_first_demo.action_window">
      <field name="name">twturbiks_first_demo window</field>
      <field name="res_model">twturbiks_first_demo.twturbiks_first_demo</field>
      <field name="view_mode">tree,form</field>
    </record>
```
### menu

```xml
    <!-- Top menu item -->
    <!-- 主選單 : 點擊 home 之後出現 ， 自動與上面的 model="ir.actions.act_window" record 做連結 -->
    <!-- 裡面只有 tree 就打不開 form , 反之 只有 form ，則看不到 tree list -->

    <menuitem name="twturbiks_first_demo" id="twturbiks_first_demo.menu_root"/>

    <!-- menu categories -->
    <!-- 頁面選單，module 內部的上方選單 -->

    <menuitem name="Menu 1" id="twturbiks_first_demo.menu_1" parent="twturbiks_first_demo.menu_root"/>
    <menuitem name="Menu 2" id="twturbiks_first_demo.menu_2" parent="twturbiks_first_demo.menu_root"/>

    <!-- actions -->
    <!-- menu categories 必需指定 action ，才會顯示在上方選單  -->

    <menuitem name="List" id="twturbiks_first_demo.menu_1_list" parent="twturbiks_first_demo.menu_1" action="twturbiks_first_demo.action_window"/>
    <menuitem name="Server to list" id="twturbiks_first_demo" parent="twturbiks_first_demo.menu_2" action="twturbiks_first_demo.action_server"/>
```

## security 

### category 定義
```xml title="security/security.xml"
<?xml version="1.0" ?>
<odoo>

  <!-- 第一區 定義一個 category 權限 -->
  <!-- model="ir.module.category" -->
  <record id="module_twturbiks_first_demo" model="ir.module.category">
    <field name="name">twturbiks_first_demo category</field>
  </record>

  <!-- 第二區 繼承第一區 category : base user -->
  <!-- model="res.groups" -->
  <!-- record id 對應到 security csv 的 group id -->
  <!-- category_id 對後到上面新增加的 ir.module.category -->
  <record id="twturbiks_first_demo_group_user" model="res.groups">
    <field name="name">User</field>
    <field name="category_id" ref="module_twturbiks_first_demo"/>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
  </record>

  <!-- 第三區 繼承第一區 category 及 線性繼承 base user : manager ，表示 manger 有 user 所有的權限-->
  <!-- model="res.groups" -->
  <record id="twturbiks_first_demo_group_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="category_id" ref="module_twturbiks_first_demo"/>
    <field name="implied_ids" eval="[(4, ref('twturbiks_first_demo_group_user'))]"/>
    <field name="users" eval="[(4, ref('base.user_root')),
                  (4, ref('base.user_admin'))]"/>
  </record>

</odoo>
```

>權限設定通常都是設定一位 user , 一位 manage (admin)

implied_ids 也就是繼承, 裡面的數字分別代表不同的意思,

- (0, _ , {'field': value}) creates a new record and links it to this one.
- (1, id, {'field': value}) updates the values on an already linked record.
- (2, id, _) removes the link to and deletes the id related record.
- (3, id, _) removes the link to, but does not delete, the id related record. This is usually what you will use to delete related records on many-to-many fields.
- (4, id, _) links an already existing record.
- (5, _, _) removes all the links, without deleting the linked records.
- (6, _, [ids]) replaces the list of linked records with the provided list.

_ 也可以改成 0 or False,

尾巴不相關的可以忽略, 像是 (4, id, _) 也可以寫成 (4, id).

group_id 的部份可以空白, 下面這個例子代表這個 Access Rights 沒特別指定 group (但通常比較少這樣使用)

```excel
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_demo_test,Test Access,model_demo_odoo_tutorial,,1,1,1,1
```
這樣 odoo 後台的 設定 -> 技術 -> 安全 -> Access Rights 查詢, 他會顯示黃色的.

補充說明 : 使用線性繼承，可在 設定 -> 管理使用者 點擊使用者後看到權限設定是下拉選單
如果不是線性繼承，是單獨的 checkbox

### 權限 CRUD 設定

```excel title="security/ir.model.access.csv"

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_twturbiks_first_demo_user,twturbiks_first_demo User Access,model_twturbiks_first_demo_twturbiks_first_demo,twturbiks_first_demo_group_user,1,0,0,0
access_twturbiks_first_demo_manager,twturbiks_first_demo Manager Access,model_twturbiks_first_demo_twturbiks_first_demo,twturbiks_first_demo_group_manager,1,1,1,1

```

model_id:id 格式 model_{model _name}
group_id:id 格式 在 security.xml 內 , model="res.groups" 的 record id 

### manifest

```python
    "data": [
      ...
        "security/security.xml",
        "security/ir.model.access.csv",
      ...
    ],
```

## data , demo

- data 是安裝 module 時也會一起安裝的資料
- demo 是建立資料庫時有有勾選 demo data 才會顯示

```xml title="demo/demo.xml"
<odoo>
    <data>

          <record id="object0" model="twturbiks_first_demo.twturbiks_first_demo">
            <field name="name">Object 0</field>
            <field name="value">0</field>
          </record>

          <record id="object1" model="twturbiks_first_demo.twturbiks_first_demo">
            <field name="name">Object 1</field>
            <field name="value">10</field>
          </record>

          <record id="object2" model="twturbiks_first_demo.twturbiks_first_demo">
            <field name="name">Object 2</field>
            <field name="value">20</field>
          </record>

          <record id="object3" model="twturbiks_first_demo.twturbiks_first_demo">
            <field name="name">Object 3</field>
            <field name="value">30</field>
          </record>

          <record id="object4" model="twturbiks_first_demo.twturbiks_first_demo">
            <field name="name">Object 4</field>
            <field name="value">40</field>
          </record>

    </data>
</odoo>
```

## report

使用 Qweb 撰寫

[official - QWeb Templates](https://www.odoo.com/documentation/16.0/zh_CN/developer/reference/frontend/qweb.html) 
[csdn - odoo Qweb 语法简要记录](https://blog.csdn.net/tsoTeo/article/details/103905169)

> reports/report.xml

```xml title="reports/report.xml"
<?xml version="1.0" encoding="utf-8"?>

<odoo>
  <template id="report_twturbiks_first_demo">
    <t t-call="web.html_container">
      <!-- t-as="o" 這邊的 o 可以換成自已喜歡的變數 -->
      <!-- o 表示 ORM 的 object -->
      <t t-foreach="docs" t-as="o">
        <t t-call="web.external_layout">
          <div class="page">
            <h2>Odoo Report</h2>
            <div>
              <strong>Name:</strong>
              <p t-field="o.name" />
            </div>
            <div>
              <strong>Name_track_always:</strong>
              <p t-field="o.name_track_always" />
            </div>
            <div>
              <strong>start datetime:</strong>
              <p t-field="o.start_datetime" />
            </div>
            <div>
              <strong>stop datetime:</strong>
              <p t-field="o.stop_datetime" t-options='{"format": "Y/MM/dd"}' />
            </div>
            <!-- 可以自已定義 def 做 trigger -->
            <!-- 因為有 () ，所以需要用 t-esc 跳脫 -->
            <div>
              <strong>custom def field</strong>
              <p t-esc="o.print_hello()" />
            </div>
          </div>
        </t>
      </t>
    </t>
  </template>

  <!-- 這邊的 name ， 對應上面 template 的 id-->
  <report id="action_report_demo" string="Demo Report"
    model="twturbiks_first_demo.twturbiks_first_demo" report_type="qweb-pdf"
    name="twturbiks_first_demo.report_twturbiks_first_demo"
    file="twturbiks_first_demo.report_twturbiks_first_demo"
    print_report_name="'Demo Report - %s' % ((object.name).replace('/', ''))" />

</odoo>
```
> 記得 model 要新增 print 的方法
```python
    # 測試 report 的 template (q-web) 呼叫自定義 field 功能用的 def
    def print_hello(self):
        return "hello"
```

> 記得 manifest 要新增
```python title="__manifest__.py"
'data': [
        ......
        'reports/report.xml',
        ......
    ],
```
## controller

>記得 controller , model 都不需要加入 `__manifest__.py` ，它們加入在 `__init__.py` 中

> controllers/controllers.py
```python
    @http.route("/demo/odoo", auth="user")
    def list2(self, **kwargs):
        # 用 env 取得 ORM object ，再用 search method 取得 objs
        obj = http.request.env["twturbiks_first_demo.twturbiks_first_demo"]
        objs = obj.search([])

        # 使用外部連結 call template
        # 格式 `<module name>.<template id> , { 代入的值 }`
        return http.request.render(
            "twturbiks_first_demo.twturbiks_first_demo_template", {"objs": objs}
        )
```

> views/twturbiks_first_demo_template.xml
```xml 
<?xml version="1.0" encoding="utf-8"?>

<odoo>
  <!-- template id 為外部識別的重要指標 -->
  <template id="twturbiks_first_demo_template" name="twturbiks_first_demo_List">

    <!-- 這邊也可以用 <t t-call="web.html_container"> 先做一層包裝 -->
    <!-- <t t-call="web.html_container"> -->
    <div id="wrap" class="container">
      <h1>twturbiks_first_demo.template</h1>
      <t t-foreach="objs" t-as="obj">
        <div class="row">
          <span t-field="obj.name" />, <span t-field="obj.is_done_track_onchange" />, <span
            t-field="obj.name_track_always" />
        </div>
      </t>
    </div>
    <!-- /t -->
  </template>
</odoo>
```
> manifest

```py
    "data": [
        ...
        "views/twturbiks_first_demo_template.xml",
        ...
    ],
```