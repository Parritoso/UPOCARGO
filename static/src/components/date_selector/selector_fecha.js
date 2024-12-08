/** @odoo-module **/

import { Component, useState, onWillStart , onWillUpdateProps} from "@odoo/owl";
import { useService } from "@odoo/owl";
import { xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { onEvent } from "@odoo/owl";

export class SelectorFecha extends Component {
  static template = 'OWLSelectorFecha';
  setup() {
    // Estado local para la fecha seleccionada
    this.state = useState({
      fecha: null,  // Fecha seleccionada por el usuario
    });

    // Servicio ORM de Odoo
    this.orm = useService("orm");
  }

  // Este método será llamado cuando el usuario cambie la fecha
  onFechaChange(event) {
    const nuevaFecha = event.target.value;
    this.state.fecha = nuevaFecha;

    // Llamar a un método para actualizar el gráfico cuando la fecha cambie
    this.trigger('fecha_cambiada', nuevaFecha);  // Emitimos el evento
  }

  render() {
    return xml`
      <div>
        <label for="fecha" string="Seleccionar Fecha" />
        <input type="date" id="fecha" value="${this.state.fecha}" on-input="onFechaChange" />
      </div>
    `;
  }
}