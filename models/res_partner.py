from email.policy import default
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    is_pegawainya = fields.Boolean(string='Pegawai', default=False)
    is_pelanggannya = fields.Boolean(string='Pelanggan', default=False)
    is_penjualnya = fields.Boolean(string='Penjual', default=False)
