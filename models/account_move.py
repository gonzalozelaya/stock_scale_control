from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)
class AccountMove(models.Model):
    _inherit = 'account.move'

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
    date_start = fields.Datetime ('Hora de entrada')
    date_done = fields.Datetime('Hora de validación')

    
    @api.model
    def create(self, vals):
        # Establecer invoice_date a hoy si no se proporciona
        if 'invoice_date' not in vals:
            vals['invoice_date'] = fields.Date.context_today(self)
         # Verificar si tiene origen de factura y es una factura de cliente
        if vals.get('invoice_origin'): 
            if vals.get('move_type') == 'out_invoice':
                # Buscar la orden de venta que tenga el mismo nombre que invoice_origin
                sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
                
                # Si encuentra la orden, puedes realizar alguna acción con ella aquí, por ejemplo:
                if sale_order:
                    vals['transport_id'] = sale_order.transport_id.id
                    vals['driver_id'] = sale_order.driver_id.id
                    vals['chasis'] = sale_order.chasis.id
                    vals['acoplado'] = sale_order.acoplado.id
                    vals['date_done'] = sale_order.effective_date
            elif vals.get('move_type') == 'in_invoice':
                # Buscar la orden de compra que tenga el mismo nombre que invoice_origin
                purchase_order = self.env['purchase.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
                
                # Si encuentra la orden, puedes realizar alguna acción con ella aquí, por ejemplo:
                if purchase_order:
                    vals['transport_id'] = purchase_order.transport_id.id
                    vals['driver_id'] = purchase_order.driver_id.id
                    vals['chasis'] = purchase_order.chasis.id
                    vals['acoplado'] = purchase_order.acoplado.id
                    vals['date_done'] = purchase_order.effective_date
                    vals['date_start'] = purchase_order.date_approve

        return super(AccountMove, self).create(vals)


