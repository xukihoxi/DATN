# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError, MissingError
import time


class TherapyRecord(models.Model):
    _name = 'therapy.record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Therapy Record', related='categ_id.name', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='onchange')
    partner_code = fields.Char(string='Code', related='partner_id.x_code', readonly=True)
    partner_birthday = fields.Date(string='Birthday', related='partner_id.x_birthday', readonly=True)
    partner_level_age_id = fields.Many2one('level.age', related='partner_id.x_level_age_id', string='Level Age', readonly=True)
    partner_street = fields.Char(string='Street', related='partner_id.street', readonly=True)
    partner_state_id = fields.Many2one('res.country.state', string='State', related='partner_id.state_id', readonly=True)
    partner_country_id = fields.Many2one('res.country', string='Country', related='partner_id.country_id', readonly=True)
    partner_phone = fields.Char(string='Phone', related='partner_id.phone', readonly=True)
    crm_lead_tag_ids = fields.Many2many('crm.lead.tag', string='Tag', related='partner_id.x_crm_lead_tag_ids', readonly=True)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange')
    categ_id = fields.Many2one('product.category', string='Category')
    note = fields.Text('Warning Information')  # thông tin lưu ý
    therapy_body_measure_ids = fields.One2many('therapy.body.measure', 'therapy_record_id', 'Therapy body measure')
    therapy_prescription_ids = fields.One2many('therapy.prescription', 'therapy_record_id', string='Therapy prescription')  # phiếu chỉ định
    therapy_record_product_ids = fields.One2many('therapy.record.product', 'therapy_record_id', string='Therapy record product')  # tổng sản phẩm, dịch vụ tồn
    therapy_prescription_return_product_line_ids = fields.One2many('therapy.prescription.return.product.line', 'therapy_record_id', string='Therapy Prescription Return Product')
    is_inventory = fields.Boolean(string='Is Inventory', default=False)

    @api.model
    def default_get(self, fields):
        res = super(TherapyRecord, self).default_get(fields)
        res['user_id'] = self._context.get('uid')
        return res

    def create_prescription(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        view = self.env.ref('izi_therapy_record.izi_view_therapy_prescription_form')
        return {
            'name': _('Therapy Prescription'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'therapy.prescription',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': '',
            'context': ctx,
        }