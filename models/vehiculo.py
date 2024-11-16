from odoo import models, fields, api
import random
import string

class Vehiculo(models.Model):
    _name = 'upocargo.vehiculo'
    _description = 'Vehiculos UPOCARGO'

    #Campos Base
    id_vehiculo = fields.Char(string="Id del vehículo", required=True, help="Identificador del vehículo", default=lambda self: self._generate_id_vehiculo(), readonly=True)
    matricula = fields.Char(string="Matricula", required=True, help="Matricula del Vehiculo")
    capacidad = fields.Float("Capacidad", help="Capacidad del Vehiculo")
    estado = fields.Selection([])

    #Campos relacionales
    mudanza = fields.Many2many('upocargo.mudanza', string='mudanza')

    @staticmethod
    def _generate_id_vehiculo():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))