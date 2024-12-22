from odoo.tests import TransactionCase

class TestFactura(TransactionCase):

    def test_create_factura_without_mudanza(self):
        # Crear una factura sin mudanza
        factura = self.env['upocargo.factura'].create({
            'precio': 1000.00,
            'currency_id': self.env.user.company_id.currency_id.id
        })

        self.assertEqual(factura.precio, 1000.00)
        self.assertFalse(factura.mudanza_id)  # Verificar que no hay mudanza asociada

    def test_create_factura_with_mudanza(self):
        # Crear una mudanza
        mudanza = self.env['upocargo.mudanza'].create({
            'cliente': self.env['upocargo.cliente'].create({
                'name': 'Cliente de prueba',
                'direccion': 'Calle Falsa 123',
                'telefono': 123456789,
                'email': 'cliente@example.com'
            }).id,
            'fecha': '2024-12-21',
            'id_mudanza': 'MUD001',
        })

        # Crear una factura con la mudanza asociada
        factura = self.env['upocargo.factura'].create({
            'precio': 1500.00,
            'currency_id': self.env.user.company_id.currency_id.id,
            'mudanza_id': mudanza.id
        })

        self.assertEqual(factura.precio, 1500.00)
        self.assertEqual(factura.mudanza_id, mudanza)  # Verificar que la mudanza esté asociada

    def test_mudanza_unique_association(self):
        # Crear una mudanza
        mudanza = self.env['upocargo.mudanza'].create({
            'cliente': self.env['upocargo.cliente'].create({
                'name': 'Cliente de prueba',
                'direccion': 'Calle Falsa 123',
                'telefono': 123456789,
                'email': 'cliente@example.com'
            }).id,
            'fecha': '2024-12-21',
            'id_mudanza': 'MUD001',
        })

        # Crear una primera factura con la mudanza asociada
        self.env['upocargo.factura'].create({
            'precio': 1000.00,
            'currency_id': self.env.user.company_id.currency_id.id,
            'mudanza_id': mudanza.id
        })

        # Intentar crear una segunda factura con la misma mudanza debería lanzar una excepción
        with self.assertRaises(ValidationError):
            self.env['upocargo.factura'].create({
                'precio': 1500.00,
                'currency_id': self.env.user.company_id.currency_id.id,
                'mudanza_id': mudanza.id
            })

    def test_agregar_gasto(self):
        # Crear una factura
        factura = self.env['upocargo.factura'].create({
            'precio': 1000.00,
            'currency_id': self.env.user.company_id.currency_id.id
        })

        # Agregar un gasto
        factura.agregar_gasto("Transporte", 200.00)

        # Verificar que el gasto ha sido añadido al desglose
        desglose = factura.obtener_desglose_gastos()
        self.assertEqual(len(desglose), 1)
        self.assertEqual(desglose[0]['concepto'], "Transporte")
        self.assertEqual(desglose[0]['valor'], 200.00)

    def test_eliminar_gasto(self):
        # Crear una factura
        factura = self.env['upocargo.factura'].create({
            'precio': 1000.00,
            'currency_id': self.env.user.company_id.currency_id.id
        })

        # Agregar algunos gastos
        factura.agregar_gasto("Transporte", 200.00)
        factura.agregar_gasto("Alquiler", 500.00)

        # Eliminar el gasto de transporte
        factura.eliminar_gasto("Transporte")

        # Verificar que el gasto ha sido eliminado
        desglose = factura.obtener_desglose_gastos()
        self.assertEqual(len(desglose), 1)
        self.assertEqual(desglose[0]['concepto'], "Alquiler")

    def test_actualizar_gasto(self):
        # Crear una factura
        factura = self.env['upocargo.factura'].create({
            'precio': 1000.00,
            'currency_id': self.env.user.company_id.currency_id.id
        })

        # Agregar un gasto
        factura.agregar_gasto("Transporte", 200.00)

        # Actualizar el valor del gasto
        factura.actualizar_gasto("Transporte", 300.00)

        # Verificar que el valor del gasto ha sido actualizado
        desglose = factura.obtener_desglose_gastos()
        self.assertEqual(desglose[0]['concepto'], "Transporte")
        self.assertEqual(desglose[0]['valor'], 300.00)

    def test_factura_with_mudanza_and_almacenamiento(self):
        # Crear una mudanza y un almacenamiento
        mudanza = self.env['upocargo.mudanza'].create({
            'cliente': self.env['upocargo.cliente'].create({
                'name': 'Cliente de prueba',
                'direccion': 'Calle Falsa 123',
                'telefono': 123456789,
                'email': 'cliente@example.com'
            }).id,
            'fecha': '2024-12-21',
            'id_mudanza': 'MUD001',
        })

        almacenamiento = self.env['upocargo.almacenamiento'].create({
            'cliente': self.env['upocargo.cliente'].create({
                'name': 'Cliente de prueba',
                'direccion': 'Calle Falsa 123',
                'telefono': 123456789,
                'email': 'cliente@example.com'
            }).id,
            'ubicacion': 'Almacen 1',
        })

        # Intentar crear una factura con mudanza y almacenamiento debería lanzar una excepción
        with self.assertRaises(ValidationError):
            self.env['upocargo.factura'].create({
                'precio': 1500.00,
                'currency_id': self.env.user.company_id.currency_id.id,
                'mudanza_id': mudanza.id,
                'almacenamiento_id': almacenamiento.id
            })
