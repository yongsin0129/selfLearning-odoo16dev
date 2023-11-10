# -*- coding: utf-8 -*-
# pylint: skip-file
{
    'name': "func01_UIMock",

    'summary': """
        func first example for UI imitation""",

    'description': """
        func first example for UI imitation , We choose a template form theme forest and try to make a mock up
    """,

    'author': "yongsin0129",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Themes',
    'version': '17.0.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],

    # assets
    'assets': {
        'web.assets_backend': [

            # webclient
            'func01_uimock/static/src/webclient/webclient.js',
            'func01_uimock/static/src/webclient/webclient.scss',
            'func01_uimock/static/src/webclient/webclient.xml',

            # navbar
            'func01_uimock/static/src/navbar/navbar.js',
            'func01_uimock/static/src/navbar/navbar.scss',
            'func01_uimock/static/src/navbar/navbar.xml',

        ]
    }
}
