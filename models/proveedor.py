from odoo import models, fields, api
import random
import string

class Proveedor(models.Model):
    _name = 'upocargo.proveedor'
    _inherit = 'upocargo.cliente'
    _description = 'Proveedores UPOCARGO'

    #Campos Base
    id_proveedor = fields.Char(string="Id del proveedor", required=True,help="Identificador de un proveedor", default=lambda self: self._generate_id_proovedor(), readonly=True)
    entidad = fields.Char(string="Nombre entidad", required=True, help="Nombre de una entidad")

    #Campos relacionales
    servicios_adicionales= fields.Many2one('upocargo.servicios_adicionales' ,string='serviciosAdicionales')

    @staticmethod
    def _generate_id_proovedor():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))