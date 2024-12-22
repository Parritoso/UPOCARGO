from odoo.tests import TransactionCase

class TestUpocargoConfiguracion(TransactionCase):

    def setUp(self):
        super(TestUpocargoConfiguracion, self).setUp()
        # Crear un registro de configuración
        self.config_obj = self.env['upocargo.configuracion'].create({})

    def test_default_values(self):
        # Verificar los valores por defecto
        self.assertEqual(self.config_obj.coste_vehiculo_extra, 100.0)
        self.assertEqual(self.config_obj.coste_empleado_extra, 50.0)
        self.assertEqual(self.config_obj.costos_reales, "300,500,700,1000,12000,15000,1700")
        self.assertEqual(self.config_obj.precio_por_dia_almacenamiento, 50.0)

    def test_set_values(self):
        # Establecer nuevos valores
        self.config_obj.coste_vehiculo_extra = 120.0
        self.config_obj.coste_empleado_extra = 60.0
        self.config_obj.costos_reales = "400,600,800,1200"
        self.config_obj.precio_por_dia_almacenamiento = 55.0
        
        # Guardar los valores usando el método set_values
        self.config_obj.set_values()
        
        # Verificar que los parámetros se han guardado correctamente
        self.assertEqual(self.env['ir.config_parameter'].get_param('upocargo.coste_vehiculo_extra'), '120.0')
        self.assertEqual(self.env['ir.config_parameter'].get_param('upocargo.coste_empleado_extra'), '60.0')
        self.assertEqual(self.env['ir.config_parameter'].get_param('upocargo.costos_reales'), '400,600,800,1200')
        self.assertEqual(self.env['ir.config_parameter'].get_param('upocargo.precio_por_dia_almacenamiento'), '55.0')

    def test_get_values(self):
        # Modificar los valores en el sistema
        self.env['ir.config_parameter'].set_param('upocargo.coste_vehiculo_extra', '150.0')
        self.env['ir.config_parameter'].set_param('upocargo.coste_empleado_extra', '75.0')
        self.env['ir.config_parameter'].set_param('upocargo.costos_reales', '500,700,900,1300')
        self.env['ir.config_parameter'].set_param('upocargo.precio_por_dia_almacenamiento', '60.0')
        
        # Obtener los valores usando el método get_values
        values = self.config_obj.get_values()
        
        # Verificar que los valores recuperados son correctos
        self.assertEqual(values['coste_vehiculo_extra'], 150.0)
        self.assertEqual(values['coste_empleado_extra'], 75.0)
        self.assertEqual(values['costos_reales'], '500,700,900,1300')
        self.assertEqual(values['precio_por_dia_almacenamiento'], 60.0)
