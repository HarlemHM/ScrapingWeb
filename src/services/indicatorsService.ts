/**
 * Servicio de Indicadores
 * Endpoints del backend declarados pero no utilizados aún
 */

// ==================================================
// ENDPOINTS DEL BACKEND (DECLARADOS - NO UTILIZADOS)
// ==================================================
export const indicatorsEndpoints = {
    // 9.3 Indicadores
    summary: {
        method: 'GET',
        url: '/api/v1/indicadores/resumen',
        description: 'Cards globales con resumen de indicadores'
    },
    tableHotels: {
        method: 'GET',
        url: '/api/v1/indicadores/tabla-hoteles',
        description: 'Tabla comparativa de hoteles'
    },
    platformDistribution: {
        method: 'GET',
        url: '/api/v1/indicadores/distribucion-plataformas',
        description: 'Gráfico de distribución por plataforma'
    },
    hotelComparison: {
        method: 'GET',
        url: '/api/v1/indicadores/comparacion-hoteles',
        description: 'Comparación general entre hoteles'
    }
};

// Cuando se conecte al backend, descomentar y usar:
// export const fetchIndicatorsSummary = async () => {
//   const response = await fetch(indicatorsEndpoints.summary.url);
//   return response.json();
// };
