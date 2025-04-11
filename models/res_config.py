# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'
   weight_pasword = fields.Char(string='Discount limit',                                               
         config_parameter='stock_scale_control.password',
         help='Contraseña para pesaje manual')
