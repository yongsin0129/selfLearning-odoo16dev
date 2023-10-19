import xmlrpc.client
from pprint import pprint

# use xmlrpc 時, 建議回傳 true
# The reason is that not all client implementations of the XML-RPC protocol
# support None/Null values, and may raise errors when such a value is returned
# by a method.

url = "http://0.0.0.0:8069"
db = "twturbiks_hierarchy"
username = "admin"
password = "admin"

"""

前置作業

"""


# 確認連線 及 版本號
def common_version():
    # provides meta-calls which don’t require authentication
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
    common.version()
    print(common.version())
    return common


# 連線 db ，取得 user id
def get_uid():
    # Logging in
    common = common_version()
    uid = common.authenticate(db, username, password, {})
    print("uid:", uid)
    return uid


#  is used to call methods of odoo models via the execute_kw RPC function.
def endpoint_object():
    return xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))


"""

odoo models operation (calling method)

"""


def call_check_access_rights():
    # Calling methods
    models = endpoint_object()
    uid = get_uid()
    # check_access_rights 是一個 method , return boolean
    # 我們檢查有沒有 read 的權限
    data = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "check_access_rights",
        ["read"],
        {"raise_exception": False},
    )
    print(data)


# all
def list_all_records():
    models = endpoint_object()
    uid = get_uid()
    # List all records
    records_data = models.execute_kw(db, uid, password, "res.partner", "search", [[]])
    print(records_data)


# using domain to filter by "search"
def list_records():
    models = endpoint_object()
    uid = get_uid()
    # List records
    records_data = models.execute_kw(
        db, uid, password, "res.partner", "search", [[["is_company", "=", True]]]
    )
    print(records_data)


#  "search_count"
def count_records():
    models = endpoint_object()
    uid = get_uid()
    # Count records
    records_count = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search_count",
        [[["is_company", "=", True]]],
    )
    print(records_count)


# "limit"
def read_records():
    models = endpoint_object()
    uid = get_uid()
    # Read records
    ids = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search",
        [[["is_company", "=", True]]],
        {"limit": 1},
    )
    print("ids:", ids)
    return ids


# 先透過上面的 method 找到 record id , 再 "read"
def read_all_field():
    models = endpoint_object()
    uid = get_uid()
    # Read records ids
    ids = read_records()
    # all field
    record = models.execute_kw(db, uid, password, "res.partner", "read", [ids])
    print(record)


# 上面的 read 是看全部的 fields , 可以限定想看的 fields
def read_need_field():
    models = endpoint_object()
    uid = get_uid()
    # Read records ids
    ids = read_records()
    # need field
    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [ids],
        {"fields": ["name", "country_id", "comment"]},
    )
    print("record")
    pprint(record)


# 把 fields 的細節 show 出來
def listing_record_fields_attributes():
    models = endpoint_object()
    uid = get_uid()
    # Listing record fields attributes
    listing_record_fields = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "fields_get",
        [],
        {"attributes": ["string", "help", "type"]},
    )
    print("Listing record fields")
    pprint(listing_record_fields)


# 常用 : search 跟 read 同時做
def search_and_read():
    models = endpoint_object()
    uid = get_uid()
    # Search and read
    search_and_read = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search_read",
        [[["is_company", "=", True]]],
        {"fields": ["name", "country_id", "comment"], "limit": 5},
    )
    print("Search and read")
    pprint(search_and_read)


# create
def create_reads():
    models = endpoint_object()
    uid = get_uid()
    # Create records
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "create",
        [
            {
                "name": "New Partner_2",
            }
        ],
    )

    # read Create records
    search_and_read = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search_read",
        [[["name", "=", "New Partner_2"]]],
        {"fields": ["name"], "limit": 5},
    )
    pprint(search_and_read)


# write
def update_records():
    models = endpoint_object()
    uid = get_uid()

    # read res.partner
    search_and_read = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search_read",
        [[["name", "=", "New Partner_2"]]],
        {"fields": ["id"], "limit": 1},
    )
    my_partner_id = search_and_read[0]["id"]
    print("my_partner_id:", my_partner_id)

    # Update records
    models.execute_kw(
        db, uid, password, "res.partner", "write", [[my_partner_id], {"name": "hello"}]
    )
    # get record name after having changed it
    my_data = models.execute_kw(
        db, uid, password, "res.partner", "name_get", [[my_partner_id]]
    )
    pprint(my_data)


# unlink
def delete_record():
    # please installl sale addons
    models = endpoint_object()
    uid = get_uid()

    # read res.partner
    my_partner_id = 41

    # Delete records
    models.execute_kw(db, uid, password, "res.partner", "unlink", [[my_partner_id]])

    # check if the deleted record is still in the database
    my_data = models.execute_kw(
        db, uid, password, "res.partner", "search", [[["id", "=", my_partner_id]]]
    )
    pprint(my_data)


"""

db 關連寫法

"""
# 前置作業
# 0.安裝 sales module
# 1.create_reads() , 建立一個 res_partner "name": "New Partner_2"
# 2.update_records() , 將這位 partner 改名為 {"name": "hello"}


