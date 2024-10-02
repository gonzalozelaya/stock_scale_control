# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AllowWeightOnStock():
    _inherit = 'stock.picking'
    
    some_variable = fields.Char('Hola soy un field')


class WeightControl():
    _name = 'stock.picking.weight_control'
    
    state = fields.Selection(string="State", 
                             selection=[("first", "First pass"),("second","Second Pass"),("finished","Finished")])
    datetime = fields.Datetime('Time')
    weight = fields.Float('Weight')


    
    
# class my_module(models.Model):
#     _name = 'my_module.my_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100