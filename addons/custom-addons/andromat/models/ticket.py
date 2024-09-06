from odoo import models, fields, api


class Ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Factura',
        domain=lambda self: self._get_invoice_domain()
    )

    invoice_confirmed = fields.Boolean(
        string='Factura Confirmada',
        compute='_compute_invoice_confirmed',
        store=False
    )

    @api.depends('invoice_id.state')
    def _compute_invoice_confirmed(self):
        for ticket in self:
            # Verifica el estado de la factura y actualiza el valor de invoice_confirmed
            if ticket.invoice_id:
                ticket.invoice_confirmed = ticket.invoice_id.payment_state == 'paid'
            else:
                ticket.invoice_confirmed = False

    @api.onchange('partner_id')
    def _onchange_partner(self):
        # Limpia el campo invoice_id cuando cambia partner_id
        if self.partner_id:
            invoices = self._get_invoices()
            if invoices:
                self.invoice_id = invoices[0].id
            else:
                self.invoice_id = None
        else:
            self.invoice_id = None

        # Actualiza el dominio del campo invoice_id
        return {
            'domain': {'invoice_id': self._get_invoice_domain()}
        }

    def _get_invoice_domain(self):
        # Devuelve el dominio para el campo invoice_id basado en el partner_id
        # Obtén la lista de facturas ordenadas
        invoices = self._get_invoices()

        if not invoices:
            return [('id', '=', 0)]  # No mostrar ningún registro

        domain = self._base_invoice_domain()
        domain.append(('id', 'in', invoices.ids))
        return domain

    def _get_invoices(self):
        # Obtiene las facturas filtradas por partner_id y ordenadas en descendente por fecha de creación, limitado a 1 resultado
        domain = self._base_invoice_domain()
        return self.env['account.move'].search(domain, order='create_date desc', limit=8)

    def _base_invoice_domain(self):
        # Devuelve el dominio base para facturas
        return [
            ('invoice_type', '=', 'bagHours'),
            ('state', '=', 'posted'),
            ('partner_id', '=', self.partner_id.id)
        ]

    @api.model_create_multi
    def create(self, vals_list):
        domain = self._base_invoice_domain()
        for vals in vals_list:
            partner_id = vals.get("partner_id")
            if partner_id and not vals.get('invoice_id'):
                domain[2] = ('partner_id', '=', partner_id)
                invoices = self.env['account.move'].search(domain, order='create_date desc', limit=1)
                if invoices:
                    vals['invoice_id'] = invoices[0].id

        return super().create(vals_list)

