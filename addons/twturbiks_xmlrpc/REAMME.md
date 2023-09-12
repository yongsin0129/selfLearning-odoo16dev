XMLRPC

server 一般都是用 RESTful api 的方式與前端做互動

類似 node.js : express , koa , python : flask , django

但 odoo 中使用 XMLRPC 的方式

## 測試 step

1. 先把 odoo server run 起來
2. 使用 `xmlrpc.client` 對 server 做連線的動作
3. 
```python
# 測試連線
print(
    xmlrpc.client.ServerProxy(
        "{}/xmlrpc/2/common".format("http://0.0.0.0:8069")
    ).version()
)

# common 就是一個 server obj ，可以做 rpc
common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
```

## 常見 method 整理

[odoo12 XMLRPC Calling methods](https://www.odoo.com/documentation/12.0/developer/webservices/odoo.html#calling-methods)

[odoo16 XMLRPC Calling methods](https://www.odoo.com/documentation/master/developer/reference/external_api.html#calling-methods)

m2x 寫法

```
(0, 0,  { values })    link to a new record that needs to be created with the given values dictionary

(1, ID, { values })    update the linked record with id = ID (write *values* on it)

(2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)

(3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)

(4, ID)                link to existing record with id = ID (adds a relationship)

(5)                    unlink all (like using (3,ID) for all linked records)

(6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
```

## 參考資料 

沈弘哲大大 [如何使用 python xmlrpc 連接 odoo-12](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/xml-rpc-odoo)

沈弘哲大大 [如何使用 python xmlrpc 連接 odoo-14](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/xml-rpc-odoo)