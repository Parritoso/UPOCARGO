# -*- coding: utf-8 -*-
from odoo import models, fields, api
import random
import string
from datetime import datetime

class Mudanza(models.Model):
    _name = 'upocargo.mudanza'
    _description = 'Mudanzas UPOCARGO'

    #Campos Base
    id_mudanza = fields.Char(string="Id de la mudanza", required=True, help="Identificador de la mudanza", default=lambda self: self._generate_id_mudanza(), readonly=True)
    fecha = fields.Date('Inicio', required=True, autodate=True)
    dirOrigen = fields.Char(string="Direccion Origen", required=True, help="Direccion del Cliente")
    dirDestino = fields.Char(string="Direccion Destino", required=True, help="Direccion del Cliente")
    estado = fields.Selection([('planificado','Planificado'),('iniciado','Iniciado'),('proceso','En proceso'),('almacenado','Bienes Almacenados'),('transportando','Transportando'),('finalizado','Finalizado'),('cancelado','Cancelado')],'Estado')

    #Campos relacionales
    cliente = fields.Many2one('upocargo.cliente', string="Cliente")
    #vehiculos = fields.Many2many('upocargo.vehiculos', string="Vehiculos")
    #empleados = fields.Many2many('upocargo.empleados', string="Empleados")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('id_mudanza'):
                creation_date = datetime.now().strftime('%d-%m-%Y')
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                vals['id_mudanza'] = f"{creation_date}-{random_suffix}"
        return super(Mudanza, self).create(vals_list)
    
    @staticmethod
    def _generate_id_mudanza():
        creation_date = datetime.now().strftime('%d-%m-%Y')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{creation_date}-{random_suffix}"