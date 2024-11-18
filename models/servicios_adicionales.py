from odoo import models, fields, api
import random
import string

class ServiciosAdicionales(models.Model):
    _name = 'upocargo.servicios_adicionales'
    _description = 'Servicios Adicionales UPOCARGO'

    #Campos Base
    id_servicios = fields.Char(string="Id del servicio adicional", required=True,help="Identificador del servicio adicional", default=lambda self: self._generate_id_servicio_adicional(), readonly=True)
    tipo = fields.Char(string="Tipo de Servicio", required=True, help="Tipo de Servicio")
    estado = fields.Selection([('true','En curso'),
                                ('false','No activo')],"Estado")

    #Campos relacionales
    proveedores = fields.One2many('upocargo.proveedor','servicios_adicionales' ,string='proveedores')
    cliente= fields.Many2one('upocargo.cliente' ,string='clientes')

    @staticmethod
    def _generate_id_servicio_adicional():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))