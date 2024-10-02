# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AllowWeightOnStock(models.Model):
    _inherit = 'stock.picking'
    some_variable = fields.Char('Hola soy un field')
    
class AllowWeightOnStock(models.Model):
    _inherit = 'stock.move'
    
    weight_control_ids = fields.One2many(
        comodel_name='stock.picking.weight_control',  # Apunta al modelo WeightControl
        inverse_name='stock_move_id',  # Nombre del campo Many2one en WeightControl
        string='Weight Controls',
    )
    
    def open_weight_control_popup(self):
        # Devolver la acción que abre el formulario en un popup
        default_values = {
            'default_state': 'first',  # Estado inicial
            'default_datetime': fields.Datetime.now(),  # Tiempo actual
            'default_weight': 0.0,  # Valor inicial del peso
            'default_stock_move_id':self.id
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Weight Control',
            'res_model': 'stock.picking.weight_control',
            'view_mode': 'form',
            'target': 'new',  # 'new' para mostrar como modal/popup
            'context': default_values
        }
        
class WeightControl(models.Model):
    _name = 'stock.picking.weight_control'
    
    state = fields.Selection(string="State", 
                             selection=[("first", "First pass"),("second","Second Pass"),("finished","Finished")])
    datetime = fields.Datetime('Time')
    weight = fields.Float('Weight')
    stock_move_id = fields.Many2one(
        comodel_name='stock.move',  # Apunta al modelo stock.move
        string='Stock Move',
        ondelete='cascade',  # Elimina en cascada si el registro de stock.move es eliminado
    )

    
    
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