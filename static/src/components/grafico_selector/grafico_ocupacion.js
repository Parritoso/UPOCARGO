/** @odoo-module **/

import { Component, useState, useEffect } from "@odoo/owl";
import { useService } from '@web/core/utils/hooks';
import { registry } from '@web/core/registry';

export class GraficoOcupacion extends Component {

  setup() {
    this.state = useState({
      fecha: null,  // Fecha seleccionada para los datos del gráfico
      datosGrafico: [],
      datosRaw: [],
    });

    // Servicio ORM para realizar consultas
    this.orm = useService("orm");

    // Escuchar el evento de cambio de fecha
    this.onFechaChange = this.onFechaChange.bind(this);

    // Usamos un useEffect para manejar la lógica de actualización de gráficos
    useEffect(() => {
      if (this.state.fecha) {
        this.obtenerDatosGrafico(this.state.fecha);
      }
    }, ()=>{return[this.state.fecha]});  // Solo se ejecutará cuando la fecha cambie
  }

  async onFechaChange(event) {
    const nuevaFecha = event.target.value;
    this.state.fecha = nuevaFecha;

    // Llamar a un método para actualizar el gráfico cuando la fecha cambie
    await this.obtenerDatosGrafico(nuevaFecha);
  }

  // Método para obtener los datos del gráfico según la fecha
  async obtenerDatosGrafico(fecha) {
    if (!fecha) return;

    try {
      // Suponiendo que el modelo 'upocargo.almacen' tiene un método que devuelva datos por fecha
      const ocupacionData = await this.orm.call('upocargo.almacen', 'get_ocupacion_by_fecha', [fecha]);
      console.log('Datos de ocupacion: ',ocupacionData);
      //this.state.datosGrafico = ocupacionData;  // Asignamos los datos al estado
      if(ocupacionData){
        this.state.datosGrafico = {
          etiquetas: ocupacionData.map(item => item.nombre_almacen),
          ocupacion: ocupacionData.map(item => item.porcentaje_ocupacion),
        };
        this.state.datosRaw = ocupacionData;
        this.renderGrafico();
      }
    } catch (error) {
      console.error("Error obteniendo datos del gráfico:", error);
    }
  }

  renderGrafico() {
    const canvas = document.getElementById('grafico-ocupacion');
    if (!canvas) {
      console.error("No se encuentra el canvas con id 'grafico-ocupacion'");
      return;  // Salir si el canvas no existe
    }
    const ctx = canvas.getContext('2d');
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
      type: 'bar',  // Tipo de gráfico (línea en este caso)
      data: datos,
      options: {
        responsive: true,
        scales: {
          x: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Almacenes',
            }
          },
          y: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: 'Ocupación (%)',
            },
            ticks: {
              callback: function(value){
                return value+'%';
              }
            }
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
          tooltip: {
            enable: true,
            callback: {
              label: function(tooltip){
                return tooltip.raw.toFixed(2) + '%';
              }
            }
          }
        }
      }
    });
  }

  static template = 'GraficoOcupacionTemplate';

}

/*
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
    `;
}*/

registry.category('actions').add('GraficoOcupacionTemplate', GraficoOcupacion);