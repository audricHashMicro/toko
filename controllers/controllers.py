# -*- coding: utf-8 -*-
# from odoo import http


# class Toko(http.Controller):
#     @http.route('/toko/toko/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/toko/toko/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('toko.listing', {
#             'root': '/toko/toko',
#             'objects': http.request.env['toko.toko'].search([]),
#         })

#     @http.route('/toko/toko/objects/<model("toko.toko"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('toko.object', {
#             'object': obj
#         })
