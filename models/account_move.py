from odoo import models, fields, api
from odoo.exceptions import UserError

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


    def _search_default_journal(self):
        if self.payment_id and self.payment_id.journal_id:
            return self.payment_id.journal_id
        if self.statement_line_id and self.statement_line_id.journal_id:
            return self.statement_line_id.journal_id
        if self.statement_line_ids.statement_id.journal_id:
            return self.statement_line_ids.statement_id.journal_id[:1]

        journal_types = self._get_valid_journal_types()
        company = self.company_id or self.env.company
        domain = [
            *self.env['account.journal']._check_company_domain(company),
            ('type', 'in', journal_types),
        ]

        journal = None
        # the currency is not a hard dependence, it triggers via manual add_to_compute
        # avoid computing the currency before all it's dependences are set (like the journal...)
        if self.env.cache.contains(self, self._fields['currency_id']):
            currency_id = self.currency_id.id or self._context.get('default_currency_id')
            if currency_id and currency_id != company.currency_id.id:
                currency_domain = domain + [('currency_id', '=', currency_id)]
                journal = self.env['account.journal'].search(currency_domain, limit=1)

        if not journal:
            if self.move_type == 'in_invoice':
                journal = self.env['account.journal'].browse(32)
            elif self.move_type == 'out_invoice':
                journal = self.env['account.journal'].browse(21)
        if not journal:
            journal = self.env['account.journal'].search(domain, limit=1)
        if not journal:
            error_msg = _(
                "No journal could be found in company %(company_name)s for any of those types: %(journal_types)s",
                company_name=company.display_name,
                journal_types=', '.join(journal_types),
            )
            raise UserError(error_msg)

        return journal