# -*- coding: utf-8 -*-
from odoo import models, fields, api
import random
import string

class Almacenamiento(models.Model):
    _name = 'upocargo.almacenamiento'
    _description = 'Almacenamiento UPOCARGO'

    #Campos Base
    id_almacenamiento = fields.Char(string="Id del Almacenamiento", required=True, help="Identificador del Almacenamiento", default=lambda self: self._generate_id_almacenamiento(), readonly=True)
    fecha_ingreso = fields.Date('Ingreso', required=True, autodate=True)
    fecha_salida = fields.Date('Salida', required=True, autodate=True)
    estado = fields.Selection([])

    #Campos relacionales
    #bienes_almacenados = fields.One2many('upocargo.bienes_almacenados', 'id_almacenamiento', string="Bienes Almacenados")
    cliente = fields.Many2one('upocargo.cliente', string="Cliente")

    @staticmethod
    def _generate_id_almacenamiento():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))