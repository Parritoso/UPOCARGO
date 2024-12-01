# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import wizard

def post_init_hook(cr, registry):
    try:
        from .models.almacen import _start_iot_simulation_for_all
        _start_iot_simulation_for_all()
    except ImportError as e:
        print("Error al importar la función de simulación IoT:", e)