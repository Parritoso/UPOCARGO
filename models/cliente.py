# -*- coding: utf-8 -*-
from odoo import models, fields, api
import random
import string
import hashlib
import os
from datetime import datetime,date

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
    servicios_adicionales = fields.One2many('upocargo.servicios_adicionales','cliente', string="Servicios Adicionales")

    #Campos internos
    password = fields.Char(string="Contraseña", groups="base.group_no_one")
    salt_password = fields.Char(string="Salt", groups="base.group_no_one")

    @staticmethod
    def _generate_id_cliente():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

    @api.depends('mudanzas')
    def _compute_display_next_mudanza(self):
        today = date.today()
        for record in self:
            mudanzas_futuras = record.mudanzas.filtered(lambda m: m.fecha and m.fecha >= today)
            if mudanzas_futuras:
                mudanza_cercana = min(mudanzas_futuras, key=lambda m: m.fecha)
                dias_restantes = (mudanza_cercana.fecha -today).days
                record.mudanza = f"ID: {mudanza_cercana.id_mudanza}, Dias restantes: {dias_restantes}"
            else:
                record.mudanza = "No hay mudanzas proximas"
    
    def _check_password(self, plain_password):
        if not self.password or not self.salt_password:
            return False
        salted_password = (plain_password + self.salt_password).encode('utf-8')
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return hashed_password == self.password #bcrypt.checkpw(plain_password.encode('utf-8'),self.password.encode('utf-8'))
    
    def _encrypt_password(self, plain_password, salt=None):
        if not salt:
            salt = os.urandom(16).hex()
        salted_password = (plain_password + salt).encode('utf-8')
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return hashed_password, salt#bcrypt.hashpw(plain_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    
    @api.model
    def create(self,vals):
        if 'password' in vals and vals['password']:
            hased_password, salt = self._encrypt_password(vals['password'])
            vals['password'] = hased_password
            vals['salt_password'] = salt
        return super(Cliente,self).create(vals)
    def write(self,vals):
        if 'password' in vals and vals['password']:
            hased_password, salt = self._encrypt_password(vals['password'])
            vals['password'] = hased_password
            vals['salt_password'] = salt
        return super(Cliente,self).write(vals)