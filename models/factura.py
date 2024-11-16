from odoo import models, fields, api
import random
import string

class Factura(models.Model):
    _name = 'upocargo.factura'
    _description = 'Facturas UPOCARGO'

    #Campos base
    id_factura = fields.Char(string="Id de la factura", required=True, help="Identificador de la factura", default=lambda self: self._generate_id_factura(), readonly=True)
    precio = fields.Float("Precio", help="Precio de la factura")

    #Campos relacionales
    mudanza = fields.One2one('upocargo.mudanza', string='mudanza')

    @staticmethod
    def _generate_id_factura():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))