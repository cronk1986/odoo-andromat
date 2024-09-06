from odoo import models, fields, api

class ContractTemplate(models.Model):
    _inherit = 'contract.template'

    invoice_type = fields.Selection(
        [
            ('bagHours', 'Bolsa de horas')
        ],
        string="Tipo de factura",
        default=None,
    )