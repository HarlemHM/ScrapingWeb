/**
 * Configuración de la API
 * Define las URLs base y configuraciones del backend
 */

// URL base de la API (cambiar según el entorno)
export const API_CONFIG = {
    // Desarrollo local
    baseURL: 'http://localhost:8000',

    // Producción (descomentar cuando esté disponible)
    // baseURL: 'https://api.pymeshoteleras.com',

    // Timeout por defecto (30 segundos)
    timeout: 30000,

    // Headers por defecto
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
};

// Configuración de endpoints específicos
export const ENDPOINTS_CONFIG = {
    v1: {
        prefix: '/api/v1'
    }
};

// Construcción de URL completa
export const buildUrl = (endpoint: string): string => {
    return `${API_CONFIG.baseURL}${ENDPOINTS_CONFIG.v1.prefix}${endpoint}`;
};
