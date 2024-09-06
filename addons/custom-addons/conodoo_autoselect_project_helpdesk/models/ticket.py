from odoo import models, api


class Ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.onchange("partner_id")
    def _onchange_partner(self):
        andromat_project_id = self.partner_id.andromat_project_id
        if self.partner_id and andromat_project_id:
            self.project_id = andromat_project_id
            # self.task_id = self.partner_id.andromat_task_id
        else:
            self.project_id = None
            # self.task_id = None

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partnerId = vals.get("partner_id")
            if partnerId and not vals.get('project_id'):
                partner = self.env['res.partner'].browse(partnerId)
                if partner and partner.andromat_project_id:
                    vals['project_id'] = partner.andromat_project_id.id

        return super().create(vals_list)
