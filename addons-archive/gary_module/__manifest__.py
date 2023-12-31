# -*- coding: utf-8 -*-
{
    "name": "gary_module",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
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
        "security/res_student_group.xml",
        "security/ir.model.access.csv",

        "views/views.xml",
        "views/templates.xml",
        "views/menu.xml",

        "reports/res_student_report.xml",

        "data/res_student.xml",
        "data/res.student.csv",
        "data/student_paperformat.xml",
        "data/res_student_cron.xml",

        "views/res_company_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
