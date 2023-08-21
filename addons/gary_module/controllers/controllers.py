# -*- coding: utf-8 -*-
# from odoo import http


# class GaryModule(http.Controller):
#     @http.route('/gary_module/gary_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gary_module/gary_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gary_module.listing', {
#             'root': '/gary_module/gary_module',
#             'objects': http.request.env['gary_module.gary_module'].search([]),
#         })

#     @http.route('/gary_module/gary_module/objects/<model("gary_module.gary_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gary_module.object', {
#             'object': obj
#         })
