# -*- coding: utf-8 -*-
# from odoo import http


# class TwturbiksInheritance(http.Controller):
#     @http.route('/twturbiks_inheritance/twturbiks_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/twturbiks_inheritance/twturbiks_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('twturbiks_inheritance.listing', {
#             'root': '/twturbiks_inheritance/twturbiks_inheritance',
#             'objects': http.request.env['twturbiks_inheritance.twturbiks_inheritance'].search([]),
#         })

#     @http.route('/twturbiks_inheritance/twturbiks_inheritance/objects/<model("twturbiks_inheritance.twturbiks_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('twturbiks_inheritance.object', {
#             'object': obj
#         })
