from odoo.tests import TransactionCase
import time

class TestAlmacen(TransactionCase):
    def test_create_almacen(self):
        # Crear un almacén con valores válidos
        almacen = self.env['upocargo.almacen'].create({
            'name': 'Almacén Central',
            'tamaño_maximo': 1000.0,
            'temp_min': 5.0,
            'temp_max': 25.0,
            'humedad_min': 30.0,
            'humedad_max': 70.0
        })
        
        self.assertEqual(almacen.name, 'Almacén Central')
        self.assertEqual(almacen.tamaño_maximo, 1000.0)
        self.assertEqual(almacen.temp_min, 5.0)
        self.assertEqual(almacen.temp_max, 25.0)
        self.assertEqual(almacen.humedad_min, 30.0)
        self.assertEqual(almacen.humedad_max, 70.0)
        self.assertTrue(almacen.id_almacen)  # Verificar que el ID es generado

class TestTamañoOcupado(TransactionCase):

    def test_compute_tamaño_ocupado(self):
        # Crear almacén y almacenamiento asociado
        almacen = self.env['upocargo.almacen'].create({
            'name': 'Almacén A',
            'tamaño_maximo': 1000.0,
            'temp_min': 10.0,
            'temp_max': 20.0,
            'humedad_min': 40.0,
            'humedad_max': 60.0
        })
        
        almacenamiento = self.env['upocargo.almacenamiento'].create({
            'almacen': almacen.id,
            'fecha_ingreso': '2024-01-01',
            'fecha_salida': '2024-12-31'
        })
        
        # Crear bienes almacenados
        bien1 = self.env['upocargo.bien'].create({
            'tamanyo': 100.0,
            'cantidad': 5
        })
        
        bien2 = self.env['upocargo.bien'].create({
            'tamanyo': 200.0,
            'cantidad': 3
        })
        
        # Asociar bienes al almacenamiento
        almacenamiento.write({
            'bienes_almacenados': [(6, 0, [bien1.id, bien2.id])]
        })
        
        # Calcular tamaño ocupado
        almacen._compute_tamaño_ocupado()
        
        # Verificar el tamaño ocupado
        self.assertEqual(almacen.tamaño_ocupado, 1300.0)
        
        # Verificar que se lanza una excepción si el tamaño ocupado excede el máximo
        with self.assertRaises(ValidationError):
            almacenamiento.write({'bienes_almacenados': [(6, 0, [bien1.id, bien2.id, bien1.id])]})



class TestSimulacionSensores(TransactionCase):

    def test_simulacion_sensores(self):
        # Crear un almacén con valores válidos
        almacen = self.env['upocargo.almacen'].create({
            'name': 'Almacén B',
            'tamaño_maximo': 1000.0,
            'temp_min': 5.0,
            'temp_max': 25.0,
            'humedad_min': 30.0,
            'humedad_max': 70.0
        })

        # Comprobar si los valores de temperatura y humedad son simulados correctamente
        initial_temp = almacen.temperatura_actual
        initial_humidity = almacen.humedad_actual
        
        # Iniciar el hilo de simulación (esto normalmente debería hacerse de forma asíncrona, pero para pruebas usamos un delay corto)
        almacen._start_iot_simulation_for_all()
        
        time.sleep(2)  # Esperamos un par de segundos para que se simule alguna lectura
        
        # Verificar que las lecturas de temperatura y humedad hayan cambiado
        self.assertNotEqual(almacen.temperatura_actual, initial_temp)
        self.assertNotEqual(almacen.humedad_actual, initial_humidity)
        
        # Verificar que los valores están dentro del rango permitido
        self.assertGreaterEqual(almacen.temperatura_actual, almacen.temp_min)
        self.assertLessEqual(almacen.temperatura_actual, almacen.temp_max)
        self.assertGreaterEqual(almacen.humedad_actual, almacen.humedad_min)
        self.assertLessEqual(almacen.humedad_actual, almacen.humedad_max)

class TestOcupacionPorFecha(TransactionCase):

    def test_ocupacion_por_fecha(self):
        # Crear almacén
        almacen = self.env['upocargo.almacen'].create({
            'name': 'Almacén C',
            'tamaño_maximo': 2000.0,
            'temp_min': 10.0,
            'temp_max': 20.0,
            'humedad_min': 40.0,
            'humedad_max': 60.0
        })
        
        # Crear almacenamiento y bienes almacenados
        almacenamiento = self.env['upocargo.almacenamiento'].create({
            'almacen': almacen.id,
            'fecha_ingreso': '2024-12-01',
            'fecha_salida': '2024-12-31'
        })
        
        bien1 = self.env['upocargo.bien'].create({
            'tamanyo': 100.0,
            'cantidad': 5
        })
        
        almacenamiento.write({'bienes_almacenados': [(6, 0, [bien1.id])]})

        # Obtener ocupación por fecha
        ocupacion = almacen.get_ocupacion_by_fecha('2024-12-10')
        
        # Verificar que la ocupación está calculada correctamente
        self.assertEqual(len(ocupacion), 1)
        self.assertEqual(ocupacion[0]['ocupacion'], 500.0)
        self.assertEqual(ocupacion[0]['id_almacen'], almacen.id)

