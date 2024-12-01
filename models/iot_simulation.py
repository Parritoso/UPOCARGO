from odoo import api, SUPERUSER_ID
import threading

def _start_iot_simulation(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    almacenes = env['upocargo.almacen'].search([])
    #if almacenes:
        # Para cada almacén, creamos un hilo que ejecute la simulación
        #for almacen in almacenes:
            #threading.Thread(target=almacen._simular_sensores, daemon=True).start()