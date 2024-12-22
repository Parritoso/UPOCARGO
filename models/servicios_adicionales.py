from odoo import models, fields, api
import random
import string

class ServiciosAdicionales(models.Model):
    _name = 'upocargo.servicios_adicionales'
    _description = 'Servicios Adicionales UPOCARGO'
    _rec_name = 'id_servicios'

    #Campos Base
    id_servicios = fields.Char(string="Id del servicio adicional", required=True,help="Identificador del servicio adicional", default=lambda self: self._generate_id_servicio_adicional(), readonly=True)
    tipo = fields.Char(string="Tipo de Servicio", required=True, help="Tipo de Servicio")
    estado = fields.Selection([('true','En curso'),
                                ('false','No activo')],"Estado")
    aplicable_a = fields.Selection([
        ('mudanza', 'Mudanza'),
        ('almacenamiento', 'Almacenamiento'),
        ('ambos', 'Ambos')
    ], string="Aplicable a", required=True, default='ambos', help="Indica si el servicio adicional se aplica a mudanza, almacenamiento o ambos.")

    precio_base = fields.Float(string="Precio Base", required=True, help="Precio proporcionado por el proveedor para el servicio adicional")
    precio_final = fields.Float(string="Precio Final", compute="_compute_precio_final", store=True, help="Precio final con el 5% adicional")

    #Campos relacionales
    proveedores = fields.One2many('upocargo.proveedor','servicios_adicionales' ,string='proveedores')
    clientes = fields.Many2many('upocargo.cliente', 'rel_servicio_cliente', 'servicio_id', 'cliente_id', string="Clientes")

    @staticmethod
    def _generate_id_servicio_adicional():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    @api.depends('precio_base')
    def _compute_precio_final(self):
        for record in self:
            record.precio_final = record.precio_base * 1.05  # Añadimos un 5%