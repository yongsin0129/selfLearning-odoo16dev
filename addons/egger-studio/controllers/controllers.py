# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class CheckoutSkipAddressCheck(WebsiteSale):

    # 不使用 return super().checkout(**post)
    # 直接 copy 原版的 code ， 再改為裡面的內容 ( skip address check )
    # @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        _logger.info('********************** CheckoutSkipAddressCheck **************************')
        # 获取订单
        order = request.website.sale_get_order()

        # 检查重定向
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        # # 检查地址
        # if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
        #     return request.redirect('/shop/address')

        # # 检查地址
        # redirection = self.checkout_check_address(order)
        # if redirection:
        #     return redirection

        # 获取值
        values = self.checkout_values(**post)

        # 检查表达
        if post.get('express'):
            return request.redirect('/shop/confirm_order')

        # 更新值
        values.update({'website_sale_order': order})

        # Avoid useless rendering if called in ajax
        # 避免不必要的渲染
        if post.get('xhr'):
            return 'ok'
        return request.render("website_sale.checkout", values)

   # 定义确认订单函数
   # @http.route(['/shop/confirm_order'], type='http', auth="public", website=True, sitemap=False)
    def confirm_order(self, **post):
        # 获取订单
        order = request.website.sale_get_order()

        # 检查重定向
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        # 计算订单的税号
        order.order_line._compute_tax_id()
        # 保存订单id
        request.session['sale_last_order_id'] = order.id
        # 更新价格列表
        request.website.sale_get_order(update_pricelist=True)
        # 检查是否有额外的步骤
        extra_step = request.website.viewref('website_sale.extra_info_option')
        if extra_step.active:
            return request.redirect("/shop/extra_info")

        # 返回支付页面
        return request.redirect("/shop/payment")

    # @http.route('/shop/payment', type='http', auth='public', website=True, sitemap=False)
    def shop_payment(self, **post):
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        render_values = self._get_shop_payment_values(order, **post)
        render_values['only_services'] = order and order.only_services or False

        if render_values['errors']:
            render_values.pop('providers', '')
            render_values.pop('tokens', '')

        return request.render("egger-studio.payment_skipAddressCheck", render_values)

    # @http.route(['/shop/confirmation'], type='http', auth="public", website=True, sitemap=False)
    def shop_payment_confirmation(self, **post):
        """ End of checkout process controller. Confirmation is basically seing
        the status of a sale.order. State at this point :

         - should not have any context / session info: clean them
         - take a sale.order id, because we request a sale.order and are not
           session dependant anymore
        """
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            values = self._prepare_shop_payment_confirmation_values(order)
            return request.render("egger-studio.confirmation", values)
        else:
            return request.redirect('/shop')


# ********************************* 筆記 :  使用 super **********************************************


# class CheckoutSkipAddressCheck(WebsiteSale):
#     # @http.route()  沒有 path 會被警告，直接 skip 這個 function

      # 路由，定义访问路径，类型为http，认证为public，网站为True，sitemap为False
#     # @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
#     # def CheckoutSkipAddressCheck(self): 直接使用 overwrite ，所以不用覆蓋 route table

#     因為使用 overwrite , 必須注意 return 的值 !!!
      # 定义函数checkout，参数为post
#     def checkout(self, **post):
#         _logger.info('********************** CheckoutSkipAddressCheck **************************')
#         return super().checkout(**post)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# *********************************** 筆記 : 腳手架的 controller  ************************************
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
#  *********************


# ********************************* 筆記 :   **********************************************

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
