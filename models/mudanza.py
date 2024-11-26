# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import random
import string
from datetime import datetime, date

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
    vehiculos = fields.Many2many('upocargo.vehiculo', string="Vehiculos", domain="[('id','not in',vehiculos_ocupados)]",track_visibility='onchange')
    empleados = fields.Many2many('upocargo.empleado', string="Empleados",domain="[('id','not in',empleados_ocupados)]",track_visibility='onchange')

    #Simulación de Campo One2one
    factura = fields.Many2one('upocargo.factura', string='Factura', ondelete='restrict')
    _sql_constraits = [
        ('unique_factura_mudanza', 'UNIQUE(id_factura)','¡Cada Mudanza solo puede tener una factura asociada!')
    ]
    # Campos auxilaries para domain dinamicos
    empleados_ocupados = fields.Many2many('upocargo.empleado', compute="_compute_ocupados", store=False)
    vehiculos_ocupados = fields.Many2many('upocargo.vehiculo', compute="_compute_ocupados", store=False)

    @api.model
    def create(self, vals):

        if not 'fecha' in vals:
            raise exceptions.ValidationError('Debe Seleccionar una fecha para la mudanza')
        fecha = vals['fecha']
        #vehiculos_id = vals.get('vehiculos',[(6,0,[])])[0][2] if vals.get('vehiculos') else []
        #empleados_id = vals.get('empleados',[(6,0,[])])[0][2] if vals.get('empleados') else []
        #if vals.get('vehiculos'):
        #    raise exceptions.ValidationError(f"Vehiculos:{vals.get('vehiculos')}")
        vehiculos = vals.get('vehiculos', [(6, 0, [])])  # Si no hay vehículos, se usará una lista vacía
        vehiculos_id = [vehiculo[1] for vehiculo in vehiculos if vehiculo[0] == 4]#vehiculos[0][2] if len(vehiculos) > 0 and len(vehiculos[0]) > 2 else []

        # Obtener los empleados seleccionados de manera segura
        empleados = vals.get('empleados', [(6, 0, [])])  # Si no hay empleados, se usará una lista vacía
        empleados_id = [empleado[1] for empleado in empleados if empleado[0] == 4]#empleados[0][2] if len(empleados) > 0 and len(empleados[0]) > 2 else []
        if not vehiculos_id or len(vehiculos_id)<1:
            raise exceptions.ValidationError('Debe seleccionar al menos un Vehiculo')
        if not empleados_id or len(empleados_id)<2:
            raise exceptions.ValidationError('Debe seleccionar al menos dos empleados')
        
        #revalidar conflictos vehiculos
        conflictos_vehiculos = self.env['upocargo.mudanza'].search([('fecha','=',fecha),('vehiculos','in',vehiculos_id)])
        if conflictos_vehiculos:
            raise exceptions.ValidationError('Uno o más vehiculos seleccionados ya estan asignados a una mudanza ese mismo dia')
        #revalidar conflictos empleados
        conflictos_empleados = self.env['upocargo.mudanza'].search([('fecha','=',fecha),('empleados','in',empleados_id)])
        if conflictos_empleados:
            raise exceptions.ValidationError('Uno o más empleados seleccionados ya estan asignados a una mudanza ese mismo dia')

        if 'id_factura' in vals:
            existing_mudanza = self.search([('id_factura', '=', vals['id_factura'])])
            if existing_mudanza:
                raise exceptions.ValidationError('Esta factura ya esta vinculada a otra mudanza.')
        mudanza = super(Mudanza, self).create(vals)

        coste = self._calcular_precio_promedio()
        coste_vehiculo_extra = 100
        coste_empleado_extra = 50
        vehiculos_extra = max(0, len(vehiculos_id)-1)
        empleados_extra = max(0, len(empleados_id)-2)
        coste = coste + (vehiculos_extra*coste_vehiculo_extra) + (empleados_extra*coste_empleado_extra)

        factura_vals = {
            'id_factura': self.env['upocargo.factura']._generate_id_factura(),
            'precio': coste,
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
    
    @staticmethod
    def _calcular_precio_promedio():
        costos_reales = [300,500, 700, 1000, 12000, 15000,1700]
        return random.choices(costos_reales,k=1) #sum(costos_reales) / len(costos_reales)
    
    @api.depends('fecha')
    def _compute_ocupados(self):
        for record in self:
            if not record.fecha:
                record.vehiculos_ocupados = [(6, 0, [])]
                record.empleados_ocupados = [(6, 0, [])]
                continue  # No hay nada que hacer más, se permite la selección
            #date_planned = datetime.strptime(record.fecha.isoformat(), "%Y-%m-%d")
            mudanzas_en_fecha = self.env['upocargo.mudanza'].search([('fecha','=',record.fecha)])
            #except Exception as e:
            #    raise exceptions.ValidationError(f"Error al buscar mudanzas para la fecha {fecha_comparable}: {str(e)}")
            if not mudanzas_en_fecha:
                record.vehiculos_ocupados = [(6, 0, [])]
                record.empleados_ocupados = [(6, 0, [])]
                continue  # No hay nada que hacer más, se permite la selección

            vehiculos_ocupados = mudanzas_en_fecha.mapped('vehiculos.id')
            empleados_ocupados = mudanzas_en_fecha.mapped('empleados.id')

            record.vehiculos_ocupados = [(6,0,vehiculos_ocupados)]
            record.empleados_ocupados = [(6,0,empleados_ocupados)]