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

        some_model = http.request.env['sale.order'].sudo().search([])  # 不加 sudo ，則 public 無法訪問這個 model
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

            'html': '<h5>This is an HTML value! 傳參數無處理 </h5> Added by attacker <script>alert("Do something!!")</script>',

            'html_escape': '<h5>This is an HTML value! 傳參數使用 html_escape() 處理 </h5> %s'
                           % html_escape('Added by attacker <script>alert("Do something!!")</script>'),

            'html_sanitize': '<h5>This is an HTML value! 傳參數使用 html_sanitize() 處理</h5> %s'
                           % html_sanitize('Added by attacker <script>alert("Do something!!")</script>'),

            'markup': Markup('<h5>This is an HTML value! 傳參數使用 Markup() 處理</h5> %s')
                      % 'Added by attacker <script>alert("Do something!!")</script>',

            'description1': '直接用 t-out=" <h5> title </h5> " 會出現錯誤 ，需要 t-out="variable" , 變數內放 HTML 才可行'
        }

        return http.request.render("qweb_tutorial.somePythonTemplate",  data)
