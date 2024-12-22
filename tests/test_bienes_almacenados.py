from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestBienesAlmacenados(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear almacenamiento
        self.almacenamiento = self.env['upocargo.almacenamiento'].create({
            'fecha_ingreso': '2024-12-01',
            'fecha_salida': '2024-12-10',
            'almacen': self.env['upocargo.almacen'].create({'name': 'Almacén 1'}).id,
            'cliente': self.env['upocargo.cliente'].create({'name': 'Cliente de prueba'}).id,
        })

    def test_create_bien_without_condition(self):
        # Crear un bien almacenado sin condición especial
        bien = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien sin condición especial',
            'tamanyo': 100,
            'cantidad': 10,
            'almacenamiento': self.almacenamiento.id,
            'condicion_especial': False
        })

        self.assertEqual(bien.descripcion, 'Bien sin condición especial')
        self.assertFalse(bien.condicion_especial)

    def test_create_bien_with_condition(self):
        # Crear un bien almacenado con condición especial
        bien = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien con condición especial',
            'tamanyo': 50,
            'cantidad': 5,
            'almacenamiento': self.almacenamiento.id,
            'condicion_especial': True,
            'tipo_sensor': 'temperatura',
            'valor_sensor_min': 10,
            'valor_sensor_max': 30
        })

        self.assertEqual(bien.descripcion, 'Bien con condición especial')
        self.assertTrue(bien.condicion_especial)
        self.assertEqual(bien.tipo_sensor, 'temperatura')
        self.assertEqual(bien.valor_sensor_min, 10)
        self.assertEqual(bien.valor_sensor_max, 30)

    def test_create_bien_with_weight(self):
        # Crear un bien con peso especificado
        bien = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien con peso',
            'tamanyo': 200,
            'cantidad': 5,
            'peso': 50,
            'almacenamiento': self.almacenamiento.id
        })

        self.assertEqual(bien.peso, 50)

    def test_create_bien_with_quantity(self):
        # Crear un bien con cantidad
        bien = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien con cantidad',
            'tamanyo': 100,
            'cantidad': 10,
            'almacenamiento': self.almacenamiento.id
        })

        self.assertEqual(bien.cantidad, 10)

    def test_generate_id_bien(self):
        # Crear un bien
        bien = self.env['upocargo.bienes_almacenados'].create({
            'descripcion': 'Bien con ID generado',
            'tamanyo': 100,
            'cantidad': 5,
            'almacenamiento': self.almacenamiento.id
        })

        # Verificar que el ID del bien sea generado correctamente (debe tener 9 caracteres)
        self.assertEqual(len(bien.id_bien), 9)
        self.assertTrue(bien.id_bien.isalnum())  # Verificar que solo contenga caracteres alfanuméricos

    def test_create_bien_with_invalid_sensor_values(self):
        # Crear un bien con valores del sensor fuera del rango válido
        with self.assertRaises(ValidationError):
            self.env['upocargo.bienes_almacenados'].create({
                'descripcion': 'Bien con valores de sensor inválidos',
                'tamanyo': 100,
                'cantidad': 5,
                'almacenamiento': self.almacenamiento.id,
                'condicion_especial': True,
                'tipo_sensor': 'temperatura',
                'valor_sensor_min': 30,
                'valor_sensor_max': 10  # Valor máximo menor que el mínimo
            })

    def test_create_bien_without_description(self):
        # Intentar crear un bien sin descripción
        with self.assertRaises(ValidationError):
            self.env['upocargo.bienes_almacenados'].create({
                'tamanyo': 100,
                'cantidad': 5,
                'almacenamiento': self.almacenamiento.id
            })
