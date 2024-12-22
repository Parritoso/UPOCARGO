from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestCliente(TransactionCase):

    def test_create_cliente_without_password(self):
        # Crear un cliente sin contraseña
        cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente de prueba',
            'direccion': 'Calle Falsa 123',
            'telefono': 123456789,
            'email': 'cliente@example.com'
        })

        self.assertEqual(cliente.name, 'Cliente de prueba')
        self.assertFalse(cliente.password)  # La contraseña debe estar vacía

    def test_create_cliente_with_password(self):
        # Crear un cliente con contraseña
        cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente con contraseña',
            'direccion': 'Calle Ejemplo 456',
            'telefono': 987654321,
            'email': 'cliente_con_pass@example.com',
            'password': 'mi_contraseña_segura'
        })

        self.assertEqual(cliente.name, 'Cliente con contraseña')
        self.assertTrue(cliente.password)  # La contraseña debe existir
        self.assertNotEqual(cliente.password, 'mi_contraseña_segura')  # La contraseña debe estar cifrada
        self.assertTrue(cliente.salt_password)  # El salt debe estar presente

    def test_update_cliente_password(self):
        # Crear un cliente sin contraseña inicialmente
        cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente para actualizar',
            'direccion': 'Calle Nueva 789',
            'telefono': 123123123,
            'email': 'cliente_update@example.com'
        })

        # Actualizar la contraseña del cliente
        cliente.write({'password': 'nueva_contraseña'})

        # Verificar que la contraseña se ha cifrado
        self.assertTrue(cliente.password)  # La contraseña debe estar cifrada
        self.assertNotEqual(cliente.password, 'nueva_contraseña')  # La contraseña debe estar cifrada
        self.assertTrue(cliente.salt_password)  # El salt debe estar presente

    def test_compute_display_next_mudanza(self):
        # Crear un cliente
        cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente con mudanza',
            'direccion': 'Calle Final 321',
            'telefono': 555123456,
            'email': 'cliente_mudanza@example.com'
        })

        # Crear mudanzas asociadas al cliente
        mudanza_futura = self.env['upocargo.mudanza'].create({
            'cliente': cliente.id,
            'fecha': date.today() + timedelta(days=5),
            'id_mudanza': 'MUD123',
        })
        mudanza_pasada = self.env['upocargo.mudanza'].create({
            'cliente': cliente.id,
            'fecha': date.today() - timedelta(days=5),
            'id_mudanza': 'MUD124',
        })

        # Actualizar el cliente y verificar el campo computado
        cliente._compute_display_next_mudanza()
        self.assertEqual(cliente.mudanza, "ID: MUD123, Dias restantes: 5")

        # Verificar cuando no hay mudanzas futuras
        mudanza_pasada.write({'fecha': date.today() - timedelta(days=10)})
        cliente._compute_display_next_mudanza()
        self.assertEqual(cliente.mudanza, "No hay mudanzas proximas")

    def test_generate_id_cliente(self):
        # Crear un cliente
        cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente con ID generado',
            'direccion': 'Calle ID 100',
            'telefono': 112233445,
            'email': 'cliente_id@example.com'
        })

        # Verificar que el ID del cliente sea generado correctamente (debe tener 9 caracteres)
        self.assertEqual(len(cliente.id_cliente), 9)
        self.assertTrue(cliente.id_cliente.isalnum())  # Verificar que solo contenga caracteres alfanuméricos

    def test_check_password(self):
        # Crear un cliente con contraseña
        cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente de contraseña',
            'direccion': 'Calle Secreta 400',
            'telefono': 666444333,
            'email': 'cliente_password@example.com',
            'password': 'contraseña_secreta'
        })

        # Verificar que la contraseña proporcionada sea correcta
        self.assertTrue(cliente._check_password('contraseña_secreta'))

        # Verificar que una contraseña incorrecta sea rechazada
        self.assertFalse(cliente._check_password('contraseña_incorrecta'))

    def test_create_cliente_with_invalid_email(self):
        # Intentar crear un cliente con un email inválido
        with self.assertRaises(ValidationError):
            self.env['upocargo.cliente'].create({
                'name': 'Cliente con email inválido',
                'direccion': 'Calle Imposible 900',
                'telefono': 123123123,
                'email': 'cliente_email_invalido.com'  # Email no válido
            })
