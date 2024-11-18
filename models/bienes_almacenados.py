from odoo import models, fields, api
import random
import string

class BienesAlmacenados(models.Model):
    _name = 'upocargo.bienes_almacenados'
    _description = 'Bienes Almacenados UPOCARGO'

    #Campos Base
    id_bien = fields.Char(string="Id bien almacenado", required=True,help="Identificador de un bien almacenado", default=lambda self: self._generate_id_bien(), readonly=True)
    descripcion = fields.Char(string="Descripcion bien", required=True, help="Descripcion de un bien alamcenado")
    peso = fields.Float("Peso",help="Peso del bien almacenado")
    tamaño = fields.Float("Tamaño",help="Tamaño del bien almacenado")
    

    #Campos relacionales
    almacenamiento= fields.Many2one('upocargo.almacenamiento' ,string='Almacenamiento')

    @staticmethod
    def _generate_id_bien():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))