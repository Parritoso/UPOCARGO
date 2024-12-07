# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import random
import string
from datetime import datetime, date
import json
import logging
_logger = logging.getLogger(__name__)

class Mudanza(models.Model):
    _name = 'upocargo.mudanza'
    _description = 'Mudanzas UPOCARGO'

    #Campos Base
    id_mudanza = fields.Char(string="Id de la mudanza", required=True, help="Identificador de la mudanza", default=lambda self: self._generate_id_mudanza(), readonly=True)
    fecha = fields.Date('Inicio', required=True, autodate=True)
    fecha_final_mudanza = fields.Date('Fecha Final Mudanza', autodate=True)
    dirOrigen = fields.Char(string="Direccion Origen", required=True, help="Direccion del Cliente")
    dirDestino = fields.Char(string="Direccion Destino", required=True, help="Direccion del Cliente")
    estado = fields.Selection([('planificado','Planificado'),('iniciado','Iniciado'),('proceso','En proceso'),('almacenado','Bienes Almacenados'),('transportando','Transportando'),('finalizado','Finalizado'),('cancelado','Cancelado')],string='Estado', default='planificado')

    #Campos relacionales
    cliente = fields.Many2one('upocargo.cliente', string="Cliente")
    vehiculos = fields.Many2many('upocargo.vehiculo', string="Vehiculos", domain="[('id','not in',vehiculos_ocupados)]",track_visibility='onchange')
    empleados = fields.Many2many('upocargo.empleado', string="Empleados",domain="[('id','not in',empleados_ocupados)]",track_visibility='onchange')
    almacenamientos = fields.One2many('upocargo.almacenamiento', 'mudanza_id', string='Almacenamientos')
    servicios_adicionales = fields.Many2many('upocargo.servicios_adicionales', string="Servicios Adicionales", track_visibility='onchange')

    #Simulación de Campo One2one
    factura = fields.Many2one('upocargo.factura', string='Factura', ondelete='restrict')
    _sql_constraits = [
        ('unique_factura_mudanza', 'UNIQUE(id_factura)','¡Cada Mudanza solo puede tener una factura asociada!')
    ]
    # Campos auxilaries para domain dinamicos
    empleados_ocupados = fields.Many2many('upocargo.empleado', compute="_compute_ocupados", store=False)
    vehiculos_ocupados = fields.Many2many('upocargo.vehiculo', compute="_compute_ocupados", store=False)

    def action_cancelar_mudanza(self):
        # Verificamos si la mudanza ya está cancelada
        if self.estado == 'cancelado':
            raise exceptions.UserError("Esta mudanza ya está cancelada.")
        
        # Lanzamos un pop-up de confirmación
        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirmar Cancelación',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'upocargo.mudanza.cancelacion.wizard',
            'target': 'new',
            'context': {
                'default_mudanza_id': self.id
            }
        }

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
        vehiculos_id = [vehiculo[1] for vehiculo in vehiculos if vehiculo[0] == 4]#vehiculos[0][2] if len(vehiculos) > 0 and len(vehiculos[0]) > 2 else [

        if 'almacenamientos' not in vals or not vals['almacenamientos']:
            vals['fecha_final_mudanza'] = fecha

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

        servicios_adicionales = vals.get('servicios_adicionales', [(6, 0, [])])
        costo_servicios_adicionales = sum([self.env['upocargo.servicios_adicionales'].browse(servicio[1]).precio_final for servicio in servicios_adicionales])

        if 'id_factura' in vals:
            existing_mudanza = self.search([('id_factura', '=', vals['id_factura'])])
            if existing_mudanza:
                raise exceptions.ValidationError('Esta factura ya esta vinculada a otra mudanza.')
        mudanza = super(Mudanza, self).create(vals)

        almacenamiento = None
        factura_almacenamiento = None
        if 'almacenamientos' in vals:
            almacenamientos_vals = vals['almacenamientos']
            for almacen in almacenamientos_vals:
                almacenamiento_vals = {
                    'fecha_ingreso': fecha,
                    'fecha_salida': mudanza.fecha_final_mudanza,  # Usamos la fecha final de la mudanza
                    'cliente': mudanza.cliente.id,
                    'almacen': almacen['almacen'],  # Suponiendo que cada almacenamiento tiene un almacén asociado
                    'mudanza_id': mudanza.id,  # Asociamos este almacenamiento a la mudanza
                }
                almacenamiento = self.env['upocargo.almacenamiento'].create(almacenamiento_vals)

        coste = self._calcular_precio_promedio()
        coste_vehiculo_extra = 100
        coste_empleado_extra = 50
        vehiculos_extra = max(0, len(vehiculos_id)-1)
        empleados_extra = max(0, len(empleados_id)-2)
        coste = float(coste) + float(vehiculos_extra*coste_vehiculo_extra) + float(empleados_extra*coste_empleado_extra)
        if 'almacenamientos'and almacenamiento:
            factura_almacenamiento = self.env['upocargo.factura'].search([('id','=',almacenamiento.factura_id)])
            coste += float(factura.precio)

        factura_vals = {
            'id_factura': self.env['upocargo.factura']._generate_id_factura(),
            'precio': coste,
            'currency_id': self.env.user.company_id.currency_id.id,
            'mudanza_id': mudanza.id,
        }
        factura = self.env['upocargo.factura'].create(factura_vals)
        factura.agregar_gasto('Costo base',coste)
        if not vehiculos_extra == 0:
            factura.agregar_gasto('Vehiculos extra',vehiculos_extra*coste_vehiculo_extra)
        if not empleados_extra == 0:
            factura.agregar_gasto('Vehiculos extra',empleados_extra*coste_empleado_extra)
        if almacenamiento and factura_almacenamiento:
            desglose = json.loads(factura_almacenamiento.desglose_gastos or "[]")
            for item in desglose:
                if item['concepto'] == 'Costo base':
                    factura.agregar_gasto('Coste almacenamiento',item['valor'])
                else:
                    factura.agregar_gasto(item['concepto'],item['valor'])
        for servicio in servicios_adicionales:
            servicio_obj = self.env['upocargo.servicios_adicionales'].browse(servicio[1])
            factura.agregar_gasto(f"Servicio Adicional: {servicio_obj.tipo}", servicio_obj.precio_final)
        if not factura or isinstance(factura, bool):
            raise exceptions.ValidationError('No se puedo crear la factura asociada')
        mudanza.factura = factura.id
        return mudanza
    
    def write(self,vals):
        if 'servicios_adicionales' in vals:
            servicios_adicionales = vals.get('servicios_adicionales', [(6, 0, [])])
            costo_servicios_adicionales = sum([self.env['upocargo.servicios_adicionales'].browse(servicio[1]).precio_final for servicio in servicios_adicionales])

            # Calcular el nuevo costo total
            coste = self._calcular_precio_promedio()
            coste_vehiculo_extra = 100
            coste_empleado_extra = 50
            _logger.info("self.vehiculos: %s",[vehiculo.id for vehiculo in self.vehiculos])
            vehiculos_extra = max(0, len(self.vehiculos)-1)
            _logger.info("self.empleados: %s",[empleado.id for empleado in self.empleados])
            empleados_extra = max(0, len(self.empleados)-2)
            coste = float(coste) + float(vehiculos_extra * coste_vehiculo_extra) + float(empleados_extra * coste_empleado_extra) + costo_servicios_adicionales

            # Actualizar la factura con el nuevo costo
            factura = self.factura
            if factura:
                factura.write({'precio': coste})

                # Agregar o actualizar los gastos de los servicios adicionales
                for servicio in servicios_adicionales:
                    servicio_obj = self.env['upocargo.servicios_adicionales'].browse(servicio[1])
                    factura.agregar_gasto(f"Servicio Adicional: {servicio_obj.tipo}", servicio_obj.precio_final)
        #if 'id_factura' in vals:
        #    existing_mudanza = self.search([('id_factura', '=', vals['id_factura'])])
        #    if existing_mudanza:
        #        raise exceptions.ValidationError('Esta factura ya esta vinculada a otra mudanza.')
        return super(Mudanza, self).write(vals)
    
    @staticmethod
    def _generate_id_mudanza():
        creation_date = datetime.now().strftime('%d-%m-%Y')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{creation_date}-{random_suffix}"
    
    @staticmethod
    def _calcular_precio_promedio():
        costos_reales = [300,500, 700, 1000, 12000, 15000,1700]
        return random.choice(costos_reales) #sum(costos_reales) / len(costos_reales)
    
    @api.depends('fecha', 'fecha_final_mudanza')
    def _compute_ocupados(self):
        for record in self:
            if not record.fecha:
                record.vehiculos_ocupados = [(6, 0, [])]
                record.empleados_ocupados = [(6, 0, [])]
                continue  # No hay nada que hacer más, se permite la selección
            #date_planned = datetime.strptime(record.fecha.isoformat(), "%Y-%m-%d")
            mudanzas_en_fecha = self.env['upocargo.mudanza'].search([
                '&',  # AND
                '|',  # OR
                ('fecha', '=', record.fecha),  # fecha == record.fecha
                ('fecha', '=', record.fecha_final_mudanza),  # fecha == record.fecha_final_mudanza
                '|',  # OR
                ('fecha_final_mudanza', '=', record.fecha),  # fecha_final_mudanza == record.fecha
                ('fecha_final_mudanza', '=', record.fecha_final_mudanza),  # fecha_final_mudanza == record.fecha_final_mudanza
                ('estado', '!=', 'cancelado')  # estado != 'cancelado'
            ])
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