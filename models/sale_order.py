from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    transport_id = fields.Many2one(
            'transport.transport', 
            string='Transporte', 
            required=False
        )
    
    driver_id = fields.Many2one(
        'transport.driver', 
        string='Conductor', 
        required=False,
    )

    chasis = fields.Many2one(
        'transport.patent', 
        string='Chasis', 
        required=False,
    )

    acoplado = fields.Many2one(
        'transport.patent', 
        string='Acoplado', 
        required=False,
    )
    dni = fields.Char('Identificación')

    date_done = fields.Datetime('Fecha validada')
    
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for picking in self.picking_ids:
            picking.acoplado = self.acoplado.id
            picking.chasis = self.chasis.id
            picking.driver_id = self.driver_id.id
            picking.transport_ids = self.transport_id.id
            #Asignar DNI si el conductor no lo tiene
            if not picking.driver_id.dni:
                picking.driver_id.dni = picking.dni
        return res
