# -*- coding: utf-8 -*-
{
    'name': "UPOCARGO",

    'summary': """Gestion del modulo upocargo""",

    'description': """Gestion de mudanzas, almacenamientos, etc..""",

    'author': "TSI - UPO, @Parritoso, @NicoPC27, @alvaro-078",
    'website': "https://www.upo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Logistics',
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
        'views/bienes_almacenados_view.xml',
        'views/proveedor_view.xml',
        'views/factura_view.xml',
        'views/vehiculo_view.xml',
        'views/empleado_view.xml',
        'views/templates.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [    
        'demo/upocargo.almacenamiento.csv',
        'demo/upocargo.bienes_almacenados.csv',
        'demo/upocargo.cliente.csv',
        'demo/upocargo.empleado.csv',
        'demo/upocargo.proveedor.csv',
        'demo/upocargo.servicios_adicionales.csv',
        'demo/upocargo.vehiculo.csv'   
    ],
    'application': True,
}
