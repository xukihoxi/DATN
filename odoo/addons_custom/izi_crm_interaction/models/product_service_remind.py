# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductServiceRemind(models.Model):
    _name = 'product.service.remind'

    name = fields.Char(string="Name")
    activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type')
    date_number = fields.Integer(string='Date Number')
    period = fields.Integer(string='Period')
    object = fields.Selection([('consultant', 'Consultant'), ('customer_care', 'Customer care')], string='Object')
    repeat = fields.Boolean(string='Repeat', default=False)
    note = fields.Char(string='Note')
    product_id = fields.Many2one('product.product', string="Product")

    @api.onchange('date_number', 'period')
    def _onchange_date_number_period(self):
        if self.date_number and self.period and self.date_number > self.period:
            raise UserError(_("Số ngày %s phải nhỏ hơn khoảng ngày %s!") % (self.date_number, self.period))


class ProductCategoryRemind(models.Model):
    _name = 'product.category.remind'

    name = fields.Char(string='Name')
    categ_id = fields.Many2one('product.category', string='Category')
    activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type')
    date_number = fields.Integer(string='Date Number')
    period = fields.Integer(string='Period')
    object = fields.Selection([('consultant', 'Consultant'), ('customer_care', 'Customer care')], string='Object')
    repeat = fields.Boolean(string='Repeat', default=False)
    note = fields.Char(string='Note')

    @api.onchange('date_number', 'period')
    def _onchange_date_number_period(self):
        if self.date_number and self.period and self.date_number > self.period:
            raise UserError(_("Số ngày %s phải nhỏ hơn khoảng ngày %s!") % (self.date_number, self.period))


class PosCategory(models.Model):
    _inherit = 'product.category'

    x_product_categ_remind_ids = fields.One2many('product.category.remind', 'categ_id', string='Product Category Remind')
