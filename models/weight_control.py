from odoo import models, fields, api

class WeightControl(models.Model):
    _name = 'stock.picking.weight_control'

    #available_scale_ids = fields.Many2many('iot.device', related='picking_type_id.iot_scale_ids')
    iot_device_id = fields.Many2one('iot.device', "Báscula")
    iot_device_identifier = fields.Char(related='iot_device_id.identifier')
    iot_ip = fields.Char(related='iot_device_id.iot_ip')
    #manual_measurement = fields.Boolean(related='iot_device_id.manual_measurement')
    manual_measurement = fields.Boolean('Manual', default = True)

    display_name = fields.Char(string = "Display Name", compute = '_compute_display_name')
    
    state = fields.Selection(string = "Estado", 
                             selection = [("first", "Entrada"),("second","Salida"),("finished","Finished")],
                             required = True)
    datetime = fields.Datetime('Fecha y Hora')
    weight = fields.Float('Peso',store=True)
    manual_weight = fields.Boolean('Ajuste manual',default=True)
    stock_move_id = fields.Many2one(
        comodel_name='stock.move',  # Apunta al modelo stock.move
        string='Movimiento',
    )
    product_id = fields.Many2one(
        comodel_name = 'product.product',
        string='Producto',
    )
    document = fields.Char(related='stock_move_id.picking_id.name',string='Documento')

    transport_id = fields.Many2one(
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
    @api.onchange('weight')
    def _onchange_weight(self):
        for weight in self:
            weight['weight'] = weight.weight
    