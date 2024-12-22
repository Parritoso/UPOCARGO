from odoo.tests import TransactionCase

class TestEmpleado(TransactionCase):

    def test_create_empleado_without_phone(self):
        # Crear un empleado sin teléfono
        empleado = self.env['upocargo.empleado'].create({
            'nombre': 'Empleado de prueba',
            'email': 'empleado@example.com',
            'cargo': 'Gerente'
        })

        self.assertEqual(empleado.nombre, 'Empleado de prueba')
        self.assertFalse(empleado.telefono)  # El teléfono no debe estar presente

    def test_create_empleado_with_phone(self):
        # Crear un empleado con teléfono
        empleado = self.env['upocargo.empleado'].create({
            'nombre': 'Empleado con teléfono',
            'email': 'empleado_con_telefono@example.com',
            'cargo': 'Supervisor',
            'telefono': 987654321
        })

        self.assertEqual(empleado.nombre, 'Empleado con teléfono')
        self.assertEqual(empleado.telefono, 987654321)  # El teléfono debe coincidir

    def test_generate_id_empleado(self):
        # Crear un empleado
        empleado = self.env['upocargo.empleado'].create({
            'nombre': 'Empleado con ID generado',
            'email': 'empleado_id@example.com',
            'cargo': 'Asistente'
        })

        # Verificar que el ID del empleado sea generado correctamente (debe tener 9 caracteres)
        self.assertEqual(len(empleado.id_empleado), 9)
        self.assertTrue(empleado.id_empleado.isalnum())  # Verificar que solo contenga caracteres alfanuméricos

    def test_create_empleado_with_cargo(self):
        # Crear un empleado con cargo
        empleado = self.env['upocargo.empleado'].create({
            'nombre': 'Empleado con cargo',
            'email': 'empleado_con_cargo@example.com',
            'cargo': 'Manager',
        })

        self.assertEqual(empleado.nombre, 'Empleado con cargo')
        self.assertEqual(empleado.cargo, 'Manager')  # El cargo debe coincidir

    def test_rec_name_field(self):
        # Crear un empleado
        empleado = self.env['upocargo.empleado'].create({
            'nombre': 'Empleado para rec_name',
            'email': 'empleado_rec_name@example.com',
            'cargo': 'Director'
        })

        # Verificar que el campo rec_name_field tenga el valor esperado
        expected_rec_name = f"Empleado para rec_name ({empleado.id_empleado})"
        self.assertEqual(empleado.rec_name_field, expected_rec_name)

    def test_assign_mudanza_to_empleado(self):
        # Crear un empleado
        empleado = self.env['upocargo.empleado'].create({
            'nombre': 'Empleado con mudanza',
            'email': 'empleado_mudanza@example.com',
            'cargo': 'Logístico'
        })

        # Crear una mudanza y asignarla al empleado
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

        # Asignar la mudanza al empleado
        empleado.mudanza = [(4, mudanza.id)]

        # Verificar que la mudanza esté correctamente asignada al empleado
        self.assertTrue(mudanza in empleado.mudanza)

    def test_create_empleado_with_invalid_email(self):
        # Intentar crear un empleado con un correo electrónico inválido
        with self.assertRaises(ValidationError):
            self.env['upocargo.empleado'].create({
                'nombre': 'Empleado con email inválido',
                'email': 'empleado_email_invalido.com',  # Email no válido
                'cargo': 'Asistente'
            })

    def test_create_empleado_with_invalid_telefono(self):
        # Intentar crear un empleado con un teléfono no numérico
        with self.assertRaises(ValidationError):
            self.env['upocargo.empleado'].create({
                'nombre': 'Empleado con teléfono no numérico',
                'email': 'empleado_telefono_invalido@example.com',
                'telefono': 'abc123',  # Teléfono no numérico
                'cargo': 'Vendedor'
            })
