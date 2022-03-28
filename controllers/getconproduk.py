from odoo import http, fields, models
from odoo.http import request
import json


class ProdukCon(http.Controller):
    @http.route(['/produk', '/produk/<int:idnya>'], auth='public', methods=['GET'], csrf=True)
    def getProduk(self, idnya=None, **kwargs):
        value = []
        if not idnya:
            produk = request.env['toko.produk'].search([])
            for k in produk:
                value.append({"id": k.id,
                              "nama_produk": k.name,
                              "kuantitas": k.kuantitas,
                              "harga_jual": k.harga_jual,
                              "harga_beli": k.harga_beli,
                              "deskripsi": k.deskripsi})
            return json.dumps(value)
        else:
            produkid = request.env['toko.produk'].search(
                [('id', '=', idnya)])
            for k in produkid:
                value.append({"id": k.id,
                              "nama_produk": k.name,
                              "kuantitas": k.kuantitas,
                              "harga_jual": k.harga_jual,
                              "harga_beli": k.harga_beli,
                              "deskripsi": k.deskripsi})
            return json.dumps(value)

    @http.route('/createproduk', auth='user', type='json', methods=['POST'])
    def createProduk(self, **kw):
        if request.jsonrequest:
            if kw['name']:
                vals = {
                    'name': kw['name'],
                    'kuantitas': kw['kuantitas'],
                    'harga_jual': kw['harga_jual'],
                    'harga_beli': kw['harga_beli'],
                    'deskripsi': kw['deskripsi'],
                }
                produkbaru = request.env['toko.produk'].create(vals)
                args = {'success': True, 'ID': produkbaru.id}
                return args
