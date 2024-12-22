from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date


class TestMudanza(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear los registros base necesarios para la prueba (clientes, empleados, vehículos, etc.)
        self.cliente = self.env['upocargo.cliente'].create({
            'name': 'Cliente de prueba',
            'email': 'cliente@prueba.com'
        })
        self.empleado_1 = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
        self.empleado_2 = self.env['upocargo.empleado'].create({'name': 'Empleado 2'})
        self.empleado_3 = self.env['upocargo.empleado'].create({'name': 'Empleado 3'})
        self.vehiculo_1 = self.env['upocargo.vehiculo'].create({'name': 'Vehículo 1'})
        self.vehiculo_2 = self.env['upocargo.vehiculo'].create({'name': 'Vehículo 2'})
        self.vehiculo_3 = self.env['upocargo.vehiculo'].create({'name': 'Vehículo 3'})
        self.servicio_adicional = self.env['upocargo.servicios_adicionales'].create({
            'tipo': 'Servicio Extra',
            'precio_final': 200
        })

    def test_creacion_mudanza_sin_fecha(self):
        """ Verifica que no se puede crear una mudanza sin fecha """
        with self.assertRaises(ValidationError):
            self.env['upocargo.mudanza'].create({
                'dirOrigen': 'Calle Falsa 123',
                'dirDestino': 'Avenida Siempre Viva 456',
                'cliente': self.cliente.id,
            })

    def test_creacion_mudanza_sin_vehiculos_empleados(self):
        """ Verifica que no se puede crear una mudanza sin al menos un vehículo y dos empleados """
        with self.assertRaises(ValidationError):
            self.env['upocargo.mudanza'].create({
                'fecha': date.today(),
                'dirOrigen': 'Calle Falsa 123',
                'dirDestino': 'Avenida Siempre Viva 456',
                'cliente': self.cliente.id,
                'vehiculos': [(6, 0, [])],  # Sin vehículos
                'empleados': [(6, 0, [])],  # Sin empleados
            })

    def test_creacion_mudanza_conflicto_vehiculos(self):
        """ Verifica que no se puede crear una mudanza con vehículos ocupados en la misma fecha """
        mudanza_existente = self.env['upocargo.mudanza'].create({
            'fecha': date.today(),
            'dirOrigen': 'Calle Falsa 123',
            'dirDestino': 'Avenida Siempre Viva 456',
            'cliente': self.cliente.id,
            'vehiculos': [(6, 0, [self.vehiculo_1.id])],
            'empleados': [(6, 0, [self.empleado_1.id, self.empleado_2.id])],
        })
        with self.assertRaises(ValidationError):
            self.env['upocargo.mudanza'].create({
                'fecha': date.today(),
                'dirOrigen': 'Calle Falsa 123',
                'dirDestino': 'Avenida Siempre Viva 456',
                'cliente': self.cliente.id,
                'vehiculos': [(6, 0, [self.vehiculo_1.id])],  # Conflicto con vehículo ya asignado
                'empleados': [(6, 0, [self.empleado_1.id, self.empleado_2.id])],
            })

    def test_calculo_factura_con_servicios_adicionales(self):
        """ Verifica que el costo de la factura se calcule correctamente con los servicios adicionales """
        mudanza = self.env['upocargo.mudanza'].create({
            'fecha': date.today(),
            'dirOrigen': 'Calle Falsa 123',
            'dirDestino': 'Avenida Siempre Viva 456',
            'cliente': self.cliente.id,
            'vehiculos': [(6, 0, [self.vehiculo_1.id, self.vehiculo_2.id])],
            'empleados': [(6, 0, [self.empleado_1.id, self.empleado_2.id])],
            'servicios_adicionales': [(6, 0, [self.servicio_adicional.id])],
        })
        factura = mudanza.factura
        self.assertEqual(factura.precio, 200)  # Verificar el precio base más el costo del servicio adicional

    def test_cancelar_mudanza(self):
        """ Verifica que no se puede cancelar una mudanza que ya está en estado 'cancelado' """
        mudanza = self.env['upocargo.mudanza'].create({
            'fecha': date.today(),
            'dirOrigen': 'Calle Falsa 123',
            'dirDestino': 'Avenida Siempre Viva 456',
            'cliente': self.cliente.id,
            'vehiculos': [(6, 0, [self.vehiculo_1.id])],
            'empleados': [(6, 0, [self.empleado_1.id, self.empleado_2.id])],
        })
        mudanza.estado = 'cancelado'
        with self.assertRaises(ValidationError):
            mudanza.action_cancelar_mudanza()

    def test_actualizacion_mudanza(self):
        """ Verifica que al modificar una mudanza, los costos adicionales se recalculen correctamente """
        mudanza = self.env['upocargo.mudanza'].create({
            'fecha': date.today(),
            'dirOrigen': 'Calle Falsa 123',
            'dirDestino': 'Avenida Siempre Viva 456',
            'cliente': self.cliente.id,
            'vehiculos': [(6, 0, [self.vehiculo_1.id])],
            'empleados': [(6, 0, [self.empleado_1.id, self.empleado_2.id])],
        })
        factura_inicial = mudanza.factura
        mudanza.write({
            'servicios_adicionales': [(6, 0, [self.servicio_adicional.id])],
        })
        self.assertNotEqual(mudanza.factura.precio, factura_inicial.precio)  # El precio debe haber cambiado debido a los servicios adicionales

def test_create_mudanza_success(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    mudanza_vals = {
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    }
    
    mudanza = self.env['upocargo.mudanza'].create(mudanza_vals)
    self.assertEqual(mudanza.estado, 'planificado')
    self.assertTrue(mudanza.id_mudanza)
    self.assertEqual(mudanza.cliente, cliente)

def test_create_mudanza_missing_fecha(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    mudanza_vals = {
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    }
    
    with self.assertRaises(exceptions.ValidationError):
        self.env['upocargo.mudanza'].create(mudanza_vals)

def test_create_mudanza_missing_vehiculos(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    mudanza_vals = {
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'empleados': [(6, 0, [empleado.id])],
    }
    
    with self.assertRaises(exceptions.ValidationError):
        self.env['upocargo.mudanza'].create(mudanza_vals)

def test_create_mudanza_missing_empleados(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    
    mudanza_vals = {
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
    }
    
    with self.assertRaises(exceptions.ValidationError):
        self.env['upocargo.mudanza'].create(mudanza_vals)

def test_create_mudanza_conflicto_vehiculos(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    # Crear una mudanza con ese vehiculo y fecha
    self.env['upocargo.mudanza'].create({
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    })
    
    # Intentar crear una nueva mudanza con el mismo vehiculo y fecha
    with self.assertRaises(exceptions.ValidationError):
        self.env['upocargo.mudanza'].create({
            'fecha': '2024-12-21',
            'dirOrigen': 'Calle 789, Ciudad',
            'dirDestino': 'Avenida 123, Ciudad',
            'cliente': cliente.id,
            'vehiculos': [(6, 0, [vehiculo.id])],
            'empleados': [(6, 0, [empleado.id])],
        })

def test_create_mudanza_conflicto_empleados(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    # Crear una mudanza con ese empleado y fecha
    self.env['upocargo.mudanza'].create({
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    })
    
    # Intentar crear una nueva mudanza con el mismo empleado y fecha
    with self.assertRaises(exceptions.ValidationError):
        self.env['upocargo.mudanza'].create({
            'fecha': '2024-12-21',
            'dirOrigen': 'Calle 789, Ciudad',
            'dirDestino': 'Avenida 123, Ciudad',
            'cliente': cliente.id,
            'vehiculos': [(6, 0, [vehiculo.id])],
            'empleados': [(6, 0, [empleado.id])],
        })

def test_update_mudanza_add_servicios_adicionales(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    mudanza = self.env['upocargo.mudanza'].create({
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    })
    
    servicio_adicional = self.env['upocargo.servicios_adicionales'].create({'tipo': 'Servicio A', 'precio_final': 100})
    
    mudanza.write({
        'servicios_adicionales': [(4, servicio_adicional.id)]
    })
    
    self.assertIn(servicio_adicional, mudanza.servicios_adicionales)

def test_update_mudanza_servicios_adicionales_cost(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    mudanza = self.env['upocargo.mudanza'].create({
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    })
    
    servicio_adicional = self.env['upocargo.servicios_adicionales'].create({'tipo': 'Servicio A', 'precio_final': 100})
    
    mudanza.write({
        'servicios_adicionales': [(4, servicio_adicional.id)]
    })
    
    self.assertEqual(mudanza.factura.precio, 100)  # Asegurarse de que la factura se actualice con el costo

def test_cancel_mudanza_success(self):
    cliente = self.env['upocargo.cliente'].create({'name': 'Cliente 1'})
    vehiculo = self.env['upocargo.vehiculo'].create({'name': 'Vehiculo 1'})
    empleado = self.env['upocargo.empleado'].create({'name': 'Empleado 1'})
    
    mudanza = self.env['upocargo.mudanza'].create({
        'fecha': '2024-12-21',
        'dirOrigen': 'Calle 123, Ciudad',
        'dirDestino': 'Avenida 456, Ciudad',
        'cliente': cliente.id,
        'vehiculos': [(6, 0, [vehiculo.id])],
        'empleados': [(6, 0, [empleado.id])],
    })
    
    mudanza.action_cancelar_mudanza()
    self.assertEqual(mudanza.estado, 'cancelado')

