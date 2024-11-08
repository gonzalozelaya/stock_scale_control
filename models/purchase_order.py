from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrderTransport(models.Model):
    _inherit = 'purchase.order'

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

    date_done = fields.Datetime('Hora de validación')
    

    
    @api.onchange('driver_id')
    def _onchange_driver_id(self):
        for order in self:
            if order.driver_id:
                order.dni = order.driver_id.dni

    @api.depends('driver_id', 'acoplado', 'chasis', 'transport_ids')
    def _update_picking_values(self):
        for record in self:
            # Asignar DNI si el conductor no lo tiene
            if not record.driver_id.dni:
                record.driver_id.write({'dni': record.driver_id.dni})
            updates = {
                'acoplado': record.acoplado.id,
                'chasis': record.chasis.id,
                'driver_id': record.driver_id.id,
                'transport_ids': record.transport_ids.id,
            }
            
            for picking in record.picking_ids:
                # Actualiza los campos con `write`
                picking.write(updates)
                
                
                    
    def button_confirm(self):
        res = super(PurchaseOrderTransport, self).button_confirm()
        for picking in self.picking_ids:
            picking.acoplado = self.acoplado.id
            picking.chasis = self.chasis.id
            picking.driver_id = self.driver_id.id
            picking.transport_ids = self.transport_id.id
            #Asignar DNI si el conductor no lo tiene
            if not picking.driver_id.dni:
                picking.driver_id.dni = self.dni
        return res