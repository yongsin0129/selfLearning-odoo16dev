# -*- coding: utf-8 -*-
# from odoo import http


# class TwturbiksHierarchy(http.Controller):
#     @http.route('/twturbiks_hierarchy/twturbiks_hierarchy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/twturbiks_hierarchy/twturbiks_hierarchy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('twturbiks_hierarchy.listing', {
#             'root': '/twturbiks_hierarchy/twturbiks_hierarchy',
#             'objects': http.request.env['twturbiks_hierarchy.twturbiks_hierarchy'].search([]),
#         })

#     @http.route('/twturbiks_hierarchy/twturbiks_hierarchy/objects/<model("twturbiks_hierarchy.twturbiks_hierarchy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('twturbiks_hierarchy.object', {
#             'object': obj
#         })
