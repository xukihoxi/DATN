# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError, MissingError


class TherapyBodyMeasure(models.Model):
    _name = 'therapy.body.measure'

    name = fields.Char(string='Name')
    upper_waist = fields.Float(string='Upper of Waist')  # eo trên
    lower_waist = fields.Float(string='Lower of Waist')  # eo dưới
    middle_waist = fields.Float(string='Middle Waist')  # eo giữa
    arm = fields.Float(string='Arm')  # bắp tay
    right_upper_thighs = fields.Float(string='Right Upper Thigh')  # bắp đùi phải trên
    left_upper_thighs = fields.Float(string='Left Upper Thigh')  # bắp đùi trái trên
    right_lower_thighs = fields.Float(string='Right lower Thigh')  # bắp đùi phải dưới
    left_lower_thighs = fields.Float(string='Left lower Thigh')  # bắp đùi trái dưới
    flank = fields.Float(string='Flank')  # hông
    armpit = fields.Float(string='Armpit')  # Nách
    lats = fields.Float(string='Lats')  # xoài
    back = fields.Float(string='Back')  # lưng
    weight = fields.Float(string='Weight')  # cân nặng
    high = fields.Float(string='High')  # chiều cao
    upper_abdomen = fields.Float(string='Upper Abdomen')  # bụng trên
    middle_abdomen = fields.Float(string='Middle Abdomen')  # bụng giữa
    abdomen = fields.Float(string='Abdomen')  # bụng dưới
    right_upper_calf = fields.Float(string='Right Upper Calf')  # bắp chan phải trên
    left_upper_calf = fields.Float(string='Left Upper Calf')  # bắp chan phải trên
    right_lower_calf = fields.Float(string='Right Lower Calf')  # bắp chan phải trên
    left_lower_calf = fields.Float(string='Left Lower Calf')  # bắp chan phải trên
    measurement_time = fields.Datetime(string='Measurement  time')  # Thời gian đo
    technician = fields.Many2one('hr.employee', string='Technician')  # Kỹ thuật viên
    note = fields.Text(string='Note')
    therapy_record_id = fields.Many2one('therapy.record', string='Therapy Record')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if vals['therapy_record_id']:
                partner_id = self.env['therapy.record'].search([('id', '=', vals['therapy_record_id'])]).partner_id.id
                array_date = vals['measurement_time'].split(' ')[0].split('-')
                measurement_time = str(array_date[2]) + str(array_date[1]) + str(array_date[0])
                vals['name'] = 'CSGB_' + str(partner_id) + '_' + measurement_time
        return super(TherapyBodyMeasure, self).create(vals)