# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AllowWeightOnStock(models.Model):
    _inherit = 'stock.picking'

    iot_device_id = fields.Many2one('iot.device', "Báscula",
                                    domain=[('type', '=', 'scale')],
                                    )

    available_iot_device_ids = fields.Many2many('iot.device')
    
    transport_ids = fields.Many2one(
            'transport.transport',
            string='Transporte', 
            readonly=True
        )
    
    driver_id = fields.Many2one(
        'transport.driver', 
        string='Conductor', 
        readonly=True,
    )

    chasis = fields.Many2one(
        'transport.patent',
        string='Chasis', 
        readonly=True,
    )

    acoplado = fields.Many2one(
        'transport.patent', 
        string='Acoplado', 
        readonly=True,
    )

    arrival_time = fields.Datetime('Hora de entrada')
    exit_time = fields.Datetime('Hora de salida')

    def button_validate(self):
        res = super(AllowWeightOnStock, self).button_validate()
        if self.origin:
            if self.picking_type_id.code == 'incoming':
                purchase_order = self.env['purchase.order'].search([('name', '=', self.origin)])
                if purchase_order:
                    purchase_order['date_done'] = self.date_done
            if self.picking_type_id.code == 'outgoing':
                sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
                if sale_order:
                    sale_order['date_done'] = self.date_done
        return res
                   
    @api.model
    def create(self, vals):
        # Ejecuta la lógica de asignación de iot_device_id solo durante la creación del registro
        picking_type_id = vals.get('picking_type_id')
        if picking_type_id:
            picking_type = self.env['stock.picking.type'].browse(picking_type_id)
            iot_scale_ids = picking_type.iot_scale_ids
            if iot_scale_ids:
                vals['iot_device_id'] = iot_scale_ids[0].id  # Seleccionar la primera báscula si hay más de una
            else:
                vals['iot_device_id'] = False
        else:
            vals['iot_device_id'] = False
        
        return super(AllowWeightOnStock, self).create(vals)
                
    @api.depends('picking_type_id')            
    def _compute_available_iot_device_ids(self):
        for picking in self:
            if picking.picking_type_id:
                picking.available_iot_device_ids = picking.picking_type_id.iot_scale_ids
            else:
                picking['iot_device_id'] = False 
        return