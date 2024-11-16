from odoo import models, fields, api
import random
import string

class Empleado(models.Model):
    _name = 'upocargo.empleado'
    _description = 'Empleados UPOCARGO'

    #Campos base
    id_empleado = fields.Char(string="Id del empleado", required=True, help="Identificador del empleado", default=lambda self: self._generate_id_empleado(), readonly=True)
    nombre = fields.Char(string="Nombre", required=True, help="Nombre del Empleado")
    telefono = fields.Integer("Telefono", help="Telefono del Empleado")
    cargo = fields.Selection([])
    email = fields.Char(string="Email", required=True, help="Email del Empleado")

    #Campos relacionales
    mudanza = fields.Many2many('upocargo.mudanza', string='mudanza')

    @staticmethod
    def _generate_id_empleado():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))