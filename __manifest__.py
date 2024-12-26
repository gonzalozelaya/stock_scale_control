# -*- coding: utf-8 -*-
{
    'name': "stock_scale_control",

    'summary': """
        Allows to weight on stock.picking""",

    'description': """
        Allows to weight on stock.picking
    """,

    'author': "OutsourceArg",
    'website': "https://www.outsourcearg.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['delivery_iot','stock','account','purchase','multi_company_direct_transfer'],
    'assets': {
    'web.assets_backend': [
        'stock_scale_control/static/src/css/style.css',
        'stock_scale_control/static/src/xml/one2many_widget.xml',
    ]
    },
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/weight_control_views.xml',
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml',
        'views/account_move.xml',
        'reports/report_recepcion.xml',
        'reports/report_small_header.xml',
        'views/transport_driver.xml',
        'views/direct_transfer_view.xml'
    ],

}