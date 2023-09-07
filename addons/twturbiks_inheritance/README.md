參考 沈弘哲大大 [odoo 繼承 - class inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_class_inheritance)

## odoo 繼承三大類

odoo 的繼承有三種

![odoo inheritance](https://camo.githubusercontent.com/82f2060d30d8be1fa42fceb5638094d9e4849be5e8dca6c9e70a1fde7faa55c5/68747470733a2f2f692e696d6775722e636f6d2f32615138424e682e706e67)

- class inheritance (沿用 _name)
    - 特性
    1. 不會產生新的 table
    2. 

    - 使用場景
    1. 在一個既有的 model 上增加一個 fields.
    2. 覆蓋掉一個已經存在的 model 中的 fields 定義.
    3. 增加 constraints 到一個既有的 model 上.
    4. 增加額外的 method 到一個既有的 model 上.
    5. 覆蓋掉一個已經存在的 model 中的 method.


- prototype inheritance (定義一個 new _name)
    - 特性
    1. 產生一個全新的 table (包含 attr1)
    2. 此類別會擁有父類別的所有特性, 在此類別中的任何修改, 都不會去影響到父類別.
    - 使用場景
    1. 繼承 mail.thread 這類的 models.AbstractModel (history track 用途)

- delegation inheritance
    - 特性
    1. 產生一個全新的 table (但只有新增的欄位 e.g. attr2 , attr3 , attr1 會在父項)
       補充: 新增資料時，父項也會新增資料 e.g. attr1
    2. 
    - 使用場景


## class inheritance

### model

使用 ClassInheritance 繼承 hr.expense model ， 新增一個欄位 ' test_field ' 

```python
class ClassInheritance(models.Model):
    _name = "hr.expense"  # 可寫可不寫，若 _name 跟 _inherit 不同時，則為 prototype inheritance
    _inherit = ["hr.expense"]

    test_field = fields.Char("test_field")
```

### view

有兩種放 fields 的方法

1. 塞在 fields 裡面
2. 使用 xpath

```xml
    <!-- explicit list view definition -->

    <record id="view_expenses_tree_custom" model="ir.ui.view">
      <field name="name">hr.expense.tree.custom</field>
      <field name="model">hr.expense</field>
      <field name="inherit_id" ref="hr_expense.view_expenses_tree" />
      <field name="arch" type="xml">
        <field name="date" position="after">
          <!-- <field name="test_field" groups="product.group_sale_pricelist" readonly="1"/> -->
          <field name="test_field" />
        </field>

        <!-- xpath the same result -->
        <!--views/views.xml
      <xpath expr="//field[@name='date']" position="after">
          <field name="test_field" />
      </xpath>
      -->

      </field>
    </record>

    <!-- explicit form view definition -->

    <record id="hr_expense_view_form_custom" model="ir.ui.view">
      <field name="name">hr.expense.view.form.custom</field>
      <field name="model">hr.expense</field>
      <field name="inherit_id" ref="hr_expense.hr_expense_view_form" />
      <field name="arch" type="xml">
        <field name="employee_id" position="after">
          <field name="test_field" />
        </field>
      </field>
    </record>
```
### manifest

```python
...
 "depends": ["base", "hr_expense"],
...
```


## prototype inheritance

### model

```python
class PrototypeInheritance(models.Model):
    _name = "demo.prototype"
    _description = "PrototypeInheritance"
    _inherit = ["mail.thread"]

    # 'demo.prototype' 擁有 'mail.thread'(父類別) 的所有特性,
    #  mail.thread 提供 message_follower_ids ,message_ids 等 fields 可使用
    # 在這裡面的修改, 都不會去影響到 'mail.thread'(父類別).

    test_field = fields.Char("test_field")
```

### security

```csv title="security/ir.model.access.csv"
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_twturbiks_inheritance_demo_prototype,twturbiks_inheritance.demo_prototype,model_demo_prototype,base.group_user,1,1,1,1
```

### view

```xml
    <!-- explicit list view definition -->

    <record id="view_tree_demo_prototype_tutorial" model="ir.ui.view">
      <field name="name">Demo Prototype List</field>
      <field name="model">demo.prototype</field>
      <field name="arch" type="xml">
        <tree>
          <field name="test_field" />
        </tree>
      </field>
    </record>

    <!-- explicit form view definition -->

    <record id="view_form_demo_prototype_tutorial" model="ir.ui.view">
      <field name="name">Demo Prototype Form</field>
      <field name="model">demo.prototype</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="test_field" />
            </group>
          </sheet>
          <div class="oe_chatter">
            <field name="message_follower_ids" widget="mail_followers" />
            <field name="message_ids" widget="mail_thread" />
          </div>
        </form>
      </field>
    </record>
```

### manifest

```python
    "data": [
        "security/ir.model.access.csv",
        "views/PrototypeInheritance_view.xml",
        ...
    ],
```

## delegation inheritance

## 參考資料

[odoo 繼承 - class inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_class_inheritance)
[odoo 繼承 - prototype inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_prototype_inheritance)
[odoo 繼承 - delegation inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_delegation_inheritance)