import { registry } from '@web/core/registry';
import { Component } from 'owl';
import SelectorFecha from './selector_fecha.js'; // Importamos el componente
import GraficoOcupacion from './grafico_ocupacion.js'; // Otro componente de ejemplo

// Registrar el componente en el sistema de OWL de Odoo
registry.category("views").add("upocargo.almacen.grafico_selector", SelectorFecha);
registry.category("views").add("upocargo.almacen.grafico_ocupacion", GraficoOcupacion);

document.addEventListener("DOMContentLoaded", () => {
    const selectorFechaContainer = document.querySelector("#selector-fecha");
    const graficoOcupacionContainer = document.querySelector("#grafico-ocupacion");
    
    if (selectorFechaContainer) {
        new SelectorFecha().mount(selectorFechaContainer);
    }

    if (graficoOcupacionContainer) {
        new GraficoOcupacion().mount(graficoOcupacionContainer);
    }
});