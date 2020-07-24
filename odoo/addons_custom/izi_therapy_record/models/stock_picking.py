# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import date
from odoo.exceptions import UserError, ValidationError, MissingError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_therapy_prescription_id = fields.Many2one('therapy.prescription', string='Therapy Prescription')
    x_therapy_record_id = fields.Many2one('therapy.record', related='x_therapy_prescription_id.therapy_record_id', string='Therapy Record', store=True, readonly=True)
    x_medicine_day_ok = fields.Boolean(string='Medicine Day')

    @api.multi
    def action_done(self):
        res = super(StockPicking, self).action_done()
        qty = 0
        if self.x_therapy_record_id:
            #todo tính số ngày thuốc trong phiếu chỉ định
            if self.x_medicine_day_ok:
                for therapy_prescription_line_remain_id in self.x_therapy_prescription_id.therapy_prescription_line_remain_ids:
                    if therapy_prescription_line_remain_id.product_id.x_is_medicine_day:
                        qty = therapy_prescription_line_remain_id.qty
            #todo trừ tồn trên HSTL
            for therapy_record_product_id in self.x_therapy_record_id.therapy_record_product_ids:
                therapy_quantity_used = 0
                check = False
                for move_line in self.move_lines:
                    if move_line.quantity_done !=0 and move_line.product_id.id == therapy_record_product_id.product_id.id:
                        if move_line.x_is_product_remain:
                            therapy_quantity_used += move_line.quantity_done
                # kiểm tra xem sản phâm có phải tử phiếu chỉ định bảo hành k?
                therapy_record_product_id.qty_used += therapy_quantity_used
                # todo trừ tồn số ngày thuốc
                if therapy_record_product_id.product_id.x_is_medicine_day:
                    therapy_record_product_id.qty_used += qty
        return res




class StockMove(models.Model):
    _inherit = 'stock.move'

    x_therapy_prescription_id = fields.Many2one('therapy.prescription', string='Therapy Prescription')
    x_therapy_record_id = fields.Many2one('therapy.record', related='x_therapy_prescription_id.therapy_record_id', string='Therapy Record', store=True, readonly=True)
    x_is_product_remain = fields.Boolean(string='Is product Remain', default=False)

