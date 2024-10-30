from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        # Establecer invoice_date a hoy si no se proporciona
        if 'invoice_date' not in vals:
            vals['invoice_date'] = fields.Date.context_today(self)
        return super(AccountMove, self).create(vals)