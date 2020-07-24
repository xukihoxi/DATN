# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError, except_orm, UserError

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.model
    def default_get(self, fields):
        res = super(MailActivity, self).default_get(fields)
        res['user_id'] = self._context.get('user_id')
        return res