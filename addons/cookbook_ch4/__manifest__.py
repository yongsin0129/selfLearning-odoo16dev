# -*- coding: utf-8 -*-
{
    "name": "cookbook_ch4",
    "summary": "轻松管理图书",
    "description": """
Manage Library
==============
Description related to library.
""",
    "author": "syu yong sin",
    "website": "https://blog.yongsin.site",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/library_book.xml",
        "views/library_book_categ.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # "demo/demo.xml",
    ],
}
