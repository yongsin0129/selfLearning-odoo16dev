# -*- coding: utf-8 -*-
# from odoo import http


# class SuSirModule(http.Controller):
#     @http.route('/su_sir_module/su_sir_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/su_sir_module/su_sir_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('su_sir_module.listing', {
#             'root': '/su_sir_module/su_sir_module',
#             'objects': http.request.env['su_sir_module.su_sir_module'].search([]),
#         })

#     @http.route('/su_sir_module/su_sir_module/objects/<model("su_sir_module.su_sir_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('su_sir_module.object', {
#             'object': obj
#         })
