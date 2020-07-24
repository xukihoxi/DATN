from odoo import api, fields, models, _
from odoo.exceptions import except_orm, UserError


class IziCrmLead(models.Model):
    _inherit = 'crm.stage'

    x_code = fields.Char(string='Code')

    _sql_constraints = {
        ('unique_x_code', 'unique(x_code)', ' Mã phải là duy nhất!')
    }

    @api.model_cr
    def init(self):
        if not self.env['crm.stage'].search([('x_code', '=', 'lead')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Lead'),
                'x_code': 'lead',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'reference')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Reference'),
                'x_code': 'reference',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'reference2')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Reference2'),
                'x_code': 'reference2',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'opportunity')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Opportunity'),
                'x_code': 'opportunity',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'to_shop')], limit=1):
            self.env['crm.stage'].create({
                'name': _('To shop'),
                'x_code': 'to_shop',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'confirm')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Confirm'),
                'x_code': 'confirm',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'won')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Won'),
                'x_code': 'won',
                'probability': 0
            })
        if not self.env['crm.stage'].search([('x_code', '=', 'lose')], limit=1):
            self.env['crm.stage'].create({
                'name': _('Lose'),
                'x_code': 'lose',
                'probability': 0
            })