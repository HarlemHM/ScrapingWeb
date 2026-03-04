/**
 * Índice de Servicios
 * Exporta todos los endpoints del backend
 */

import { hotelsEndpoints } from './hotelsService';
import { reviewsEndpoints } from './reviewsService';
import { indicatorsEndpoints } from './indicatorsService';
import { scrapingEndpoints } from './scrapingService';
import { exportEndpoints } from './exportService';

// Exportar individualmente
export { hotelsEndpoints } from './hotelsService';
export { reviewsEndpoints } from './reviewsService';
export { indicatorsEndpoints } from './indicatorsService';
export { scrapingEndpoints } from './scrapingService';
export { exportEndpoints } from './exportService';

// Exportación centralizada de todos los endpoints
export const backendEndpoints = {
    hotels: hotelsEndpoints,
    reviews: reviewsEndpoints,
    indicators: indicatorsEndpoints,
    scraping: scrapingEndpoints,
    export: exportEndpoints
};
