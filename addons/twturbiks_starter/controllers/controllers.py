# -*- coding: utf-8 -*-
from odoo import http


class TwturbiksStarter(http.Controller):
    @http.route("/twturbiks_starter/twturbiks_starter", auth="public")
    def index(self, **kw):
        return "Hello, world"

    @http.route("/twturbiks_starter/twturbiks_starter/objects", auth="public")
    def list(self, **kw):
        return http.request.render(
            "twturbiks_starter.listing",
            {
                "root": "/twturbiks_starter/twturbiks_starter",
                "objects": http.request.env["twturbiks_starter.main"].search([]),
            },
        )

    @http.route(
        '/twturbiks_starter/twturbiks_starter/objects/<model("twturbiks_starter.main"):obj>',
        auth="public",
    )
    def object(self, obj, **kw):
        return http.request.render("twturbiks_starter.object", {"object": obj})
