from odoo import models, fields, api


class Account(models.Model):
    _inherit = 'account.move'

    invoice_type = fields.Selection(
        [
            ('bagHours', 'Bolsa de horas')
        ],
        string="Tipo de factura",
        default=None
    )

    helpdesk_ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket',
        inverse_name='invoice_id',
        string='Tickets'
    )

    ticket_count = fields.Integer(
        string='Total Tickets',
        compute='_compute_ticket_count',
        store=True
    )

    ticket_delivered_time = fields.Float(
        string='Delivered time',
        compute='_compute_ticket_delivery_time',
        store=True
    )

    ticket_delivered_time_formatted = fields.Char(
        string='Delivered time formatter',
        compute='_compute_ticket_delivered_time_formatted',
        store=True  # Para permitir su uso en vistas tree
    )

    smart_button_ticket_text = fields.Char(
        string="Smart Button Ticket Text",
        compute='_compute_smart_button_ticket_text'
    )

    planned_total_hours = fields.Float(
        string='Total Horas',
        compute='_compute_total_hours',
        store=True
    )

    partner_nif = fields.Char(
        string='Partner NIF',
        compute='_compute_partner_nif',
        store=False
    )

    @api.depends('partner_id.vat')
    def _compute_partner_nif(self):
        for record in self:
            partner = record.partner_id
            if partner:
                record.partner_nif = partner.vat

    @api.depends('helpdesk_ticket_ids.total_hours')
    def _compute_ticket_delivery_time(self):
        for record in self:
            computed_time = sum(ticket.total_hours for ticket in record.helpdesk_ticket_ids)
            record.ticket_delivered_time = computed_time

    @api.depends('ticket_delivered_time', 'planned_total_hours')
    def _compute_ticket_delivered_time_formatted(self):
        for record in self:
            if record.invoice_type == 'bagHours':
                record.ticket_delivered_time_formatted = f"{self._float_to_time_str(record.ticket_delivered_time)} / {self._float_to_time_str(record.planned_total_hours)}"

    def _float_to_time_str(self, hours_float):
        hours = int(hours_float)
        minutes = int((hours_float - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    @api.depends('helpdesk_ticket_ids')
    def _compute_ticket_count(self):
        for record in self:
            record.ticket_count = len(record.helpdesk_ticket_ids)

    @api.depends('ticket_count')
    def _compute_smart_button_ticket_text(self):
        for record in self:
            record.smart_button_ticket_text = 'Ticket' if record.ticket_count == 1 else 'Tickets'

    @api.depends('invoice_line_ids', 'invoice_line_ids.quantity', 'invoice_line_ids.product_uom_id')
    def _compute_total_hours(self):
        for record in self:
            total_hours = sum(line.quantity for line in record.invoice_line_ids if
                              line.product_uom_id.name == 'Hours' or line.product_uom_id.name == 'Horas')
            record.planned_total_hours = total_hours

    def action_show_ticket_count(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Tickets',
                'view_mode': 'tree,form',
                'res_model': 'helpdesk.ticket',
                'views': [
                    (self.env.ref('helpdesk_mgmt.ticket_view_tree').id, 'tree'),
                    (self.env.ref('helpdesk_mgmt.ticket_view_form').id, 'form'),
                ],
                'target': 'current',
                'domain': [('invoice_id', '=', record.id)],
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            update_vals = {}  # Diccionario temporal para almacenar cambios

            for field, value in vals.items():
                if field == 'invoice_line_ids':
                    for line_command in value:
                        if isinstance(line_command, tuple) and line_command[0] == 0:
                            line_vals = line_command[2]
                            contract_line_id = line_vals.get('contract_line_id')
                            if contract_line_id:
                                contract_line = self.env['contract.line'].browse(contract_line_id)
                                if contract_line.exists():
                                    contract = contract_line.contract_id
                                    contract_template = contract.contract_template_id
                                    if contract_template and contract_template.invoice_type == 'bagHours':
                                        update_vals['invoice_type'] = 'bagHours'
                                    # if contract.invoice_confirmed:
                                    #     update_vals['state'] = 'posted'
            vals.update(update_vals)
        invoices = super().create(vals_list)

        for invoice in invoices:
            # Verifica si hay líneas de factura y si alguna está vinculada a un contract.line
            contract_line = None
            for line in invoice.invoice_line_ids:
                if line.contract_line_id:
                    contract_line = line.contract_line_id
                    break  # Asumiendo que solo necesitas verificar una línea

            if contract_line:
                contract = contract_line.contract_id
                if contract and contract.invoice_confirmed and invoice.state == 'draft':
                    invoice.action_post()

        return invoices
