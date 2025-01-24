from odoo import models, fields, api
from odoo.exceptions import AccessError,UserError

class WeightControl(models.Model):
    _name = 'stock.picking.weight_control'

    company_id = fields.Many2one(
    'res.company', 
    string='Empresa', 
    required=True,
    default=lambda self: self.env.company
)
    show_password = fields.Boolean('Habilitar peso manual', default=False, store=False)
    password = fields.Char('Contraseña', store=True)
    show_success_message = fields.Boolean('Mostrar Mensaje de Éxito', default=False, store=False)

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
    weight_to_show = fields.Float('Mostrar peso', compute='_compute_weight_to_show', store=True, readonly=True)
    manual_weight = fields.Boolean('Ajuste manual',default=False )
    stock_move_id = fields.Many2one(
        comodel_name='stock.move',  # Apunta al modelo stock.move
        string='Movimiento',
    )
    company_id_from_move = fields.Many2one(
    comodel_name='res.company',
    string='Empresa (desde Movimiento)',
    related='stock_move_id.company_id',
    readonly=True,
    store=True  # Si quieres que se almacene en la base de datos
)
    stock_direct_move_id =fields.Many2one(
        comodel_name='stock.move.direct_transfer',  # Apunta al modelo stock.move
        string='Movimiento',
    )
    company_from_direct_move = fields.Many2one(
    comodel_name='res.company',
    string='Empresa (desde Movimiento)',
    related='stock_direct_move_id.company_id',
    readonly=True,
    store=True  # Si quieres que se almacene en la base de datos
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
                
    @api.depends('weight')
    def _compute_weight_to_show(self):
        for record in self:
            record.weight_to_show = record.weight

    def show_password_field(self):
        """Este método se llama cuando el usuario presiona el botón para mostrar el campo de contraseña."""
        for record in self:
            record.show_password = True

    @api.onchange('password')
    def _onchange_password(self):
        """Este método se ejecuta cuando el usuario cambia el valor de la contraseña."""
        correct_password = "contraseña"  # Define tu contraseña en un lugar seguro

        for record in self:
            if record.password and record.password == correct_password:
                record.manual_weight = True
                record.show_password = False  # Ocultar el campo de contraseña una vez validado
                record.password = False  # Limpiar el campo de contraseña después de validarla
                record.show_success_message = True  # Mostrar mensaje de éxito
            elif record.password:
                # Si la contraseña es incorrecta, muestra un error y restablece la contraseña
                record.password = False
                raise AccessError("Contraseña incorrecta. No tienes permisos para cambiar el ajuste manual.")