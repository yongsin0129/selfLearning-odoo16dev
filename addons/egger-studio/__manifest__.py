# -*- coding: utf-8 -*-
{
    "name": "egger studio",
    "summary": """
        專為艾格工作室客製化的模組""",
    "description": """
        主要功能
        1. eshop skip address check
        2. specific translation
    """,
    "author": "許永昕",
    "website": "https://www.blog.yongsin.site/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Administration",
    "version": "16.0.0.1",
    "license": "LGPL-3",

    # any module necessary for this one to work correctly
    "depends": ["base", "web", "website_sale"],

    # always loaded
    "data": [
        "security/ir.model.access.csv",

        "views/payment_skipAddressCheck.xml"
    ],

    # only loaded in demonstration mode
    "demo": [

    ],
}
