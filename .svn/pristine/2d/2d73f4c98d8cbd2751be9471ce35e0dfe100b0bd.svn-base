# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError, except_orm, UserError


class ActivityHistory(models.Model):
    _name = 'activity.history'
    _description = 'Activity History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', related='partner_id.name', readonly=True)
    therapy_record_id = fields.Many2one('therapy.record', string='Therapy Record', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='onchange')
    mail_activity_type_id = fields.Many2one('mail.activity.type', string='Mail Activity Type', track_visibility='onchange')
    type = fields.Selection([('out_of_medicine', 'Out of medicine'), ('customer_care', 'Customer care')], string='Type', track_visibility='onchange')
    object = fields.Selection([('consultant', 'Consultant'), ('customer_care', 'Customer care')], string='Object', track_visibility='onchange')
    date_deadline = fields.Date(string='Date Deadline', track_visibility='onchange')
    partner_interaction_ids = fields.One2many('partner.interaction', 'activity_history_id', string='Partner Interaction', track_visibility='onchange')
    state = fields.Selection([('new', 'New'), ('assigned', 'Assigned'), ('interacted', 'Interacted')], string='State', default='new', track_visibility='onchange')
    color = fields.Integer('Color Index', compute="_check_color", track_visibility='onchange')
    is_activity_constant = fields.Boolean(string='Is activity constant', default=False, track_visibility='onchange')
    note = fields.Text(string='Note', track_visibility='onchange')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return {
            'value': {
                'therapy_record_id': False
            }
        }

    def _check_color(self):
        for record in self:
            color = 0
            if record.state == 'new':
                color = 1
            elif record.state == 'assigned':
                color = 3
            elif record.state == 'interacted':
                color = 4
            else:
                color = 5
            record.color = color

    @api.multi
    def action_assign(self):
        for activity in self:
            if not activity.user_id:
                raise UserError(_("Người nhận chưa được chọn để giao!"))
            if not activity.date_deadline:
                raise UserError(_("Chưa có lịch giao!"))
            activity.env['mail.activity'].create({
                'activity_type_id': activity.mail_activity_type_id.id,
                'res_model_id': activity.env.ref('izi_crm_interaction.model_activity_history').id,
                'res_model': activity.env.ref('izi_crm_interaction.model_activity_history').name,
                'res_id': activity.id,
                'user_id': activity.user_id.id,
                'date_deadline': activity.date_deadline,
            })
            activity.state = 'assigned'

    def action_create_interaction(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({
            'default_method_interaction': 'proactive',
            'default_partner_id': self.partner_id.id,
            'default_activity_history_id': self.id,
            'default_user_id': self.user_id.id,
            'default_expected_date': self.date_deadline,
            'default_mail_activity_type_id': self.mail_activity_type_id.id,
            'default_type': self.type,
            'default_object': self.object,
            'default_therapy_record_id': self.therapy_record_id.id
        })
        view = self.env.ref('izi_crm_interaction.partner_interaction_form_view')
        return {
            'name': _('Partner Interaction'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'partner.interaction',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': '',
            'context': ctx,
        }


class ActivityHistoryAssign(models.TransientModel):
    _name = 'activity.history.assign'

    user_id = fields.Many2one('res.users', string='User')

    @api.multi
    def assign_activity(self):
        for activity in self:
            if not activity.user_id:
                raise UserError(_('Bạn chưa chọn nhân viên thực hiện'))
            activity_ids = activity._context.get('active_ids')
            for activity_id in activity_ids:
                activity_history = activity.env['activity.history'].search([('id', '=', activity_id)])
                if activity_history.user_id:
                    raise UserError(_('Nhắc lịch cho %s đã có nhân viên thực hiện') % activity_history.partner_id.name)
                activity_history.update({
                    'user_id': activity.user_id.id,
                })
                activity_history.action_assign()