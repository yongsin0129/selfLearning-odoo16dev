參考 沈弘哲大大 [odoo 繼承 - class inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_class_inheritance)

## odoo 繼承三大類

odoo 的繼承有三種

![odoo inheritance](https://camo.githubusercontent.com/82f2060d30d8be1fa42fceb5638094d9e4849be5e8dca6c9e70a1fde7faa55c5/68747470733a2f2f692e696d6775722e636f6d2f32615138424e682e706e67)

- class inheritance
    - 特性
    1. 不會產生新的 table
    2. 

    - 使用場景
    1. 在一個既有的 model 上增加一個 fields.
    2. 覆蓋掉一個已經存在的 model 中的 fields 定義.
    3. 增加 constraints 到一個既有的 model 上.
    4. 增加額外的 method 到一個既有的 model 上.
    5. 覆蓋掉一個已經存在的 model 中的 method.


- prototype inheritance
    - 特性
    1. 產生一個全新的 table (包含 attr1)
    2. 
    - 使用場景


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

## delegation inheritance

## 參考資料

[odoo 繼承 - class inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_class_inheritance)
[odoo 繼承 - prototype inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_prototype_inheritance)
[odoo 繼承 - delegation inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_delegation_inheritance)