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