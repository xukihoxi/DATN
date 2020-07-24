# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockInventoryCustomerUpdateTherapy(models.Model):
    _name = 'stock.inventory.customer.update.therapy'

    inventory_id = fields.Many2one('stock.inventory.customer.update',string='Update Inventory')
    partner_id = fields.Many2one('res.partner', 'Customer')
    therapy_id = fields.Many2one('therapy.record', string='Therapy Record')
    product_id = fields.Many2one('product.product','Service')
    total_qty = fields.Integer('Qty total')
    qty_hand = fields.Integer('Qty hand')
    qty_use = fields.Integer('Qty used')
    total_amount_money = fields.Float('Amount total')
    payment_amount = fields.Float('Amount payment')
    debt = fields.Float('Amount debt')
    order_id = fields.Many2one('pos.order')
    body_area_ids = fields.Many2many('body.area', string='Body Area')
    note = fields.Char("Note")
