from odoo import api, fields, models


class Produk(models.Model):
    _name = 'toko.produk'
    _description = 'New Description'

    id_produk = fields.Char(string='ID Produk',
                            readonly=True,
                            required=True,
                            copy=False,
                            default='New')
    name = fields.Char(string='Nama Produk', required=True)
    kuantitas = fields.Integer(
        string='Kuantitas', readonly=True)
    harga_jual = fields.Integer(string='Harga Jual', required=True)
    harga_beli = fields.Integer(string='Harga Beli', required=True)
    deskripsi = fields.Text(string='Deskripsi', required=True)

    @api.model
    def create(self, vals):
        if vals.get('id_produk', 'New') == 'New':
            vals['id_produk'] = self.env['ir.sequence'].next_by_code(
                'toko.produk.sequence') or 'New'
        result = super(Produk, self).create(vals)
        return result

    kuantitas_total = fields.Integer(
        string='Kuantitas Total', compute='_compute_ktotal')

    @api.depends('kuantitas')
    def _compute_ktotal(self):
        for record in self:
            record.kuantitas_total = record.kuantitas
