from odoo import models, fields, api

class Patent(models.Model):
    _name = 'transport.patent'
    
    name = fields.Char('Número de patente',required = True)
    display_name = fields.Char(readonly=True,compute='_compute_display_name')
    type = fields.Selection(string='Tipo',selection = [('chasis','Chasis'),('acoplado','Acoplado')])

    driver_ids = fields.Many2many(
        'transport.driver',
        string='Conductores'
    )

    @api.depends('name')
    def _compute_display_name(self):
        for patent in self:
            patent.display_name = patent.name