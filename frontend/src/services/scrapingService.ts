/**
 * Servicio de Scraping
 * Endpoints del backend declarados pero no utilizados aún
 */

// ==================================================
// ENDPOINTS DEL BACKEND (DECLARADOS - NO UTILIZADOS)
// ==================================================
export const scrapingEndpoints = {
    // 9.4 Scraping
    executeSimulation: {
        method: 'POST',
        url: '/api/v1/scraping/ejecutar',
        description: 'Simulación de scraping para frontend'
    },
    executeReal: {
        method: 'POST',
        url: '/api/v1/scraping/ejecutar-ahora',
        description: 'Scraping real'
    }
};

// Cuando se conecte al backend, descomentar y usar:
// export const executeScraping = async (platforms: string[]) => {
//   const response = await fetch(scrapingEndpoints.executeSimulation.url, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ platforms })
//   });
//   return response.json();
// };
