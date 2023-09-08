介紹 actions.server 跟 singleton

## model

```python
import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class DemoActionsSingleton(models.Model):
    _name = "demo.actions.singleton"
    _description = "Demo Actions Singleton"

    name = fields.Char("Description", required=True)

    def action_demo(self):
        # 這邊的 self 會是選中的 record , 如果選中的 records 數量不為 0 或 1 則會報錯。
        self.ensure_one()
        _logger.warning("=== CALL action_demo ===")
```
model 新增一個方法，待 server action 來 call

## security

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_twturbiks_singleton_demo_actions_singleton,twturbiks_singleton.demo_actions_singleton,model_demo_actions_singleton,base.group_user,1,1,1,1
```

## view (list form)
```xml
    <!-- form view -->
    <record id="view_form_demo_actions_singleton" model="ir.ui.view">
      <field name="name">Demo Actions Singleton Form</field>
      <field name="model">demo.actions.singleton</field>
      <field name="arch" type="xml">
        <form string="Demo Actions Singleton">
          <sheet>
            <group>
              <field name="name" />
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <!-- list view -->
    <record id="view_tree_demo_actions_singleton" model="ir.ui.view">
      <field name="name">Demo Actions Singleton List</field>
      <field name="model">demo.actions.singleton</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
        </tree>
      </field>
    </record>
```

## menu & action

```xml
    <!-- server actions -->
    <record id="action_action_demo" model="ir.actions.server">
      <field name="name">Action Demo</field>

      <!-- model_id : Odoo model linked to the action. -->
      <!-- 實際測試沒有加 model_id 一樣可以執行
           如果 ref="base.model_res_users" ， error =  <class 'AttributeError'>: "'NoneType' object has no
      attribute 'action_demo'"
      -->
      <field name="model_id" ref="twturbiks_singleton.model_demo_actions_singleton" />

      <!-- binding_model_id : specifies which model the action is bound to -->
      <!-- 
        1. 如果沒有寫 ref="twturbiks_singleton.model_demo_actions_singleton" , 則 Action Demo 的選項都沒有 ，
        不過先寫且讀取後，再 comment 掉一樣可以用，不知道是不是預設行為 ?
        
        2. 如果改成 ref="base.model_res_users",則 Action Demo 的選項都沒有 ，comment 掉一樣不會出現。
      -->
      <field name="binding_model_id" ref="twturbiks_singleton.model_demo_actions_singleton" />

      <field name="state">code</field>
      <field name="code">
        records.action_demo()
      </field>
    </record>

    <!-- demo_actions_singleton App Menu -->
    <menuitem id="demo_actions_singleton_menu" name="Demo Actions Singleton" />

    <!-- Action to open the demo_actions_singleton -->
    <record id="action_singleton" model="ir.actions.act_window">
      <field name="name">Demo Actions Singleton Action</field>
      <field name="res_model">demo.actions.singleton</field>
      <field name="view_mode">tree,form</field>
    </record>

    <!-- Menu item to open the demo_actions_singleton -->
    <menuitem id="menu_action_singleton"
      name="Demo Actions Singleton"
      action="action_singleton"
      parent="demo_actions_singleton_menu" />
```

## 筆記心得

1. `<record id="_" model="ir.actions.server">` 會實例化一個物件，所以才會有 model_id ，binding_model_id 不加也一樣有上一次設定效果的現象。

## 參照 model 與 ID 的寫法整理

```xml
<!-- 寫實際 model 的 _name -->
<field name="model">foo.bar.tar</field> 
<field name="res_model">foo.bar.tar</field>

<!-- 有 ref 表示外部參照，可加 module 名，也可以不加 -->
<!-- model_id 表示 model _name 改為開頭加 "model_" , _name 的 點 必需改為 _ -->
<field name="model_id" ref="twturbiks_singleton.model_demo_actions_singleton" />
<field name="binding_model_id" ref="twturbiks_singleton.model_demo_actions_singleton" />

<!-- 有 ref 表示外部參照，可加 module 名，也可以不加 -->
<!-- 

    view_id 要參照 view record 的 id  
    e.g. <record id="this_is_id" model="ir.ui.view"> 
      
-->
<field name="view_id" ref="module_name.this_is_id" />
```


## 參考資料 

[沈弘哲-odoo 觀念 - actions 和 singleton](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_actions_singleton)