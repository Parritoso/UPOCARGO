from odoo import models, fields, api, exceptions
import random
import string
import json

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
    almacenamiento_id = fields.Many2one('upocargo.almacenamiento',string='Almacenamiento', ondelete='restrict')
    _sql_constraits = [
        ('unique_mudanza_factura', 'UNIQUE(id_mudanza)','¡Cada factura solo puede tener una mudanza asociada!')
    ]

    desglose_gastos = fields.Json(string="Desglose de gastos", default=lambda self: [])

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
    
    @api.constrains('id_mudanza','almacenamiento_id')
    def _check_unique_relation(self):
        for record in self:
            if record.mudanza_id and record.almacenamiento_id:
                raise exceptions.ValidationError('Una factura no puede estar asociada a una mudanza y un almacenamiento al mismo tiempo.')

    def agregar_gasto(self, concepto, valor):
        for record in self:
            desglose = json.loads(record.desglose_gastos or "[]")
            desglose.append({"concepto": concepto, "valor": valor})
            record.desglose_gastos = json.dumps(desglose)

    def eliminar_gasto(self,concepto):
        for record in self:
            desglose = json.load(record.desglose_gastos or "[]")
            desglose = [item for item in desglose if item['concepto'] != concepto]

    def actualizar_gasto(self, concepto, nuevo_valor):
        for record in self:
            desglose = json.loads(record.desglose_gastos or "[]")
            for item in desglose:
                if item['concepto'] == concepto:
                    item['valor'] = nuevo_valor
                    break
            record.desglose_gastos = json.dumps(desglose)

    def obtener_desglose_gastos(self):
        if not isinstance(self.desglose_gastos, str):
            self.desglose_gastos = json.dumps(self.desglose_gastos)
        if isinstance(self.desglose_gastos, str):
            try:
                desglose = json.loads(self.desglose_gastos)
            except json.JSONDecodeError:
                desglose = []
        return desglose