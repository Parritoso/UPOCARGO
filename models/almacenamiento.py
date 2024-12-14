# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import random
import string
import logging
_logger = logging.getLogger(__name__)

class Almacenamiento(models.Model):
    _name = 'upocargo.almacenamiento'
    _description = 'Almacenamiento UPOCARGO'
    _mostrar_error = fields.Boolean(string="mostrar_error", store=False)
    _texto = fields.Text(string="error_msg", store=False)
    _rec_name = 'id_almacenamiento'

    #Campos Base
    id_almacenamiento = fields.Char(string="Id del Almacenamiento", required=True, help="Identificador del Almacenamiento", default=lambda self: self._generate_id_almacenamiento(), readonly=True)
    fecha_ingreso = fields.Date('Ingreso', required=True, autodate=True)
    fecha_salida = fields.Date('Salida', required=True, autodate=True)
    estado = fields.Selection([])

    #Campos relacionales
    bienes_almacenados = fields.One2many('upocargo.bienes_almacenados', 'almacenamiento', string="Bienes Almacenados")
    cliente = fields.Many2one('upocargo.cliente', string="Cliente")
    factura_id = fields.Many2one('upocargo.factura', string='Factura', ondelete='cascade')
    almacen = fields.Many2one('upocargo.almacen',string='Almacen', ondelete='restrict', required=True)
    mudanza_id = fields.Many2one('upocargo.mudanza', string="Mudanza", ondelete='cascade')
    servicios_adicionales = fields.Many2many('upocargo.servicios_adicionales', string="Servicios Adicionales", track_visibility='onchange')

    @api.model
    def create(self,vals):
        if vals.get('fecha_ingreso') >= vals.get('fecha_salida'):
            raise exceptions.ValidationError('La fecha de ingreso debe ser anterior a la fecha de salida.')
        
        bienes = vals.get('bienes_almacenados')
        almacen = vals.get('almacen')
        almacen = self.env['upocargo.almacen'].search([('id','=',vals.get('almacen'))])
        #if bienes:
        #    self._agregar_bienes_sin_duplicados(almacenamienrto, bienes)
        #else:
        #    raise exceptions.ValidationError('Debe incluir bienes en el almacenamiento')
        if not bienes:
            raise exceptions.ValidationError('Debe incluir bienes en el almacenamiento')
        # Validar tamaño total y condiciones de los sensores
        errores = []
        tamaño_total = 0
        bienes_por_crear = []  # Para guardar los bienes y sus cantidades
        bienes_no_validos = []  # Para los bienes que no cumplen con las condiciones
        _logger.info(f"Pasamos a comprobar bienes!\nBienes: {bienes}")
        for bien in bienes:#almacenamienrto.bienes_almacenados:
            bien = bien[2]
            _logger.info(f"comprobando: {bien}")
            tamaño_total += bien.get('tamanyo')

            # Verificar las condiciones de los sensores
            _logger.info(f"bien condicion_especial: {bien.get('condicion_especial')}")
            if bien.get('condicion_especial') == True:
                if bien.get('tipo_sensor') == 'temperatura':
                    if not (almacen.temp_min >= bien.get('valor_sensor_min') and almacen.temp_max <= bien.get('valor_sensor_max')):
                        bienes_no_validos.append(bien)
                elif bien.get('tipo_sensor') == 'humedad':
                    if not (almacen.humedad_min >= bien.get('valor_sensor_min') and almacen.humedad_max <= bien.get('valor_sensor_max')):
                        bienes_no_validos.append(bien)
        # Verificar si se excede el tamaño máximo del almacén
        if not self._tamaño_disponible(almacen, tamaño_total,self):
            errores.append(f"El tamaño total de los bienes excede el tamaño máximo del almacén. ({tamaño_total} > {almacen.tamaño_maximo})")

        if errores or bienes_no_validos:
            _logger.info("Hay errores! mostrando mensaje")
            # Si hay errores, mostrar mensaje con opciones para corregir automáticamente o manualmente
            error_msg = "\n".join(errores) if errores else ""
            if bienes_no_validos:
                error_msg += "\nLos siguientes bienes no cumplen con las condiciones del sensor: "
                for bien in bienes_no_validos:
                    _logger.info(f"bien: {bien}")
                    error_msg += ", ".join([bien.get('descripcion')])

            self._mostrar_error = True
            self._texto = error_msg
            #self.open_wizard()
            #raise exceptions.ValidationError(error_msg)
            # Mostrar un mensaje con opciones al usuario (p. ej., usar un modal o alguna ventana de acción)
            #return {
            #    'name': 'Error en la creación',
            #    'type': 'ir.actions.act_window',
            #    'res_model': 'upocargo.error.wizard',
            #    'view_mode': 'form',
            #    'view_type': 'form',
            #    'target': 'new',
            #    'context': {
            #        'default_error_msg': error_msg,
            #        'default_almacenamiento_id': almacenamienrto.id
            #    }
            #}

        
        tamaños_solucionado = []
        bienes_caben = []
        # Si el tamaño excede el límite, intentamos dividir los bienes en varios almacenamientos
        if tamaño_total > almacen.tamaño_maximo:
            _logger.info(f"Los bienes exceden el tamaño del almacen {tamaño_total}>{almacen.tamaño_maximo}")
            tamaños_solucionado = self._handle_size_exceeded(bienes,almacen)

        _logger.info(f"Tamaños solucionados: {tamaños_solucionado}")
        # Si las condiciones del sensor no se cumplen, buscar un nuevo almacenamiento que las cumpla
        if bienes_no_validos:
            _logger.info(f"Hay bienes no validos: {bienes_no_validos}")
            if tamaños_solucionado:
                self._handle_sensor_conditions(bienes_no_validos,tamaños_solucionado)
            else:
                self._handle_sensor_conditions(bienes_no_validos)

        #raise exceptions.ValidationError('Debug Error')
        if tamaños_solucionado:
            bienes = tamaños_solucionado[0]
            if tamaños_solucionado[1]:
                bienes_caben = tamaños_solucionado[1]
            vals['bienes_almacenados'] = bienes
        almacenamienrto = super(Almacenamiento, self).create(vals)

        if not vals.get('factura_id'):
            dias = (fields.Date.from_string(vals['fecha_salida']) - fields.Date.from_string(vals['fecha_ingreso'])).days
            precio_por_dia = 50
            coste_total = dias * precio_por_dia
            factura_vals = {
                'id_factura': self.env['upocargo.factura']._generate_id_factura(),
                'precio': coste_total,
                'currency_id': self.env.user.company_id.currency_id.id,
                'almacenamiento_id': almacenamienrto.id
            }
            factura = self.env['upocargo.factura'].create(factura_vals)

            almacenamienrto.factura_id = factura.id

            factura.agregar_gasto('Costo base',coste_total)

        if bienes_caben:
            for lista in bienes_caben:
                almacen_id = lista[0]
                bienes_almacenables =[]
                if lista[1:]:
                    for bien in lista[1:]:
                        bienes_almacenables.append(bien)
                    vals['id_almacenamiento'] = self._generate_id_almacenamiento()    
                    vals['bienes_almacenados'] = bienes_almacenables
                    vals['almacen'] = almacen_id
                    vals['factura_id'] = factura.id
                    nuevo_almacenamiento = self.env['upocargo.almacenamiento'].create(vals)

        return almacenamienrto
    
    def write(self,vals):
        if 'servicios_adicionales' in vals:
            servicios_adicionales = vals.get('servicios_adicionales', [(6, 0, [])])
            costo_servicios_adicionales = sum([self.env['upocargo.servicios_adicionales'].browse(servicio[1]).precio_final for servicio in servicios_adicionales])

            # Calcular el nuevo costo total
            coste = float(self.precio) + costo_servicios_adicionales

            # Actualizar la factura con el nuevo costo
            factura = self.factura
            if factura:
                factura.write({'precio': coste})

                # Agregar o actualizar los gastos de los servicios adicionales
                for servicio in servicios_adicionales:
                    servicio_obj = self.env['upocargo.servicios_adicionales'].browse(servicio[1])
                    factura.agregar_gasto(f"Servicio Adicional: {servicio_obj.tipo}", servicio_obj.precio_final)

    @staticmethod
    def _generate_id_almacenamiento():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    @api.constrains('fecha_ingreso','fecha_salida')
    def _check_fechas(self):
        for record in self:
            if record.fecha_ingreso > record.fecha_salida:
                raise exceptions.ValidationError("La fecha de ingreso no puede ser posterior a la fecha de salida.")
            
        

    def _tamaño_disponible(self, almacen, tamaño, almacenamiento):
        """
        Verifica si el tamaño del bien cabe en el almacén considerando
        la ocupación actual de bienes en el almacén durante las fechas del nuevo almacenamiento.
        """
        _logger.info(f"Parametros: almacen:{almacen}, tamaño:{tamaño}, almacenamiento:{almacenamiento}")
        # Obtener bienes almacenados que se superponen con las fechas de este nuevo almacenamiento
        bienes_ocupados = self.env['upocargo.bienes_almacenados'].search([
            ('almacenamiento.almacen', '=', almacen.id),
            ('almacenamiento.fecha_salida', '>=', almacenamiento.fecha_ingreso),
            ('almacenamiento.fecha_ingreso', '<=', almacenamiento.fecha_salida)
        ])

        #bienes_ocupados = bienes_ocupados.filtered(lambda b: b.id != bien.get('id'))
        _logger.info(f"Bienes ocupados: {bienes_ocupados.mapped('descripcion')}")

        tamaño_ocupado = sum(bien.tamanyo for bien in bienes_ocupados)

        _logger.info(f"Tamaño ocupado: {tamaño_ocupado}, Tamaño maximo del almacén: {almacen.tamaño_maximo}")

        tamaño_disponible = almacen.tamaño_maximo - tamaño_ocupado

        _logger.info(f"Tamaño disponible: {tamaño_disponible}")
        return tamaño_disponible >= tamaño#bien.get('tamanyo')


    def _handle_size_exceeded(self, bienes, almacen):
        _logger.info(f"\nParametros:\n-bienes: {bienes}\n-almacen: {almacen}")
        bienes_caben = []
        bienes_nuevo_almacen = []
        total = 0
        almacenamientos = self.env['upocargo.almacenamiento'].search([
            ('almacen', '=', almacen.id),
            ('fecha_salida', '>=', self.fecha_ingreso),
            ('fecha_ingreso', '<=', self.fecha_salida)
        ])
        _logger.info(f"ALmacenamientos primera vuelta: {almacenamientos}")
        for almacenamiento in almacenamientos:
            total += sum(bien.tamanyo for bien in almacenamiento.bienes_almacenados)
        _logger.info(f"Almacenamiento capacidad: {total}")
        for bien in bienes:
            _logger.info(f"Bien: {bien}")
            bien_nuevo = bien[2]
            _logger.info(f"Bien nuevo: {bien_nuevo}")
            tamaño = bien_nuevo.get('tamanyo')
            if not total+tamaño > almacen.tamaño_maximo:
                total += tamaño
                bienes_caben.append(bien)
                bienes.remove(bien)
        while(bienes):
                total=0
                almacen_2 = self.env['upocargo.almacen'].search([('id','!=',almacen.id)],limit=1)
                almacenamientos = self.env['upocargo.almacenamiento'].search([
                    ('almacen', '=', almacen_2.id),
                    ('fecha_salida', '>=', self.fecha_ingreso),
                    ('fecha_ingreso', '<=', self.fecha_salida)
                ])
                for almacenamiento in almacenamientos:
                    total += sum(bien.tamanyo for bien in almacenamiento.bienes_almacenados)
                lista_aux = []
                lista_aux.append(almacen_2.id)
                for bien in bienes:
                    _logger.info(f"Bien segunda vuelta: {bien}")
                    bien_nuevo = bien[2]
                    _logger.info(f"Bien nuevo segunda vuelta: {bien_nuevo}")
                    tamaño = bien_nuevo.get('tamanyo')
                    if not total+tamaño > almacen_2.tamaño_maximo:
                        total += tamaño
                        lista_aux.append(bien)
                        #bienes_nuevo_almacen.append(bien)
                        bienes.remove(bien)
                bienes_nuevo_almacen.append(lista_aux)
        _logger.info(f"Almacenes: {bienes_caben, bienes_nuevo_almacen}")
        return [bienes_caben, bienes_nuevo_almacen]


        

    def _handle_sensor_conditions(self, bienes_no_validos,tamaños_solucionado=None):
        # Lógica para mover bienes que no cumplen con las condiciones del sensor a un nuevo almacén

        _logger.info(f"\nPatametros:\n-bienes_no_validos: {bienes_no_validos}\n- tamaños_solucionado: {tamaños_solucionado}")
        bienes_no_validos_a_mover = []
        if tamaños_solucionado:
            bienes_caben, bienes_nuevo_almacen = tamaños_solucionado
            for bien in bienes_caben:
                for bien_no_valido in bienes_no_validos:
                    if bien.get('id') == bien_no_valido.id:
                        if bien.get('tipo_sensor') == 'temperatura':
                            almacenes_validos = self.env['upocargo.almacen'].search([
                                ('temp_min', '>=', bien.get('valor_sensor_min')),
                                ('temp_max', '<=', bien.get('valor_sensor_max')),
                            ])
                        else:
                            almacenes_validos = self.env['upocargo.almacen'].search([
                                ('humedad_min', '>=', bien.get('valor_sensor_min')),
                                ('humedad_max', '<=', bien.get('valor_sensor_max'))
                            ])
                        if not almacenes_validos:
                            # Si no existe almacén que cumpla con las condiciones, eliminamos el bien
                            bienes_caben.remove(bien)
                            raise exceptions.ValidationError(f"No se encontró un almacén que cumpla con las condiciones de sensor para el bien {bien.descripcion}. El bien ha sido eliminado.")
                        for almacen in almacenes_validos:
                            almacenamientos = self.env['upocargo.almacenamiento'].search([
                                ('almacen', '=', almacen.id),
                                ('fecha_salida', '>=', self.fecha_ingreso),
                                ('fecha_ingreso', '<=', self.fecha_salida)
                            ])
                            for almacenamiento in almacenamientos:
                                total += sum(bien.tamanyo for bien in almacenamiento.bienes_almacenados)
                            if not total + bien.get('tamanyo') > almacen.tamaño_maximo:
                                total += bien.get('tamanyo')
                                bien.remove(bien)
                                bienes_no_validos_a_mover.append({almacen.id,bien})
            for bien in bienes_nuevo_almacen:
                for bien_no_valido in bienes_no_validos:
                    if bien.get('id') == bien_no_valido.id:
                        if bien.get('tipo_sensor') == 'temperatura':
                            almacenes_validos = self.env['upocargo.almacen'].search([
                                ('temp_min', '>=', bien.get('valor_sensor_min')),
                                ('temp_max', '<=', bien.get('valor_sensor_max')),
                            ])
                        else:
                            almacenes_validos = self.env['upocargo.almacen'].search([
                                ('humedad_min', '>=', bien.get('valor_sensor_min')),
                                ('humedad_max', '<=', bien.get('valor_sensor_max'))
                            ])
                        if not almacenes_validos:
                            # Si no existe almacén que cumpla con las condiciones, eliminamos el bien
                            bienes_nuevo_almacen.remove(bien)
                            raise exceptions.ValidationError(f"No se encontró un almacén que cumpla con las condiciones de sensor para el bien {bien.get('descripcion')}. El bien ha sido eliminado.")
                        for almacen in almacenes_validos:
                            almacenamientos = self.env['upocargo.almacenamiento'].search([
                                ('almacen', '=', almacen.id),
                                ('fecha_salida', '>=', self.fecha_ingreso),
                                ('fecha_ingreso', '<=', self.fecha_salida)
                            ])
                            for almacenamiento in almacenamientos:
                                total += sum(bien.tamanyo for bien in almacenamiento.bienes_almacenados)
                            if not total + bien.get('tamanyo') > almacen.tamaño_maximo:
                                total += bien.get('tamanyo')
                                bien.remove(bien)
                                bienes_no_validos_a_mover.append({almacen.id,bien})
        else:
            for bien in bienes_no_validos:
                _logger.info(f"bien: {bien}")
                if bien.get('tipo_sensor') == 'temperatura':
                    almacenes_validos = self.env['upocargo.almacen'].search([
                                ('temp_min', '>=', bien.get('valor_sensor_min')),
                                ('temp_max', '<=', bien.get('valor_sensor_max')),
                            ])
                else:
                    almacenes_validos = self.env['upocargo.almacen'].search([
                                ('humedad_min', '>=', bien.get('valor_sensor_min')),
                                ('humedad_max', '<=', bien.get('valor_sensor_max'))
                            ])
                _logger.info(f"Almacenes: {almacenes_validos}")
                if not almacenes_validos:
                    # Si no existe almacén que cumpla con las condiciones, eliminamos el bien
                    bienes_no_validos.remove(bien)
                    raise exceptions.ValidationError(f"No se encontró un almacén que cumpla con las condiciones de sensor para el bien {bien.descripcion}. El bien ha sido eliminado.")
                list = []
                for almacen in almacenes_validos:
                    almacenamientos = self.env['upocargo.almacenamiento'].search([
                                ('almacen', '=', almacen.id),
                                ('fecha_salida', '>=', self.fecha_ingreso),
                                ('fecha_ingreso', '<=', self.fecha_salida)
                            ])
                    for almacenamiento in almacenamientos:
                        total += sum(bien.tamanyo for bien in almacenamiento.bienes_almacenados)
                    if not total + bien.get('tamanyo') > almacen.tamaño_maximo:
                        total += bien.get('tamanyo')
                        bien.remove(bien)
                        list.append(almacen.id)
                        list.append(bien)
                bienes_no_validos_a_mover.append(list)
        _logger.info(f"bienes_no_validos_a_mover: {bienes_no_validos_a_mover}")
        return {bienes_caben,bienes_nuevo_almacen,bienes_no_validos_a_mover}