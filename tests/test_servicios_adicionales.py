from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
import string


class TestServiciosAdicionales(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear un cliente para pruebas
        self.cliente = self.env['upocargo.cliente'].create({
            'entidad': 'Cliente de Prueba'
        })
        # Crear un proveedor para pruebas
        self.proveedor = self.env['upocargo.proveedor'].create({
            'entidad': 'Proveedor de Prueba'
        })

    def test_creacion_servicio_adicional_con_id_unico(self):
        """ Verifica que el id_servicios sea generado correctamente y sea único """
        servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Mudanza',
            'precio_base': 100,
            'aplicable_a': 'mudanza'
        })
        self.assertTrue(servicio_adicional.id_servicios, "El id_servicios debería ser generado")
        self.assertEqual(len(servicio_adicional.id_servicios), 9, "El id_servicios debería tener una longitud de 9 caracteres")
        self.assertTrue(all(c in string.ascii_uppercase + string.digits for c in servicio_adicional.id_servicios),
                        "El id_servicios debería contener solo caracteres alfanuméricos")

    def test_campos_obligatorios(self):
        """ Verifica que los campos id_servicios, tipo, precio_base y aplicable_a son obligatorios """
        with self.assertRaises(ValidationError):
            self.env['upocargo.servicios_adicionales'].create({
                'tipo': 'Mudanza',
                'precio_base': 100,
                'aplicable_a': 'mudanza'
            })
        
        with self.assertRaises(ValidationError):
            self.env['upocargo.servicios_adicionales'].create({
                'id_servicios': 'SERV1234',
                'precio_base': 100,
                'aplicable_a': 'mudanza'
            })
        
        with self.assertRaises(ValidationError):
            self.env['upocargo.servicios_adicionales'].create({
                'id_servicios': 'SERV1234',
                'tipo': 'Mudanza',
                'aplicable_a': 'mudanza'
            })

        with self.assertRaises(ValidationError):
            self.env['upocargo.servicios_adicionales'].create({
                'id_servicios': 'SERV1234',
                'tipo': 'Mudanza',
                'precio_base': 100,
            })

    def test_calculo_precio_final(self):
        """ Verifica que el precio final se calcule correctamente con un 5% añadido """
        servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Mudanza',
            'precio_base': 100,
            'aplicable_a': 'mudanza'
        })
        servicio_adicional._compute_precio_final()  # Forzar el cálculo del precio final
        self.assertEqual(servicio_adicional.precio_final, 105.0, "El precio final debe ser el precio base más un 5%")

    def test_relacion_con_proveedores(self):
        """ Verifica que un servicio adicional pueda tener proveedores asociados """
        servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Mudanza',
            'precio_base': 100,
            'aplicable_a': 'mudanza'
        })
        
        # Asignar el proveedor al servicio adicional
        servicio_adicional.proveedores = self.proveedor.id
        
        # Verificar que el proveedor esté asociado al servicio adicional
        self.assertIn(self.proveedor, servicio_adicional.proveedores, "El proveedor no está asociado correctamente al servicio adicional")

    def test_relacion_con_clientes(self):
        """ Verifica que un servicio adicional pueda tener un cliente asociado """
        servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Mudanza',
            'precio_base': 100,
            'aplicable_a': 'mudanza'
        })
        
        # Asignar el cliente al servicio adicional
        servicio_adicional.cliente = self.cliente.id
        
        # Verificar que el cliente esté asociado al servicio adicional
        self.assertEqual(servicio_adicional.cliente, self.cliente, "El cliente no está asociado correctamente al servicio adicional")
