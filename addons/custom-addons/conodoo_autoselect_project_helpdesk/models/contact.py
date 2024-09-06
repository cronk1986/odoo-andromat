from odoo import models, fields, api

class Contact(models.Model):
    _inherit = 'res.partner'

    andromat_project_id = fields.Many2one(comodel_name='project.project', string='Proyecto por defecto', required=True)
    #andromat_task_id = fields.Many2one(
    #    comodel_name='project.task',
    #    string='Tarea por defecto',
    #    domain="[('project_id','=',andromat_project_id)]"
    #)

    #@api.onchange('andromat_project_id')
    #def onchange_andromat_project_id(self):
    #    self.andromat_task_id = None
    #    return {'domain': {'andromat_task_id': [('project_id', '=', self.andromat_project_id.id)]}}
    #    return {'domain': {'andromat_task_id': [('project_id', '=', self.andromat_project_id.id)]}}