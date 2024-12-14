from odoo import models, fields

class UpocargoConfiguracion(models.TransientModel):
    _name = 'upocargo.configuracion'
    _inherit = 'res.config.settings'

    coste_vehiculo_extra = fields.Float(string="Coste Vehículo Extra", default=100.0)
    coste_empleado_extra = fields.Float(string="Coste Empleado Extra", default=50.0)
    costos_reales = fields.Char(string="Costos Reales", default="300,500,700,1000,12000,15000,1700")
    precio_por_dia_almacenamiento = fields.Float(string="Precio por Día de Almacenamiento", default=50.0)

    def set_values(self):
        super(UpocargoConfiguracion, self).set_values()
        # Guardamos los valores en los parámetros del sistema
        self.env['ir.config_parameter'].set_param('upocargo.coste_vehiculo_extra', self.coste_vehiculo_extra)
        self.env['ir.config_parameter'].set_param('upocargo.coste_empleado_extra', self.coste_empleado_extra)
        self.env['ir.config_parameter'].set_param('upocargo.costos_reales', self.costos_reales)
        self.env['ir.config_parameter'].set_param('upocargo.precio_por_dia_almacenamiento', self.precio_por_dia_almacenamiento)

    def get_values(self):
        res = super(UpocargoConfiguracion, self).get_values()
        # Recuperamos los valores de los parámetros del sistema
        res.update(
            coste_vehiculo_extra=float(self.env['ir.config_parameter'].get_param('upocargo.coste_vehiculo_extra', default=100.0)),
            coste_empleado_extra=float(self.env['ir.config_parameter'].get_param('upocargo.coste_empleado_extra', default=50.0)),
            costos_reales=self.env['ir.config_parameter'].get_param('upocargo.costos_reales', default="300,500,700,1000,12000,15000,1700"),
            precio_por_dia_almacenamiento=float(self.env['ir.config_parameter'].get_param('upocargo.precio_por_dia_almacenamiento', default=50.0)),
        )
        return res