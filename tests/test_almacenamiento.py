from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestAlmacenamiento(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear un cliente
        self.cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente de prueba'
        })
        # Crear un almacén
        self.almacen = self.env['upocargo.almacen'].create({
            'name': 'Almacén 1',
            'tamaño_maximo': 1000,
            'temp_min': 10,
            'temp_max': 30,
            'humedad_min': 20,
            'humedad_max': 80
        })
        # Crear un bien almacenado
        self.bien = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien de prueba',
            'tamanyo': 100,
            'condicion_especial': False,
            'almacen': self.almacen.id
        })

    def test_create_almacenamiento_valid_dates(self):
        # Crear almacenamiento con fechas válidas
        almacenamiento = self.env['upocargo.almacenamiento'].create({
            'fecha_ingreso': '2024-12-01',
            'fecha_salida': '2024-12-10',
            'almacen': self.almacen.id,
            'cliente': self.cliente.id,
            'bienes_almacenados': [(4, self.bien.id)]
        })
        self.assertEqual(almacenamiento.fecha_ingreso, '2024-12-01')
        self.assertEqual(almacenamiento.fecha_salida, '2024-12-10')

    def test_create_almacenamiento_invalid_dates(self):
        # Intentar crear un almacenamiento con fechas inválidas
        with self.assertRaises(ValidationError):
            self.env['upocargo.almacenamiento'].create({
                'fecha_ingreso': '2024-12-10',
                'fecha_salida': '2024-12-01',
                'almacen': self.almacen.id,
                'cliente': self.cliente.id,
                'bienes_almacenados': [(4, self.bien.id)]
            })

    def test_create_almacenamiento_without_goods(self):
        # Crear almacenamiento sin bienes
        with self.assertRaises(ValidationError):
            self.env['upocargo.almacenamiento'].create({
                'fecha_ingreso': '2024-12-01',
                'fecha_salida': '2024-12-10',
                'almacen': self.almacen.id,
                'cliente': self.cliente.id
            })

    def test_create_almacenamiento_with_exceeding_size(self):
        # Crear un bien cuyo tamaño excede el límite del almacén
        bien_grande = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien muy grande',
            'tamanyo': 2000,  # Excede el tamaño máximo del almacén
            'condicion_especial': False,
            'almacen': self.almacen.id
        })
        
        # Intentar crear el almacenamiento con este bien
        with self.assertRaises(ValidationError):
            self.env['upocargo.almacenamiento'].create({
                'fecha_ingreso': '2024-12-01',
                'fecha_salida': '2024-12-10',
                'almacen': self.almacen.id,
                'cliente': self.cliente.id,
                'bienes_almacenados': [(4, bien_grande.id)]
            })

    def test_create_almacenamiento_with_sensor_condition(self):
        # Crear un bien con condición especial de temperatura
        bien_con_sensor = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien con sensor de temperatura',
            'tamanyo': 100,
            'condicion_especial': True,
            'tipo_sensor': 'temperatura',
            'valor_sensor_min': 15,
            'valor_sensor_max': 25,
            'almacen': self.almacen.id
        })

        # Crear un almacenamiento con este bien, y el almacén no cumple con las condiciones de sensor
        with self.assertRaises(ValidationError):
            self.env['upocargo.almacenamiento'].create({
                'fecha_ingreso': '2024-12-01',
                'fecha_salida': '2024-12-10',
                'almacen': self.almacen.id,
                'cliente': self.cliente.id,
                'bienes_almacenados': [(4, bien_con_sensor.id)]
            })

    def test_create_almacenamiento_with_invoice(self):
        # Crear almacenamiento
        almacenamiento = self.env['upocargo.almacenamiento'].create({
            'fecha_ingreso': '2024-12-01',
            'fecha_salida': '2024-12-10',
            'almacen': self.almacen.id,
            'cliente': self.cliente.id,
            'bienes_almacenados': [(4, self.bien.id)]
        })

        # Comprobar que se crea la factura
        self.assertTrue(almacenamiento.factura_id)
        self.assertEqual(almacenamiento.factura_id.precio, 500)  # Esto depende de los parámetros configurados

    def test_update_services_in_invoice(self):
        # Crear un servicio adicional
        servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Servicio adicional 1',
            'precio_final': 100
        })

        # Crear almacenamiento y agregar servicio adicional
        almacenamiento = self.env['upocargo.almacenamiento'].create({
            'fecha_ingreso': '2024-12-01',
            'fecha_salida': '2024-12-10',
            'almacen': self.almacen.id,
            'cliente': self.cliente.id,
            'bienes_almacenados': [(4, self.bien.id)],
            'servicios_adicionales': [(6, 0, [servicio_adicional.id])]
        })

        # Verificar que la factura se actualizó correctamente
        self.assertEqual(almacenamiento.factura_id.precio, 600)  # Precio base + servicio adicional

