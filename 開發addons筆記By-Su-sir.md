## step 0

使用腳本架新增模組
[official tutorial](https://www.odoo.com/documentation/15.0/developer/cli.html#reference-cmdline-scaffold)

Scaffolding
Scaffolding is the automated creation of a skeleton structure to simplify bootstrapping (of new modules, in the case of Odoo). While not necessary it avoids the tedium of setting up basic structures and looking up what all starting requirements are.

Scaffolding is available via the odoo-bin scaffold subcommand.

```
$ python3 odoo-bin scaffold my_module ../addons/

  - scaffold 建立架本架
  - 第一個參數 資料夾名稱
  - 第二個參數 資料夾產生的位置
```
## step 1 編輯畫面

一開始的 model , controller , view 都是被 comment 起來的

```xml title="my_module/views/views.xml"
<odoo>
  <data>
    <!-- explicit list view definition 這邊是 list 的畫面 -->
<!--
    <record model="ir.ui.view" id="my_module.list">
      <field name="name">my_module list</field>
      <field name="model">my_module.my_module</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name"/>
          <field name="value"/>
          <field name="value2"/>
        </tree>
      </field>
    </record>
-->

    <!-- actions opening views on models 這邊是 action 的動作 -->
<!--
    <record model="ir.actions.act_window" id="my_module.action_window">
      <field name="name">my_module window</field>
      <field name="res_model">my_module.my_module</field>
      <field name="view_mode">tree,form</field>
    </record>
-->

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

    <!-- Top menu item 這邊是 主選單 的畫面 -->
<!--
    <menuitem name="my_module" id="my_module.menu_root"/>
-->
    <!-- menu categories 這邊是 目錄選單 的畫面 -->
<!--
    <menuitem name="Menu 1" id="my_module.menu_1" parent="my_module.menu_root"/>
    <menuitem name="Menu 2" id="my_module.menu_2" parent="my_module.menu_root"/>
-->
    <!-- actions 這邊是 實際上 的 action -->
<!--
    <menuitem name="List" id="my_module.menu_1_list" parent="my_module.menu_1"
              action="my_module.action_window"/>
    <menuitem name="Server to list" id="my_module" parent="my_module.menu_2"
              action="my_module.action_server"/>
-->
  </data>
</odoo>
```

## step 2 權限開放

```python title="my_module/__manifest__.py"
# -*- coding: utf-8 -*-
{
    'name': "my_module",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "yongsin0129",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv', # <------ 這邊打開權限
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
```

## step 3 server restart

記得 module 必需要點 "升級"

## 參考資料

[kulius Odoo 顧問及客製-DAY 02 : Odoo 15 基礎開發](https://ithelp.ithome.com.tw/m/articles/10291865)