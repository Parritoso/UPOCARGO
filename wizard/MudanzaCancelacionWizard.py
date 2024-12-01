from odoo import models, fields, api, exceptions

class MudanzaCancelacionWizard(models.TransientModel):
    _name = 'upocargo.mudanza.cancelacion.wizard'

    confirmar_cancelacion = fields.Boolean("¿Está seguro de que desea cancelar esta mudanza?", default=False)
    mudanza_id = fields.Many2one('upocargo.mudanza', string="Mudanza", required=True)

    def confirmar_cancelacion_action(self):
        if not self.confirmar_cancelacion:
            raise exceptions.UserError("La cancelación no fue confirmada.")
        
        # Cambiar el estado de la mudanza a 'cancelado'
        self.mudanza_id.write({'estado': 'cancelado'})
        return {'type': 'ir.actions.act_window_close'}