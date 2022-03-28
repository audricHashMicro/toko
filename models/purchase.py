from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class Purchase(models.Model):
    _name = 'toko.purchase'
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
                'toko.purchase.sequence') or 'New'
        result = super(Purchase, self).create(vals)
        return result

    penjual = fields.Many2one(
        comodel_name='res.partner',
        string='Penjual')

    nama_penjual = fields.Char(
        string='Nama Penjual',
        compute='_compute_penjual')

    @api.depends('penjual')
    def _compute_penjual(self):
        for record in self:
            record.nama_penjual = record.res_partner

    tanggal_pesan = fields.Datetime(
        string='Tanggal Pemesanan',
        default=datetime.now(),
        readonly=True)

    tanggal_bayar = fields.Datetime(
        string='Tanggal Pembayaran',
        readonly=True)

    tanggal_diterima = fields.Datetime(
        string='Tanggal Penerimaan',
        readonly=True)

    tanggal_selesai = fields.Datetime(
        string='Tanggal Selesai',
        readonly=True)

    orderpurchase_ids = fields.One2many(
        comodel_name='toko.orderpurchasedetail',
        inverse_name='order_id',
        string='Order')

    total = fields.Integer(
        compute='_compute_total',
        string='Total',
        store=True)

    @api.depends('orderpurchase_ids')
    def _compute_total(self):
        for record in self:
            record.total = sum(self.env['toko.orderpurchasedetail'].search(
                [('order_id', '=', record.id)]).mapped('total_harga'))

    state = fields.Selection([
        ('pesan', 'Terpesan'),
        ('bayar', 'Terbayar'),
        ('terima', 'Di terima'),
        ('batal', 'Pesanan Batal'),
        ('selesai', 'Pesanan Selesai')], string='State', default="pesan")

    def action_bayar(self):
        self.state = 'bayar'
        self.tanggal_bayar = datetime.now()

    def action_terima(self):
        self.state = 'terima'
        self.tanggal_diterima = datetime.now()

    def action_selesai(self):
        self.state = 'selesai'
        self.tanggal_selesai = datetime.now()

    def action_batal(self):
        self.state = 'batal'


class OrderPurchaseDetail(models.Model):
    _name = 'toko.orderpurchasedetail'
    _description = 'New Description'

    order_id = fields.Many2one(
        comodel_name='toko.purchase',
        string='Order')

    produk_id = fields.Many2one(
        comodel_name='toko.produk',
        string='Produk')

    name = fields.Char(string='Name')

    kuantitas = fields.Integer(string='Qty')

    kuantitas_tersedia = fields.Integer(
        string='Tersedia',
        compute="_compute_harga")

    harga = fields.Integer(
        string='Harga per Unit',
        compute="_compute_harga")

    @api.depends('produk_id')
    def _compute_harga(self):
        for record in self:
            record.harga = record.produk_id.harga_beli
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
        record = super(OrderPurchaseDetail, self).create(vals)
        if record.kuantitas:
            self.env['toko.produk'].search([('id', '=', record.produk_id.id)]).write(
                {'kuantitas': record.produk_id.kuantitas + record.kuantitas})
            self.env['toko.produk'].search([('id', '=', record.produk_id.id)]).write(
                {'kuantitas_total': record.produk_id.kuantitas_total + record.kuantitas})
            return record
