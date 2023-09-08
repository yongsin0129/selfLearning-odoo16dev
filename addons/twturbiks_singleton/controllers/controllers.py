# -*- coding: utf-8 -*-
# from odoo import http


# class TwturbiksSingleton(http.Controller):
#     @http.route('/twturbiks_singleton/twturbiks_singleton', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/twturbiks_singleton/twturbiks_singleton/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('twturbiks_singleton.listing', {
#             'root': '/twturbiks_singleton/twturbiks_singleton',
#             'objects': http.request.env['twturbiks_singleton.twturbiks_singleton'].search([]),
#         })

#     @http.route('/twturbiks_singleton/twturbiks_singleton/objects/<model("twturbiks_singleton.twturbiks_singleton"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('twturbiks_singleton.object', {
#             'object': obj
#         })
