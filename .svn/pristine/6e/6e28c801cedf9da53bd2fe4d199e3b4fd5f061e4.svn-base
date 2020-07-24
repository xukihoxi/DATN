# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError, except_orm, UserError


class TherapyRecord(models.Model):
    _inherit = 'therapy.record'

    interaction_last_date = fields.Date(string='Interaction Last Date')
    out_of_medicine_date = fields.Date(string='Out of Medicine Date')
    interaction_ids = fields.One2many('partner.interaction', 'therapy_record_id', string='Interactions')

    #todo nhắc lịch tự động cho chăm sóc khách hàng
    @api.model
    def cron_create_activity_history_auto(self):
        therapy_record_ids = []
        for therapy_record in self.search([]):
            bundle_therapies = therapy_record.therapy_bundle_ids.filtered(lambda line: line.state in ('signed_commitment', 'stop_care'))
            if not len(bundle_therapies) and len(therapy_record.therapy_record_product_ids):
                therapy_record_ids.append(therapy_record.id)
            is_activity_constant = False
        self.create_activity_history(therapy_record_ids, is_activity_constant)

    #todo hàm tạo lịch nhắc
    def create_activity_history(self, therapy_record_ids, is_activity_constant):
        for therapy_record_id in therapy_record_ids:
            therapy_record = self.search([('id', '=', therapy_record_id)], limit=1)
            if not therapy_record: raise UserError('Không tìm thấy hồ sơ trị liệu có id: %s! Liên hệ Admin để được giải quyết.' % (str(therapy_record_id)))
            if not therapy_record.categ_id.x_product_categ_remind_ids:
                raise UserError(
                    _("Nhóm dịch vụ %s chưa cấu hình nhắc lịch") % str(therapy_record.categ_id.name))
            config_remind = therapy_record.env['product.product'].get_config_remind(therapy_record.categ_id.x_product_categ_remind_ids)
            #nếu tạo lịch nhắc sau khi tạo tương tác muộn thì quét hết các lịch nhắc
            if is_activity_constant:
                reminds_created = therapy_record.env['activity.history'].search(
                    [('therapy_record_id', '=', therapy_record.id), ('state', '!=', 'interacted'), ('type', '=', 'customer_care')])
            #nếu tạo lịch tự động bằng job thì chỉ quét các lịch nhắc dc sinh tự động
            else:
                reminds_created = therapy_record.env['activity.history'].search(
                    [('therapy_record_id', '=', therapy_record.id), ('state', '!=', 'interacted'),
                     ('type', '=', 'customer_care'), ('is_activity_constant', '=', False)])
            if reminds_created:
                for remind_created in reminds_created:
                    remind_created.unlink()
            for config in config_remind:
                if config['repeat'] and therapy_record.interaction_last_date:
                    condition_end = timedelta(days=config['period']) + datetime.strptime(therapy_record.interaction_last_date, '%Y-%m-%d')
                    date_deadline = timedelta(days=config['date_number']) + datetime.strptime(therapy_record.interaction_last_date, '%Y-%m-%d')
                    while date_deadline < condition_end:
                        remind = therapy_record.env['activity.history'].create({
                            'therapy_record_id': therapy_record.id,
                            'partner_id': therapy_record.partner_id.id,
                            'mail_activity_type_id': config['activity_type_id'],
                            'type': 'customer_care',
                            'object': config['object'],
                            'user_id': False,
                            'date_deadline': date_deadline,
                        })
                        date_deadline += timedelta(days=config['date_number'])