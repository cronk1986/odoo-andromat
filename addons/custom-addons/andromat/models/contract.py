from odoo import models, fields, api


class AndromatContract(models.Model):
    _inherit = 'contract.contract'

    invoice_type = fields.Selection(
        [
            ('bagHours', 'Bolsa de horas')
        ],
        string="Tipo de factura",
        default=None,
    )

    invoice_confirmed = fields.Boolean(
        string='Confirmar factura',
        store=True,
        default=False
    )
