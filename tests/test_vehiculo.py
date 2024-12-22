from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
import string


class TestVehiculo(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear una mudanza para pruebas
        self.mudanza = self.env['upocargo.mudanza'].create({
            'nombre': 'Mudanza de prueba',
        })

    def test_creacion_vehiculo_con_id_unico(self):
        """ Verifica que el id_vehiculo sea generado correctamente y sea único """
        vehiculo = self.env['upocargo.vehiculo'].create({
            'matricula': '1234ABC',
            'capacidad': 5000,
            'estado': 'activo',
        })
        self.assertTrue(vehiculo.id_vehiculo, "El id_vehiculo debería ser generado")
        self.assertEqual(len(vehiculo.id_vehiculo), 9, "El id_vehiculo debería tener una longitud de 9 caracteres")
        self.assertTrue(all(c in string.ascii_uppercase + string.digits for c in vehiculo.id_vehiculo),
                        "El id_vehiculo debería contener solo caracteres alfanuméricos")

    def test_campos_obligatorios(self):
        """ Verifica que los campos id_vehiculo y matricula sean obligatorios """
        with self.assertRaises(ValidationError):
            self.env['upocargo.vehiculo'].create({
                'capacidad': 5000,
                'estado': 'activo',
            })
        
        with self.assertRaises(ValidationError):
            self.env['upocargo.vehiculo'].create({
                'id_vehiculo': 'VEH1234',
                'capacidad': 5000,
                'estado': 'activo',
            })

    def test_relacion_many2many_con_mudanza(self):
        """ Verifica que un vehículo pueda estar relacionado con varias mudanzas """
        vehiculo = self.env['upocargo.vehiculo'].create({
            'matricula': '1234ABC',
            'capacidad': 5000,
            'estado': 'activo',
        })
        
        # Asignar una mudanza al vehículo
        vehiculo.mudanza = self.mudanza.id
        
        # Verificar que la mudanza esté asociada al vehículo
        self.assertIn(self.mudanza, vehiculo.mudanza, "La mudanza no está asociada correctamente al vehículo")

    def test_capacidad_vehiculo(self):
        """ Verifica que el campo capacidad acepte valores flotantes """
        vehiculo = self.env['upocargo.vehiculo'].create({
            'matricula': '1234ABC',
            'capacidad': 3500.5,
            'estado': 'activo',
        })
        self.assertEqual(vehiculo.capacidad, 3500.5, "La capacidad debería ser 3500.5")

    def test_estado_vehiculo(self):
        """ Verifica que el campo estado acepte valores seleccionados """
        vehiculo = self.env['upocargo.vehiculo'].create({
            'matricula': '1234ABC',
            'capacidad': 5000,
            'estado': 'activo',  # Aquí debería haber una lista de opciones posibles
        })
        self.assertEqual(vehiculo.estado, 'activo', "El estado del vehículo no es correcto")
