# -*- coding: utf-8 -*-
from odoo import http


class TwturbiksFirstDemo(http.Controller):
    # user 表示需要登入才可以使用這個 route
    @http.route("/demo/odoo", auth="user")
    def list2(self, **kwargs):
        obj = http.request.env["twturbiks_first_demo.twturbiks_first_demo"]
        objs = obj.search([])
        return http.request.render(
            "twturbiks_first_demo.twturbiks_first_demo_template", {"objs": objs}
        )

    @http.route("/twturbiks_first_demo/twturbiks_first_demo", auth="public")
    def index(self, **kw):
        return "Hello, world"

    @http.route("/twturbiks_first_demo/twturbiks_first_demo/objects", auth="public")
    def list(self, **kw):
        return http.request.render(
            "twturbiks_first_demo.listing",
            {
                "root": "/twturbiks_first_demo/twturbiks_first_demo",
                "objects": http.request.env[
                    "twturbiks_first_demo.twturbiks_first_demo"
                ].search([]),
            },
        )

    @http.route(
        '/twturbiks_first_demo/twturbiks_first_demo/objects/<model("twturbiks_first_demo.twturbiks_first_demo"):obj>',
        auth="public",
    )
    def object(self, obj, **kw):
        return http.request.render("twturbiks_first_demo.object", {"object": obj})
