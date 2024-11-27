from odoo import models, fields, api, exceptions
import random
import string

class Factura(models.Model):
    _name = 'upocargo.factura'
    _description = 'Facturas UPOCARGO'

    #Campos base
    id_factura = fields.Char(string="Id de la factura", required=True, help="Identificador de la factura", default=lambda self: self._generate_id_factura(), readonly=True)
    #Editado para poder formatearlo como moneda
    currency_id = fields.Many2one('res.currency', string="Moneda",default=lambda self: self.env.user.company_id.currency_id)
    precio = fields.Monetary("Precio",currency_field='currency_id', help="Precio de la factura")

    #Campos relacionales #Simulación de Campo One2one
    mudanza_id = fields.Many2one('upocargo.mudanza',string='Mudanza', ondelete='restrict')
    _sql_constraits = [
        ('unique_mudanza_factura', 'UNIQUE(id_mudanza)','¡Cada factura solo puede tener una mudanza asociada!')
    ]

    @api.model
    def create(self, vals):
        if 'id_mudanza' in vals:
            existing_factura = self.search([('id_mudanza', '=', vals['id_mudanza'])])
            if existing_factura:
                raise exceptions.ValidationError('Esta Mudanza ya esta vinculada a otra factura.')
        return super(Factura, self).create(vals)
    
    def write(self,vals):
        if 'id_mudanza' in vals:
            existing_factura = self.search([('id_mudanza', '=', vals['id_mudanza'])])
            if existing_factura:
                raise exceptions.ValidationError('Esta Mudanza ya esta vinculada a otra factura.')
        return super(Factura, self).write(vals)

    @staticmethod
    def _generate_id_factura():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    def compute_desglose_gastos(self):
        desglose=[]
        for record in self:
            if record.mudanza_id:
                vehiculos_extra = max(0, len(record.mudanza_id.vehiculos)-1) *100
                empleados_extra = max(0, len(record.mudanza_id.empleados)-2) *50
                coste_base = record.precio -vehiculos_extra -empleados_extra
                desglose.append({
                    "concepto": "Costo base",
                    "valor": coste_base
                })
                desglose.append({
                    "concepto": "Vehículos adicionales",
                    "valor": vehiculos_extra
                })
                desglose.append({
                    "concepto": "Empleados adicionales",
                    "valor": empleados_extra
                })
        return desglose