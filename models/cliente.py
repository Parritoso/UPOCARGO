# -*- coding: utf-8 -*-
from odoo import models, fields, api
import random
import string
from datetime import datetime,timedelta

class Cliente(models.Model):
    _name = 'upocargo.cliente'
    _description = 'Clientes UPOCARGO'

    #Campos Base
    id_cliente = fields.Char(string="Id del Cliente", required=True, help="Identificador del Cliente", default=lambda self: self._generate_id_cliente(), readonly=True)
    name = fields.Char(string="Nombre", required=True, help="Nombre del Cliente")
    direccion = fields.Char(string="Direccion", required=True, help="Direccion del Cliente")
    telefono = fields.Integer("Telefono", help="Telefono del Cliente")
    email = fields.Char(string="Email", help="Email del Cliente")

    #Campos Computados
    mudanza = fields.Char(compute='_compute_display_next_mudanza', store=True, readonly=True)

    #Campos relacionales
    mudanzas = fields.One2many('upocargo.mudanza','cliente', string="Mudanzas")
    almacenamiento = fields.One2many('upocargo.almacenamiento','cliente', string="Almacenamiento")
    #servicios_adicionales = fields.One2many('upocargo.servicios_adicionales', string="Servicios Adicionales")

    @staticmethod
    def _generate_id_cliente():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

    @api.depends('mudanzas')
    def _compute_display_next_mudanza(self):
        today = datetime.now
        for record in self:
            mudanzas_futuras = record.mudanzas.filtered(lambda m: m.fecha and m.fecha >= today)
            if mudanzas_futuras:
                mudanza_cercana = min(mudanzas_futuras, key=lambda m: m.fecha)
                dias_restantes = (mudanza_cercana.fecha -today).days
                record.mudanza = f"ID: {mudanza_cercana.id_mudanza}, Dias restantes: {dias_restantes}"
            else:
                record.mudanza = "No hay mudanzas proximas"