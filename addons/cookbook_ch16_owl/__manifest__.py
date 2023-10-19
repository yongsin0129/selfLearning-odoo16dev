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
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/library_book.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'cookbook_ch16_owl/static/src/js/component.js',
        ],
    },
    # 'demo': ['demo.xml'],
}