# 本範例的作用
# 1. 找到  {"name": "hello"} 的 partner ID
# 2. Many2one - create ，在 sales.order 中新增一筆資料
def many2one_create():
    # please installl sale addons
    models = endpoint_object()
    uid = get_uid()

    # read res.partner
    search_and_read = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search_read",
        [[["name", "=", "hello"]]],
        {"fields": ["id"], "limit": 1},
    )
    my_partner_id = search_and_read[0]["id"]
    print("my_partner_id:", my_partner_id)

    # Many2one - create
    id_ = models.execute_kw(
        db,
        uid,
        password,
        "sale.order",
        "create",
        [
            {
                "partner_id": my_partner_id,
            }
        ],
    )

    # get record name after having changed it
    # check form pgadmin4
    my_data = models.execute_kw(db, uid, password, "sale.order", "name_get", [[id_]])
    pprint(my_data)


# 本範例的作用
# 1. 找到  res_partner_id = 38
# 2. Many2many - link ，新增一筆分類 category_id = 7 name : {"en_US": "Desk Manufacturers"}
def many2many_add_record():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 7

    # res.partner
    # check form pgadmin4
    res_partner_id = 42

    # (4, id, _) links an already existing record.
    # add many2many field,
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "write",
        [[res_partner_id], {"category_id": [(4, category_id, 0)]}],
    )

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)


# 本範例的作用
# 1. 找到  res_partner_id = 38
# 2. Many2many - replace ，category_id = 5 & 6
def many2many_add_mutil_record():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_ids = [5, 7]

    # res.partner
    # check form pgadmin4
    res_partner_id = 42

    # (6, _, [ids]) replaces the list of linked records with the provided list.
    # add mutil many2many field
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "write",
        [[res_partner_id], {"category_id": [(6, 0, category_ids)]}],
    )

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)


# 本範例的作用
# 1. 修改 m2x record 內 fields 的值
# 2. 本範例中，將 category_id = 6 的 name 改為 {"name": "hello2"}
def many2many_update_record():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 6

    # res.partner
    # check form pgadmin4
    res_partner_id = 42

    # read - res_partner_id = 42
    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)

    # update many2many field value
    # (1, ID, { values }) update the linked record with id = ID
    # 將 category_id = 6 的 name 改為 {"name": "hello2"}
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "write",
        [[res_partner_id], {"category_id": [(1, category_id, {"name": "hello2"})]}],
    )

    # read res.partner.category中 category_id = 6 的 id , name
    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner.category",
        "read",
        [category_id],
        {"fields": ["id", "name"]},
    )
    print("record:", record)


# 本範例的作用
# 1. 使用 (2) 這個 delete method
# 2. 會執行 unlink and delete 那筆關連的資料
# 本範例中，會將 res_partner_id = 42 與 category_id = 6 的關連 unlink , 並且 category_id = 6 這筆資料也會不見
def many2many_delete_record_2():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 6

    # res.partner
    # check form pgadmin4
    res_partner_id = 42

    # read res_partner_id=42
    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)

    # delete many2many field.
    # 2, ID) remove and delete the linked record with id = ID
    # (calls unlink on ID, that will delete the object completely,
    # and the link to it as well)
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "write",
        [[res_partner_id], {"category_id": [(2, category_id, 0)]}],
    )

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)

    # res.partner.category
    # check form pgadmin4
    # id = 6 deleted

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner.category",
        "read",
        [category_id],
        {"fields": ["id", "name"]},
    )
    print("record:", record)


# 本範例的作用
# 1. 使用 (3) 這個 delete method
# 2. 會執行 unlink , 但不會 delete 那筆關連的資料
def many2many_delete_record_3():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 5

    # res.partner
    # check form pgadmin4
    res_partner_id = 42

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)

    # delete many2many field.
    # (3, ID) cut the link to the linked record with id = ID
    # (delete the relationship between the two objects
    # but does not delete the target object itself)
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "write",
        [[res_partner_id], {"category_id": [(3, category_id, 0)]}],
    )

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)

    # res.partner.category
    # check form pgadmin4
    # id = 7 not deleted

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner.category",
        "read",
        [category_id],
        {"fields": ["id", "name"]},
    )
    print("record:", record)


# 本範例的作用
# 1. 使用 (5) 這個 delete method
# 2. 跟 (3) 類似會執行 unlink , 而且是全部的 unlink 。 ( 不會 delete 關連的資料 )
def many2many_delete_record_5():
    models = endpoint_object()
    uid = get_uid()

    # res.partner
    # check form pgadmin4
    res_partner_id = 42

    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)

    # delete many2many field.
    # (5, 0, 0) unlink all
    # (like using (3,ID, 0) for all linked records)
    models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "write",
        [[res_partner_id], {"category_id": [(5, 0, 0)]}],
    )

    # res.partner.category
    # check form pgadmin4
    # ids not deleted
    record = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "read",
        [res_partner_id],
        {"fields": ["id", "name", "category_id"]},
    )
    print("record:", record)
