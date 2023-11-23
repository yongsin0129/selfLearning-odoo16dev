# -*- coding: utf-8 -*-

from odoo import http
from odoo.tools import html_escape, html_sanitize
from markupsafe import Markup


class QwebTutorials(http.Controller):
    @http.route('/qweb-tutorials', type='http', auth='public', website=True)
    def qweb_tutorials(self):
        """ QWEB Tutorials """

        def some_function():
            return "returning string  from a function"

        some_model = http.request.env['sale.order'].search([])
        some_model_sudo = http.request.env['sale.order'].sudo().search([])

        data = {
            'string': 'QWEB Tutorials',
            'integer': '1000',
            'some_float': 10.05,
            'boolean': True,
            'some_list': [1, 2, 3, 4, 5],
            'some_dict': {'any_key': "any_value", 'key1': 'value1'},
            'some_function': some_function(),
            'model': some_model,
            'model_sudo': some_model_sudo,
        }

        return http.request.render("qweb_tutorial.somePythonTemplate",  data)
