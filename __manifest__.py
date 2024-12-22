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
        'views/config_views.xml',
        'views/mudanzas_view.xml',
        'views/clientes_view.xml',
        'views/almacen_view.xml',
        'views/almacenamiento_view.xml',
        'views/bienes_almacenados_view.xml',
        'views/proveedor_view.xml',
        'views/factura_view.xml',
        'views/vehiculo_view.xml',
        'views/empleado_view.xml',
        'views/servicios_adicionales_view.xml',
        'views/templates.xml',
        'wizard/MudanzaCancelacionWizard_view.xml',
        'views/menu.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'upocargo/static/src/components/grafico_selector/grafico_ocupacion.xml',
            'upocargo/static/src/components/grafico_selector/grafico_ocupacion.js'
        ],
    },
    # only loaded in demonstration mode
    'demo': [    
        'demo/upocargo.almacen.csv',
        'demo/upocargo.empleado.csv',
        'demo/upocargo.vehiculo.csv' ,
        'demo/upocargo.proveedor.csv',
        'demo/upocargo.servicios_adicionales.csv',
        'demo/upocargo.cliente.csv',
        'demo/upocargo.bienes_almacenados.csv'
    ],
    'test': [
        'tests/test_configuracion.py',
        'tests/test_almacen.py',
        'tests/test_empleado.py',
        'tests/test_vehiculo.py',
        'tests/test_proveedor.py',
        'tests/test_servicios_adicionales.py',
        'tests/test_cliente.py',
        'tests/test_bienes_almacenados.py',
        'tests/test_factura.py',
        'tests/test_almacenamiento.py',
        'tests/test_mudanza.py',
        'tests/test_controllers.py'
    ],
    'application': True,
}
