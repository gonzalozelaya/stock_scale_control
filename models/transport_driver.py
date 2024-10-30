from odoo import models, fields, api

class Driver(models.Model):
    _name = 'transport.driver'

    name = fields.Char('Nombre')
    dni = fields.Char('Identificación')

    transport_id = fields.Many2one(
        'transport.transport', 
        string='Transporte',
        ondelete='set null'
    )
    
    patent_ids = fields.Many2many(
            'transport.patent', 
            string='Patentes'
        )