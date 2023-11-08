# -*- coding: utf-8 -*-
# from odoo import http


# class Func01Uimock(http.Controller):
#     @http.route('/func01__uimock/func01__uimock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/func01__uimock/func01__uimock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('func01__uimock.listing', {
#             'root': '/func01__uimock/func01__uimock',
#             'objects': http.request.env['func01__uimock.func01__uimock'].search([]),
#         })

#     @http.route('/func01__uimock/func01__uimock/objects/<model("func01__uimock.func01__uimock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('func01__uimock.object', {
#             'object': obj
#         })
