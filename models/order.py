from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'toko.order'
    _description = 'New Description'

    name = fields.Char(
        string='ID Order',
        readonly=True,
        required=True,
        copy=False,
        default='New')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'toko.order.sequence') or 'New'
        result = super(Order, self).create(vals)
        return result

    pelanggan = fields.Many2one(
        comodel_name='res.partner',
        string='Pelanggan')

    nama_pelanggan = fields.Char(
        string='Nama Pelanggan',
        compute='_compute_pelanggan')

    @api.depends('pelanggan')
    def _compute_pelanggan(self):
        for record in self:
            record.nama_pelanggan = record.res_partner

    tanggal_pesan = fields.Datetime(
        string='Tanggal Pemesanan',
        default=fields.Datetime.now(),
        readonly=True)

    orderproduk_ids = fields.One2many(
        comodel_name='toko.orderprodukdetail',
        inverse_name='order_id',
        string='Order')

    total = fields.Integer(
        compute='_compute_total',
        string='Total',
        store=True)

    @api.depends('orderproduk_ids')
    def _compute_total_payment(self):
        for record in self:
            record.total = sum(self.env['toko.orderprodukdetail'].search(
                [('order_id', '=', record.id)]).mapped('total_harga'))


class OrderProdukDetail(models.Model):
    _name = 'toko.orderprodukdetail'
    _description = 'New Description'

    order_id = fields.Many2one(
        comodel_name='toko.order',
        string='Order')

    produk_id = fields.Many2one(
        comodel_name='toko.produk',
        string='Produk')

    name = fields.Char(string='Name')

    kuantitas = fields.Integer(string='Qty')

    @api.constrains('kuantitas')
    def _check_stok(self):
        for record in self:
            bahan = self.env['toko.produk'].search(
                [('kuantitas', '<', record.kuantitas), ('id', '=', record.id)])
            if bahan:
                raise ValidationError("Stok produk yang dipilih tidak cukup.")

    kuantitas_tersedia = fields.Integer(
        string='Tersedia',
        compute="_compute_harga")

    harga = fields.Integer(
        string='Harga per Unit',
        compute="_compute_harga")

    @api.depends('produk_id')
    def _compute_harga(self):
        for record in self:
            record.harga = record.produk_id.harga_jual
            record.kuantitas_tersedia = record.produk_id.kuantitas

    total_harga = fields.Integer(
        string='Total Harga',
        compute='_compute_total_harga')

    @api.depends('harga', 'kuantitas')
    def _compute_total_harga(self):
        for record in self:
            record.total_harga = record.harga * record.kuantitas

    @api.model
    def create(self, vals):
        record = super(OrderProdukDetail, self).create(vals)
        if record.kuantitas:
            self.env['toko.produk'].search([('id', '=', record.produk_id.id)]).write(
                {'kuantitas': record.produk_id.kuantitas - record.kuantitas})
            return record
