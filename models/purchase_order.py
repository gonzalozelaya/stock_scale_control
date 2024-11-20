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
        
    @api.depends_context('lang')
    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals(self):
        for order in self:
            # Filtrar las líneas que no sean de tipo display
            order_lines = order.order_line.filtered(lambda x: not x.display_type)

            # Preparar las líneas para el cálculo de impuestos con base en las cantidades recibidas
            tax_base_lines = []
            for line in order_lines:
                # Convertir la línea en un diccionario base de impuestos
                base_line_dict = line._convert_to_tax_base_line_dict()

                # Utilizar la cantidad recibida si está disponible
                quantity = line.qty_received if line.qty_received > 0 else line.product_qty

                # Actualizar la cantidad en el diccionario base
                base_line_dict['quantity'] = quantity


                tax_base_lines.append(base_line_dict)

            # Calcular los impuestos utilizando las líneas modificadas
            order.tax_totals = self.env['account.tax']._prepare_tax_totals(
                tax_base_lines,
                order.currency_id or order.company_id.currency_id,
            )