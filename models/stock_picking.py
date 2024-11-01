# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AllowWeightOnStock(models.Model):
    _inherit = 'stock.picking'

    iot_device_id = fields.Many2one('iot.device', "Scale",
                                    domain=[('type', '=', 'scale')],
                                    compute = '_compute_iot_device')

    available_iot_device_ids = fields.Many2many('iot.device',compute='_compute_available_iot_device_ids')
    
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
                   
    @api.depends('picking_type_id')
    def _compute_iot_device(self):
        for picking in self:
            if picking.picking_type_id:
                iot_scale_ids = picking.picking_type_id.iot_scale_ids
                if iot_scale_ids[0]:
                    # Seleccionar la primera báscula si hay más de una
                    picking['iot_device_id'] = iot_scale_ids[0].id
                else:
                    picking['iot_device_id'] = False
            else:
                picking['iot_device_id'] = False
                
    @api.depends('picking_type_id')            
    def _compute_available_iot_device_ids(self):
        for picking in self:
            if picking.picking_type_id:
                picking.available_iot_device_ids = picking.picking_type_id.iot_scale_ids
            else:
                picking['iot_device_id'] = False 
        return