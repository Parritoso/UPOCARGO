# -*- coding: utf-8 -*-
{
    'name': "upocargo",

    'summary': """Gestion del modulo upocargo""",

    'description': """Gestion de clases, usuarios, material, etc.""",

    'author': "TSI - UPO",
    'website': "https://www.upo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/mudanzas_view.xml',
        'views/clientes_view.xml',
        'views/almacenamiento_view.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [     
    ],
    'application': True,
}