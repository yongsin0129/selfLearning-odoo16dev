參考 沈弘哲大大 [odoo hierarchy 實作](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_hierarchy_tutorial#odoo-hierarchy-%E5%AF%A6%E4%BD%9C)

## hierarchy 介紹

資料庫的關連除了 m2o , o2m , m2x

還有一種是自關連，就是 hierarchy

## model

```python
class DemoHierarchyTutorial(models.Model):
    _name = "demo.hierarchy"
    _description = "Demo Hierarchy Tutorial"

    name = fields.Char(string="name", index=True)
    # Many2one : 這個 one 就是 parent Id , 本身類有很多個，都指向同一個 parent
    parent_id = fields.Many2one("demo.hierarchy", string="Related Partner", index=True)
    # 因為只會有一個，所以 related 指向就是 parent
    parent_name = fields.Char(
        related="parent_id.name", readonly=True, string="Parent name"
    )
    # one2many : 這個 one 就是自已
    # "demo.hierarchy", "parent_id"　： 到這個 model 中找 parent_id　等於自已本身 id 的所有物件。
    child_ids = fields.One2many(
        "demo.hierarchy", "parent_id", string="Contacts", domain=[("active", "=", True)]
    )
    active = fields.Boolean(default=True)

# python orm ：　說明 child_of 和 parent_of 的使用方法
# https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_hierarchy_tutorial#%E8%AA%AA%E6%98%8E-child_of-%E5%92%8C-parent_of

```

## security

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_twturbiks_hierarchy_main,twturbiks_hierarchy.main,model_demo_hierarchy,base.group_user,1,1,1,1
```

## views

### views
```xml
<odoo>
  <data>
    <record id="view_tree_demo_hierarchy" model="ir.ui.view">
      <field name="name">Demo Hierarchy List</field>
      <field name="model">demo.hierarchy</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
          <field name="active" />
          <field name="parent_id" />
          <field name="parent_name" />
        </tree>
      </field>
    </record>

    <record
      id="view_form_demo_hierarchy" model="ir.ui.view">
      <field name="name">Demo Hierarchy Form</field>
      <field name="model">demo.hierarchy</field>
      <field name="arch" type="xml">
        <form string="Demo Hierarchy">
          <sheet>
            <group>
              <field name="name" />
              <field name="active" />
              <field name="parent_id" />
              <field name="parent_name" />
            </group>
            <notebook>
              <page string="Hierarchy">
                <field name="child_ids" mode="kanban">
                  <form string="Contact / Address">
                    <sheet>
                      <field name="parent_id" invisible="1" />
                      <hr />
                      <group>
                        <field name="name" string="Contact Name" />
                      </group>
                    </sheet>
                  </form>
                </field>
              </page>
            </notebook>
          </sheet>
        </form>
      </field>
    </record>
  </data>
</odoo>
```

### menu

```xml
<?xml version="1.0"?>
<odoo>

  <!-- demo_hierarchy App Menu -->
  <menuitem id="demo_hierarchy_menu"
    name="Demo Hierarchy" />

  <!-- Action to open the demo_hierarchy_menu -->
  <record id="action_hierarchy" model="ir.actions.act_window">
    <field name="name">Demo Hierarchy Action</field>
    <field name="res_model">demo.hierarchy</field>
    <field name="view_mode">tree,form</field>
  </record>

  <!-- Menu item to open the demo_hierarchy_menu -->
  <menuitem id="menu_odoo_tutorial"
    name="Demo Hierarchy Tutorial"
    action="action_hierarchy"
    parent="demo_hierarchy_menu" />
</odoo>
```

## manifest

```python
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/templates.xml",
        "views/views.xml",
    ],
```