from odoo import models, fields, api

class Contact(models.Model):
    _inherit = 'res.partner'

    #andromat_project_id = fields.Many2one(comodel_name='project.project', string='Proyecto por defecto', required=True)
