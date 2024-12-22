from odoo import models, fields, api
import json, logging
_logger = logging.getLogger(__name__)

#class UpocargoConfiguracion(models.TransientModel):
#    _name = 'upocargo.configuracion'
#    _inherit = 'ir.config_parameter'
#
#    coste_vehiculo_extra = fields.Float(string="Coste Vehículo Extra", default=100.0)
#    coste_empleado_extra = fields.Float(string="Coste Empleado Extra", default=50.0)
#    costos_reales = fields.Char(string="Costos Reales", default="300,500,700,1000,12000,15000,1700")
#    precio_por_dia_almacenamiento = fields.Float(string="Precio por Día de Almacenamiento", default=50.0)

#    def set_values(self):
#        super(UpocargoConfiguracion, self).set_values()
#        # Guardamos los valores en los parámetros del sistema
#        self.env['ir.config_parameter'].set_param('value', self.coste_vehiculo_extra)
#        self.env['ir.config_parameter'].set_param('value', self.coste_empleado_extra)
#        self.env['ir.config_parameter'].set_param('value', self.costos_reales)
#        self.env['ir.config_parameter'].set_param('value', self.precio_por_dia_almacenamiento)

#    def get_values(self):
#        res = super(UpocargoConfiguracion, self).get_values()
#        # Recuperamos los valores de los parámetros del sistema
#        res.update(
#            coste_vehiculo_extra=float(self.env['ir.config_parameter'].get_param('upocargo.coste_vehiculo_extra', default=100.0)),
#            coste_empleado_extra=float(self.env['ir.config_parameter'].get_param('upocargo.coste_empleado_extra', default=50.0)),
#            costos_reales=self.env['ir.config_parameter'].get_param('upocargo.costos_reales', default="300,500,700,1000,12000,15000,1700"),
#            precio_por_dia_almacenamiento=float(self.env['ir.config_parameter'].get_param('upocargo.precio_por_dia_almacenamiento', default=50.0)),
#        )
#        return res

class UpocargoConfiguracion(models.Model):
    _name = 'upocargo.configuracion'
    _description = 'Configuración del módulo'

    coste_vehiculo_extra = fields.Float(string="Coste Vehículo Extra", default=100.0)
    coste_empleado_extra = fields.Float(string="Coste Empleado Extra", default=50.0)
    costos_reales = fields.Char(string="Costos Reales", default="300,500,700,1000,12000,15000,1700")
    precio_por_dia_almacenamiento = fields.Float(string="Precio por Día de Almacenamiento", default=50.0)

    @api.model
    def default_get(self, fields_list):
        res = super(UpocargoConfiguracion, self).default_get(fields_list)

        # Recuperar parámetros de configuración si están disponibles
        config_obj = self.env['ir.config_parameter']
        res['coste_vehiculo_extra'] = float(config_obj.get_param('upocargo.coste_vehiculo_extra', default='100.0'))
        res['coste_empleado_extra'] = float(config_obj.get_param('upocargo.coste_empleado_extra', default='50.0'))
        res['costos_reales'] = config_obj.get_param('upocargo.costos_reales', default='300,500,700,1000,12000,15000,1700')
        res['precio_por_dia_almacenamiento'] = float(config_obj.get_param('upocargo.precio_por_dia_almacenamiento', default='50.0'))

        _logger.info(f"res: {res}")
        return res

    @api.model
    def set_default_parameters(self,id):
        # Establecer parámetros por defecto si no están definidos
        config_obj = self.env['ir.config_parameter']
        config = self.env['upocargo.configuracion'].sudo().search([('id','in',id)],limit=1)

        _logger.info(f"self.coste_vehiculo_extra: {config.coste_vehiculo_extra}")
        _logger.info(f"self.coste_empleado_extra: {config.coste_empleado_extra}")
        _logger.info(f"self.precio_por_dia_almacenamiento: {config.precio_por_dia_almacenamiento}")
        _logger.info(f"self.costos_reales: {config.costos_reales}")
        

        # Parámetros simples
        config_obj.set_param('upocargo.coste_vehiculo_extra', str(config.coste_vehiculo_extra))
        config_obj.set_param('upocargo.coste_empleado_extra', str(config.coste_empleado_extra))
        config_obj.set_param('upocargo.precio_por_dia_almacenamiento', str(config.precio_por_dia_almacenamiento))

        # Parámetro tipo array (usando JSON)
        if isinstance(config.costos_reales, str):
            costos_reales = [int(x) for x in config.costos_reales.split(',')]
            config_obj.set_param('upocargo.costos_reales', json.dumps(costos_reales))
        else:
            # Si no es una cadena, se establece un valor por defecto
            config_obj.set_param('upocargo.costos_reales', json.dumps(300, 500, 700,1000,12000,15000,1700))
        return True
    @api.model
    def get_param(self, key, default=None):
        config_obj = self.env['ir.config_parameter']
        value = config_obj.get_param(key, default=default)
        if key == 'upocargo.costos_reales':
            # Si el parámetro es un array (JSON), lo decodificamos
            return json.loads(value) if value else []
        return value
