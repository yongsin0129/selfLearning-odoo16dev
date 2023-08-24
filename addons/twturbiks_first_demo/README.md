odoo 手把手建立第一個 addons

參考 : 沈弘哲大大的 [odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

## model

odoo 中的 model 主要有幾個, 分別是 AbstractModel、Model、TransientModel,

[official - model](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#models)

### field attribute - track_visibility

1. manifest 的依賴要有　mail 

``` py
    'depends': ['base','mail'],
```

2. model 必需繼承　mail 的相關屬性

```py
_inherit = ["mail.thread", "mail.activity.mixin"]  # 集成消息模型 增加消息记录通知功能
```

3. model field attribute 要設定

```py
  name = fields.Char(tracking=True)
  
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