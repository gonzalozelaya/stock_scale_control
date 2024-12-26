from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class DirectTransfer(models.Model):
    _inherit = 'stock.picking.transfer'
    
    transport_id = fields.Many2one(
            'transport.transport', 
            string='Transporte', 
            required=True
        )

    driver_id = fields.Many2one(
        'transport.driver', 
        string='Conductor', 
        required=True,
    )

    chasis = fields.Many2one(
        'transport.patent', 
        string='Chasis', 
        required=True,
    )

    acoplado = fields.Many2one(
        'transport.patent', 
        string='Acoplado', 
        required=True,
    )
    dni = fields.Char('Identificación')

    iot_device_id = fields.Many2one('iot.device', "Báscula",
                                domain=[('type', '=', 'scale')],)

    available_iot_device_ids = fields.Many2many('iot.device')

    def send_products(self):
        _logger.info('Hola mundoooooo')    
        self.date = fields.Datetime.now()
        if not self.name:
            self.name = self.env['ir.sequence'].next_by_code('stock.picking.transfer') or 'Nuevo'
            self.display_name = self.name
            self.sequence_used = self.name
        # Asegúrate de que los valores no se pierdan aquí
        
        self.write({
            'state': 'assigned',
            'location_dest_id_new': int(self.location_dest_id),
            
        })
        iot_device = self.env['stock.picking.type'].sudo().search([('company_id','=',self.location_dest_id_new.company_id.id)],limit=1)
        _logger.info(str(iot_device.iot_scale_ids))
        if iot_device.iot_scale_ids:
            self['iot_device_id'] =iot_device.iot_scale_ids[0].id
    
    @api.onchange('driver_id')
    def _onchange_driver_id(self):
        for order in self:
            if order.driver_id:
                order.dni = order.driver_id.dni
    
