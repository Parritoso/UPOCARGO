# -*- coding: utf-8 -*-
'''
from odoo import models, fields, api


class Classes(models.Model):
     _name = 'gym.classes'
     _description = 'Gym Classes'

     name = fields.Char(string="Title", required=True, help="name of the gym")
     description = fields.Text()
     start = fields.Datetime('Starts',required=True, autodate = True)
     end = fields.Datetime('Ends',required=True, autodate = True)
     capacity = fields.Integer("Capacity") 
     activityType = fields.Selection([('dance','Dance'),
                                     ('aerobic','Aerobic'),
                                     ('anaerobic','Anaerobic'),
                                     ('relax','Relax'),],
                                     'Type of activity')
     users_ids = fields.Many2many("gym.users",string="Confirmed users")
     instructores_id=fields.Many2one('gym.instructores',string="Instructor")
     ocupacion = fields.Integer(compute='_ocupacionTotal',string='Ocupacion total',store=True)

     def btn_desapuntar_socios(self):
          self.write({'users_ids':[(5,)]})
     
     @api.depends('users_ids')
     def _ocupacionTotal(self): 
          for record in self:
               record.ocupacion = len(record.users_ids)
     
     @api.constrains('capacity')
     def _check_capacity(self):
          if self.capacity >= 50:
               raise models.ValidationError('La capacidad de la clase debe ser inferior a 50.')
     
     @api.onchange('capacity','activityType')
     def onchange_classes(self):
          resultado = {}
          if self.capacity >= 30 and self.activityType == 'dance':
               resultado = {
                    'value': {'capacity':30},
                    'warning': {
                         'title':'Valores incorrectos',
                         'message':'Las clases de baile son para maximos 30 personas'
                    }
               }
               return resultado
'''