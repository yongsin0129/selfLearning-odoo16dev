# pylint: skip-file
{
    'name': "My library",
    'summary': "轻松管理图书",
    'description': """
Manage Library
==============
Description related to library.
""",
    'author': "Alan Hou",
    'website': "https://alanhou.org",
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['base'],
    "license": "LGPL-3",
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/library_book.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'owl2-learning/static/src/js/component.js',
        ],
    },
    # 'demo': ['demo.xml'],
}
