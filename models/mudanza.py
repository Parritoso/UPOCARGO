# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
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
    vehiculos = fields.Many2many('upocargo.vehiculo', string="Vehiculos")
    empleados = fields.Many2many('upocargo.empleado', string="Empleados")
        #Simulación de Campo One2one
    factura = fields.Many2one('upocargo.factura', string='Factura', ondelete='restrict')
    _sql_constraits = [
        ('unique_factura_mudanza', 'UNIQUE(id_factura)','¡Cada Mudanza solo puede tener una factura asociada!')
    ]

    @api.model
    def create(self, vals):
        if 'id_factura' in vals:
            existing_mudanza = self.search([('id_factura', '=', vals['id_factura'])])
            if existing_mudanza:
                raise exceptions.ValidationError('Esta factura ya esta vinculada a otra mudanza.')
        mudanza = super(Mudanza, self).create(vals)
        factura_vals = {
            'id_factura': self.env['upocargo.factura']._generate_id_factura(),
            'precio': 0.0,
            'currency_id': self.env.user.company_id.currency_id.id,
            'mudanza_id': mudanza.id,
        }
        factura = self.env['upocargo.factura'].create(factura_vals)
        if not factura or isinstance(factura, bool):
            raise exceptions.ValidationError('No se puedo crear la factura asociada')
        mudanza.factura = factura.id
        return mudanza
    
    def write(self,vals):
        if 'id_factura' in vals:
            existing_mudanza = self.search([('id_factura', '=', vals['id_factura'])])
            if existing_mudanza:
                raise exceptions.ValidationError('Esta factura ya esta vinculada a otra mudanza.')
        return super(Mudanza, self).write(vals)
    
    @staticmethod
    def _generate_id_mudanza():
        creation_date = datetime.now().strftime('%d-%m-%Y')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{creation_date}-{random_suffix}"