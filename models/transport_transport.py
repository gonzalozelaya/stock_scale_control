from odoo import models, fields, api
from odoo.exceptions import UserError

class Transport(models.Model):
    _name = 'transport.transport'

    name = fields.Char('Transport', required = True)
    
    driver_ids = fields.One2many(
        'transport.driver',
        'transport_id',
        string='Conductores'
    )