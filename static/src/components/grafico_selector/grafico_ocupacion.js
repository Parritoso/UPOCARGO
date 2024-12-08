/** @odoo-module **/

import { Component, useState, useEffect } from "@odoo/owl";
import { xml } from "@odoo/owl";
import { useService } from "@odoo/owl";

export class GraficoOcupacion extends Component {
  static template = 'OWLGraficoOcupacion';
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

  render() {
    return xml`
      <div>
        <h3>Gráfico de Ocupación para la Fecha ${this.state.fecha || 'Seleccionada'}</h3>
        <div id="grafico-ocupacion" style="height: 400px; width: 100%;"></div>
      </div>
    `;
  }
}