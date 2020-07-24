# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError, MissingError
import json


class TherapyPrescription(models.Model):
    _inherit = 'therapy.prescription'

    activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type')

    @api.model_cr
    def init(self):
        date_synchronize = self.env['ir.config_parameter'].search([('key', '=', 'Remind.Medicine')])
        if not date_synchronize:
            arr = {
                'date_deadline': 3,
                'activity_type_id': 2,
            }
            date_synchronize.set_param('Remind.Medicine', arr)