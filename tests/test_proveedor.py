from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
import string


class TestProveedor(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear un servicio adicional para pruebas
        self.servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Servicio Extra',
            'precio_final': 300
        })

    def test_creacion_proveedor_con_id_unico(self):
        """ Verifica que el id_proveedor sea generado correctamente y sea único """
        proveedor = self.env['upocargo.proveedor'].create({
            'entidad': 'Proveedor de Prueba'
        })
        self.assertTrue(proveedor.id_proveedor, "El id_proveedor debería ser generado")
        self.assertEqual(len(proveedor.id_proveedor), 9, "El id_proveedor debería tener una longitud de 9 caracteres")
        self.assertTrue(all(c in string.ascii_uppercase + string.digits for c in proveedor.id_proveedor),
                        "El id_proveedor debería contener solo caracteres alfanuméricos")

    def test_campos_obligatorios(self):
        """ Verifica que los campos id_proveedor y entidad son obligatorios """
        with self.assertRaises(ValidationError):
            self.env['upocargo.proveedor'].create({
                'entidad': 'Proveedor de Prueba'
            })
        
        with self.assertRaises(ValidationError):
            self.env['upocargo.proveedor'].create({
                'id_proveedor': 'ABCDEFGHI'
            })

    def test_relacion_servicios_adicionales(self):
        """ Verifica que un proveedor pueda tener un servicio adicional asignado """
        proveedor = self.env['upocargo.proveedor'].create({
            'entidad': 'Proveedor con Servicio'
        })
        
        # Asignar un servicio adicional
        proveedor.servicios_adicionales = self.servicio_adicional.id
        
        self.assertEqual(proveedor.servicios_adicionales, self.servicio_adicional,
                         "El servicio adicional asignado al proveedor no es correcto")
    
    def test_herencia_de_cliente(self):
        """ Verifica que el proveedor hereda correctamente del modelo cliente """
        proveedor = self.env['upocargo.proveedor'].create({
            'entidad': 'Proveedor con Cliente Heredado'
        })

        # Comprobamos que el proveedor tenga el comportamiento de cliente
        self.assertTrue(proveedor._inherit == 'upocargo.cliente', "El proveedor no hereda correctamente de cliente")
    
    def test_id_proveedor_unico(self):
        """ Verifica que no se puedan crear dos proveedores con el mismo id_proveedor """
        proveedor_1 = self.env['upocargo.proveedor'].create({
            'entidad': 'Proveedor 1'
        })
        
        # Probar que el id_proveedor sea único
        proveedor_2 = self.env['upocargo.proveedor'].create({
            'entidad': 'Proveedor 2'
        })
        
        # Aunque se genere un id automáticamente, debería ser único en la base de datos
        self.assertNotEqual(proveedor_1.id_proveedor, proveedor_2.id_proveedor,
                            "Los ID de los proveedores deben ser únicos")

