# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
class AllowWeightOnStock(models.Model):
    _inherit = 'stock.picking'
    transport_id = fields.Many2one(
        comodel_name='stock.picking.transport',  # Apunta al modelo stock.move
        string='Transport',
    )

    
class AllowWeightOnStock(models.Model):
    _inherit = 'stock.move'

    discount = fields.Float('Discount')
    
    weight_control_ids = fields.One2many(
        comodel_name='stock.picking.weight_control',  # Apunta al modelo WeightControl
        inverse_name='stock_move_id',  # Nombre del campo Many2one en WeightControl
        string='Weight Controls',
    )

    first_weight = fields.Float(
        string='Entrada',
        compute='_compute_first_weight',
        store=False  # Cambia a True si deseas almacenar este campo
    )
    second_weight = fields.Float(
        string='Salida',
        compute='_compute_second_weight',
        store=False  # Cambia a True si deseas almacenar este campo
    )

    @api.depends('discount')
    def _compute_quantity_discount(self):
        for move in self:
            move.quantity = move.quantity + (move.quantity * discount / 100)
            
    @api.depends('first_weight', 'second_weight')
    def _compute_quantity(self):
        for move in self:
            if move.first_weight != 0 and move.second_weight != 0:
                line_found = False
                new_value = move.first_weight - move.second_weight
                for line in move.move_line_ids:
                    if line.product_id == move.product_id:
                        line_found = True
                        line.quantity = new_value
                
                if not line_found:
                    # Si no existe una línea con el mismo producto, la creamos
                    self.env['stock.move.line'].create({
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'quantity': new_value,
                        'location_id': move.location_id.id,
                        'location_dest_id': move.location_dest_id.id,
                        'picking_id': move.picking_id.id
                    })
                move.quantity = new_value

    @api.depends('weight_control_ids')
    def _compute_first_weight(self):
        for move in self:
            # Obtén el peso del primer WeightControl relacionado
            weight_control = self.env['stock.picking.weight_control'].search([
                ('stock_move_id', '=', move.id),('state', '=', 'first')
            ], limit=1)  # Limita a 1 para obtener solo el primero
            move.first_weight = weight_control.weight if weight_control else 0.0

    @api.depends('weight_control_ids')
    def _compute_second_weight(self):
        for move in self:
            # Obtén el peso del primer WeightControl relacionado
            weight_control = self.env['stock.picking.weight_control'].search([
                ('stock_move_id', '=', move.id),('state', '=', 'second')
            ], limit=1)  # Limita a 1 para obtener solo el primero
            move.second_weight = weight_control.weight if weight_control else 0.0

    
    
    def open_weight_control_popup(self):
        default_state = 'first'
        hasRecord = self.env['stock.picking.weight_control'].search([
                ('stock_move_id', '=', self.id),('state', '=', 'first')
            ], limit=1)
        if hasRecord:
            default_state = 'second'
        default_values = {
            'default_state': default_state,  # Estado inicial
            'default_datetime': fields.Datetime.now(),  # Tiempo actual
            'default_weight': 0.0,  # Valor inicial del peso
            'default_stock_move_id':self.id,
            'default_transport_id':self.picking_id.transport_id.id if self.picking_id.transport_id else False,
            'default_product_id': self.product_id.id
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

    display_name = fields.Char(string = "Display Name", compute = '_compute_display_name')
    
    state = fields.Selection(string = "State", 
                             selection = [("first", "Entrada"),("second","Salida"),("finished","Finished")],
                             required = True)
    datetime = fields.Datetime('Time')
    weight = fields.Float('Weight')
    stock_move_id = fields.Many2one(
        comodel_name='stock.move',  # Apunta al modelo stock.move
        string='Stock Move',
    )
    transport_id = fields.Many2one(
        comodel_name = 'stock.picking.transport',
        string='Transport',
    )
    product_id = fields.Many2one(
        comodel_name = 'product.product',
        string='Product',
    )
    document = fields.Char(related='stock_move_id.picking_id.name',string='Document')

    @api.depends('state','product_id')
    def _compute_display_name(self):
        for weight in self:
            if weight.state and weight.product_id:
                if weight.state == 'first':
                    weight.display_name = f'Entrada {weight.product_id.name}'
                elif weight.state == 'second':
                    weight.display_name = f'Salida {weight.product_id.name}'
            else:
                weight.display_name = False

class StockVehicles(models.Model):
    _name='stock.picking.transport'

    driver = fields.Char('Driver')
    driver_dni = fields.Char('DNI')
    transport = fields.Selection(string='Transport',selection=[('particular','Particular'),('econorte','Transporte de Econorte')])
    
    chasis = fields.Char('Chasis')
    acoplado = fields.Selection(string = 'Acoplado',selection=[('carro','CARRO'),('add','Add more')])

    stock_move_ids = fields.One2many(
        comodel_name='stock.picking',  
        inverse_name='transport_id', 
        string='Moves',
    )
    weight_control_ids = fields.One2many(
        comodel_name='stock.picking.weight_control',  # Apunta al modelo WeightControl
        inverse_name='transport_id',  # Nombre del campo Many2one en WeightControl
        string='Moves',
    )

    display_name = fields.Char(string = "Display Name", compute = '_compute_display_name')

    @api.depends('driver','chasis')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'{record.driver} - {record.chasis}'
    
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