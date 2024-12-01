from odoo import models, fields, api, exceptions
import random
import string

class BienesAlmacenados(models.Model):
    _name = 'upocargo.bienes_almacenados'
    _description = 'Bienes Almacenados UPOCARGO'

    #Campos Base
    id_bien = fields.Char(string="Id bien almacenado", required=True,help="Identificador de un bien almacenado", default=lambda self: self._generate_id_bien(), readonly=True)
    descripcion = fields.Char(string="Descripcion bien", required=True, help="Descripcion de un bien alamcenado")
    peso = fields.Float(string="Peso",help="Peso del bien almacenado")
    tamanyo = fields.Float(string="Tamaño",help="Tamaño del bien almacenado", required=True)
    cantidad = fields.Integer(string="Cantidad", required=True)
    

    #Campos relacionales
    almacenamiento= fields.Many2one('upocargo.almacenamiento' ,string='Almacenamiento')

    condicion_especial = fields.Boolean(string="Condición Especial", help="Indica si el bien tiene una condición especial asociada a sensores IoT.")
    tipo_sensor = fields.Selection([
        ('temperatura', 'Temperatura'),
        ('humedad', 'Humedad'),
        ('otro', 'Otro')
    ], string="Tipo de Sensor", help="Tipo de sensor relacionado con el bien almacenado", default="temperatura")
    valor_sensor_min = fields.Float(string="Valor mínimo del sensor", help="Valor mínimo para el sensor, como la temperatura mínima permitida.")
    valor_sensor_max = fields.Float(string="Valor máximo del sensor", help="Valor máximo para el sensor, como la temperatura máxima permitida.")

    @staticmethod
    def _generate_id_bien():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    #@api.constrains('condicion_especial', 'tipo_sensor', 'valor_sensor_min', 'valor_sensor_max', 'almacenamiento')
    #def _check_condiciones_sensor(self):
    #    for record in self:
    #        if record.condicion_especial:
    #            almacen = record.almacenamiento.almacen  # Obtener el almacén relacionado
    #            almacen = self.env['upocargo.almacen'].search([('id','=',almacen.id)])
    #            if almacen:
    #                # Comprobar si los valores del sensor están dentro de los rangos del almacén
    #                if record.tipo_sensor == 'temperatura':
    #                    if not (almacen.temp_min <= record.valor_sensor_min <= almacen.temp_max):
    #                        raise exceptions.ValidationError(f"La temperatura mínima ({record.valor_sensor_min}ºC) no está dentro del rango permitido en el almacén.")
    #                    if not (almacen.temp_min <= record.valor_sensor_max <= almacen.temp_max):
    #                        raise exceptions.ValidationError(f"La temperatura máxima ({record.valor_sensor_max}ºC) no está dentro del rango permitido en el almacén.")
    #                elif record.tipo_sensor == 'humedad':
    #                    if not (almacen.humedad_min <= record.valor_sensor_min <= almacen.humedad_max):
    #                        raise exceptions.ValidationError(f"La humedad mínima ({record.valor_sensor_min}%) no está dentro del rango permitido en el almacén.")
    #                    if not (almacen.humedad_min <= record.valor_sensor_max <= almacen.humedad_max):
    #                        raise exceptions.ValidationError(f"La humedad máxima ({record.valor_sensor_max}%) no está dentro del rango permitido en el almacén.")
    #@api.depends('valor_sensor_min', 'valor_sensor_max', 'tipo_sensor')
    #def _compute_cumple_condicion(self):
        #for record in self:
            # Aquí puede ir la lógica para verificar si el valor del sensor cumple con las condiciones
            #if record.tipo_sensor == 'temperatura':
                #if record.valor_sensor_min is not False and record.valor_sensor_max is not False:
                    # Comprobar que los valores están en el rango permitido
                    #record.cumple_condicion = record.valor_sensor_min >= -5 and record.valor_sensor_max <= 30
                #else:
                    #record.cumple_condicion = False
            #else:
                #record.cumple_condicion = True