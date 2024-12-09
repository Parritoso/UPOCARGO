/** @odoo-module **/

/*import { Component, useState, useEffect } from "@odoo/owl";
import { useService } from "@odoo/owl";
import { registry } from '@web/core/registry';

export class GraficoOcupacion extends Component {
  constructor() {
    super(...arguments);
    this.state = useState({
        fecha: null,
        datosGrafico: []
    });
    this.orm = useService("orm");
    this.on('fecha_cambiada', async (nuevaFecha) => {
      this.state.fecha = nuevaFecha;
      await this.obtenerDatosGrafico(nuevaFecha);
    });
  }
  setup() {
    this.state = useState({
      fecha: null,  // Fecha seleccionada para los datos del gráfico
      datosGrafico: [],
    });

    // Servicio ORM para realizar consultas
    this.orm = useService("orm");

    // Escuchar el evento de cambio de fecha
    this.on('fecha_cambiada', async (nuevaFecha) => {
      this.state.fecha = nuevaFecha;
      await this.obtenerDatosGrafico(nuevaFecha);
    });
  }

  onFechaChange(event) {
    const nuevaFecha = event.target.value;
    this.state.fecha = nuevaFecha;

    // Llamar a un método para actualizar el gráfico cuando la fecha cambie
    this.trigger('fecha_cambiada', nuevaFecha);  // Emitimos el evento
  }

  // Método para obtener los datos del gráfico según la fecha
  async obtenerDatosGrafico(fecha) {
    if (!fecha) return;

    // Suponiendo que el modelo 'upocargo.almacen' tiene un método que devuelva datos por fecha
    const ocupacionData = await this.orm.call('upocargo.almacen', 'get_ocupacion_by_fecha', [fecha]);
    this.state.datosGrafico = ocupacionData;  // Asignamos los datos al estado
    this.renderGrafico();
  }

  renderGrafico() {
    const ctx = document.getElementById('grafico-ocupacion').getContext('2d');
    if (this.chart) {
      this.chart.destroy(); // Si ya existe un gráfico, lo destruimos antes de crear uno nuevo
    }

    // Suponemos que `datosGrafico` tiene una estructura como { etiquetas: ['fecha1', 'fecha2', ...], ocupacion: [25, 40, ...] }
    const datos = {
      labels: this.state.datosGrafico.etiquetas || [],
      datasets: [{
        label: 'Ocupación',
        data: this.state.datosGrafico.ocupacion || [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.1
      }]
    };

    // Crear el gráfico usando Chart.js
    this.chart = new Chart(ctx, {
      type: 'line',  // Tipo de gráfico (línea en este caso)
      data: datos,
      options: {
        responsive: true,
        scales: {
          x: {
            beginAtZero: true
          },
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }

  static template = 'upocargo.GraficoOcupacionTemplate';

  /*render() {
    return 'upocargo.GraficoOcupacionTemplate'/*xml`
      <div>
        <h3>Gráfico de Ocupación para la Fecha ${this.state.fecha || 'Seleccionada'}</h3>
        <div id="grafico-ocupacion" style="height: 400px; width: 100%;"></div>
      </div>
    `;
  }
}*/

import { Component, useState } from "@odoo/owl";
import { xml } from "@odoo/owl"; // Importación de OWL para definir la plantilla
import { registry } from '@web/core/registry';

export class MiComponenteOWL extends Component {
    constructor() {
        super(...arguments);
        this.state = useState({
            fecha: null,
            datosGrafico: []
        });
    }

    onFechaChange(event) {
        this.state.fecha = event.target.value;
        this.actualizarGrafico(event.target.value); // Actualiza el gráfico al cambiar la fecha
    }

    actualizarGrafico(fecha) {
        if (fecha) {
            // Lógica para obtener los datos del gráfico
            const datos = this.generarDatosGrafico(fecha);
            this.state.datosGrafico = datos;
        }
    }

    generarDatosGrafico(fecha) {
        const valor = Math.random() * 100;  // Simulación de datos
        return [{ name: "Valor Calculado", values: [[fecha, valor]] }];
    }

    static template = 'upocargo.GraficoOcupacionTemplate'/*xml`
        <div>
            <div>
                <label for="fecha">Seleccionar Fecha:</label>
                <input type="date" id="fecha" t-on-change="onFechaChange"/>
            </div>
            <div>
                <t t-if="state.datosGrafico.length > 0">
                    <graph string="Gráfico de Valor Calculado" t-att-data="state.datosGrafico"/>
                </t>
                <t t-else="">
                    <p>No hay datos disponibles para el gráfico.</p>
                </t>
            </div>
        </div>
    `*/;
}

registry.category('actions').add('upocargo.GraficoOcupacionTemplate', MiComponenteOWL);