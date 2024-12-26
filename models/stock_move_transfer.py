from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class DirectTransfer(models.Model):
    _inherit = 'stock.move.direct_transfer'

    discount = fields.Float('Descuento')

    weight_control_ids = fields.One2many(
        comodel_name='stock.picking.weight_control',  # Apunta al modelo WeightControl
        inverse_name='stock_direct_move_id',  # Nombre del campo Many2one en WeightControl
        string='Weight Controls',
    )
    
    first_weight = fields.Float(
        string='Entrada',
        compute='_compute_first_weight',
        store=True  # Cambia a True si deseas almacenar este campo
    )
    second_weight = fields.Float(
        string='Salida',
        compute='_compute_second_weight',
        store=True  # Cambia a True si deseas almacenar este campo
    )

    value_with_discount = fields.Float('Valor con descuento')
                   
    @api.depends('first_weight', 'second_weight','discount')
    def _compute_quantity(self):
        for move in self:
            if move.first_weight != 0:
                line_found = False
                new_value = abs(move.first_weight - move.second_weight) - move.discount
                move.quantity = new_value

    @api.depends('weight_control_ids')
    def _compute_first_weight(self):
        for move in self:
            # Obtén el peso del primer WeightControl relacionado
            weight_control = self.env['stock.picking.weight_control'].search([
                ('stock_direct_move_id', '=', move.id),('state', '=', 'first')
            ], limit=1)  # Limita a 1 para obtener solo el primero
            move.first_weight = weight_control.weight if weight_control else 0.0

    @api.depends('weight_control_ids')
    def _compute_second_weight(self):
        for move in self:
            # Obtén el peso del primer WeightControl relacionado
            weight_control = self.env['stock.picking.weight_control'].search([
                ('stock_direct_move_id', '=', move.id),('state', '=', 'second')
            ], limit=1)  # Limita a 1 para obtener solo el primero
            move.second_weight = weight_control.weight if weight_control else 0.0


    def open_weight_control_popup(self):
        default_state = 'first'
        hasRecord = self.env['stock.picking.weight_control'].search([
                ('stock_direct_move_id', '=', self.id),('state', '=', 'first')
            ], limit=1)
        if hasRecord:
            default_state = 'second'
        default_values = {
            'default_state': default_state,  # Estado inicial
            'default_datetime': fields.Datetime.now(),  # Tiempo actual
            'default_stock_direct_move_id':self.id,
            'default_product_id': self.product_id.id,
            'default_iot_device_id': self.picking_transfer_id.iot_device_id.id,
            'default_driver_id':self.picking_transfer_id.driver_id.id,
            'default_transport_id': self.picking_transfer_id.transport_id.id,
            'default_chasis': self.picking_transfer_id.chasis.id,
            'default_acoplado':self.picking_transfer_id.acoplado.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pesaje',
            'res_model': 'stock.picking.weight_control',
            'view_mode': 'form',
            'target': 'new',  # 'new' para mostrar como modal/popup
            'context': default_values
        }
