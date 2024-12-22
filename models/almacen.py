from odoo import models, fields, api, exceptions
import random
import string
import threading
import time
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

def _simular_sensores(self):
        #with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            while True:
                for record in self:
                    record.temperatura_actual = random.uniform(self.temp_min,self.tamaño_maximo)
                    record.humedad_actual = random.uniform(self.humedad_min,self.humedad_max)
                    new_cr.commit()

def _start_iot_simulation(self):
    while True:
        self._simular_sensores()
        time.sleep(5)
            
class Almacen(models.Model):
    _name = 'upocargo.almacen'
    _description = 'Almacén UPOCARGO'
    _rec_name = 'name'
    _iot_thread = threading.Thread(target=_start_iot_simulation)
    _iot_thread.daemon = True

    #Campos base
    id_almacen = fields.Char(string="ID del Almacén", required=True, help="Identificador del almacén", default=lambda self: self._generate_id_almacen(), readonly=True)
    name = fields.Char(string="Lugar del Almacén",required=True, help="Ciudad, pueblo o pais donde se encuentra el almacen")
    tamaño_maximo = fields.Float(string="Tamaño máximo", required=True, help="Tamaño total ocupado por los bienes almacenados.")
    tamaño_ocupado = fields.Float(string="Tamaño Ocupado", compute='_compute_tamaño_ocupado', store=True, readonly=True)

    #Campos relacionales
    almacenamiento_id = fields.Many2one('upocargo.almacenamiento',string="Almacenamiento asociado",ondelete='cascade')
    bienes_almacenados = fields.One2many(related='almacenamiento_id.bienes_almacenados',string="Bienes almacenados",readonly=True)

    #Campos IoT simulados
    temperatura_actual = fields.Float(string="Temperatura (ºC)",readonly=True,help="Lectura actual simulada de temperatura del almacén.", track_visibility='onchange')
    humedad_actual = fields.Float(string="Humedad (%)",readonly=True,help="Lectura actual simulada de humedad del almacén.", track_visibility='onchange')
    temp_min = fields.Float(string="Temperatura mínima permitida", help="Temperatura mínima permitida para los bienes almacenados.")
    temp_max = fields.Float(string="Temperatura máxima permitida", help="Temperatura máxima permitida para los bienes almacenados.")
    humedad_min = fields.Float(string="Humedad mínima permitida", help="Humedad mínima permitida para los bienes almacenados.")
    humedad_max = fields.Float(string="Humedad máxima permitida", help="Humedad máxima permitida para los bienes almacenados.")

    @api.model
    def create(self, vals):
        new_record = super(Almacen, self).create(vals)
        
        #self._start_iot_thread(new_record)
        
        return new_record
    
    def _start_iot_thread(self, record):
        _logger.info(f"Iniciando la simulación IoT para el almacén {record.id_almacen}")
        if not hasattr(record, '_iot_thread') or not self._iot_thread.is_alive():
            _logger.info(f"Creando nuevo hilo para el almacén {record.id_almacen}")
            #_iot_thread = threading.Thread(target=record._start_iot_simulation)
            #_iot_thread.daemon = True
            self._iot_thread.start()
        else:
        # Log o mensaje de advertencia si el hilo ya está en ejecución
            _logger.info(f"El hilo de IoT ya está en ejecución para el almacén {record.id_almacen}")

    def write(self, vals):
        res = super(Almacen, self).write(vals)
        #for record in self:
            #self._start_iot_thread(record)
        return res

    @staticmethod
    def _generate_id_almacen():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    @api.depends('almacenamiento_id.bienes_almacenados')
    def _compute_tamaño_ocupado(self):
        for record in self:
            if record.almacenamiento_id:
                total_tamaño = sum(bien.tamanyo for bien in record.almacenamiento_id.bienes_almacenados)
                record.tamaño_ocupado = total_tamaño
                if total_tamaño > record.tamaño_maximo:
                    raise exceptions.ValidationError(
                        f"El tamaño ocupado ({total_tamaño}) supera el tamaño máximo permitido ({record.tamaño_maximo})."
                    )
            else:
                record.tamaño_ocupado = 0

    def _start_iot_simulation_for_all(self):
        almacenes = self.search([])  # Obtén todos los almacenes existentes
        for almacen in almacenes:
            #self._start_iot_thread(almacen)
            return
        
    @api.model
    def get_ocupacion_by_fecha(self, fecha):
        if not fecha:
            return []
        
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        almacenamientos = self.env['upocargo.almacenamiento'].search([
            ('fecha_ingreso', '<=', fecha),  # Fecha de ingreso antes o igual a la fecha proporcionada
            ('fecha_salida', '>=', fecha)  # Fecha de salida después o igual a la fecha proporcionada
        ])

        ocupacion = {}

        for almacenamiento in almacenamientos:
            # Calcular el tamaño total ocupado en ese almacenamiento
            total_tamano = sum(bien.tamanyo * bien.cantidad for bien in almacenamiento.bienes_almacenados)

            # Agrupar la ocupación por almacén (almacen.almacen es el campo de relación)
            if almacenamiento.almacen.id not in ocupacion:
                ocupacion[almacenamiento.almacen.id] = {
                    'id_almacen': almacenamiento.almacen.id,
                    'nombre_almacen': almacenamiento.almacen.name,
                    'ocupacion': total_tamano,
                    'tamaño_maximo': almacenamiento.almacen.tamaño_maximo,
                }
            else:
                ocupacion[almacenamiento.almacen.id]['ocupacion'] += total_tamano

        # Retornar la ocupación por almacén
        result = []
        for data in ocupacion.values():
            porcentaje_ocupacion = (data['ocupacion']/ data['tamaño_maximo']) *100 if data['tamaño_maximo'] > 0 else 0
            result.append({
                'id_almacen': data['id_almacen'],
                'nombre_almacen': data['nombre_almacen'],
                'ocupacion': data['ocupacion'],
                'porcentaje_ocupacion': round(porcentaje_ocupacion,2),
            })
        return result#[{'id_almacen': data['id_almacen'], 'nombre_almacen': data['nombre_almacen'], 'ocupacion': data['ocupacion']} for data in ocupacion.values()]