/**
 * Tipos para las respuestas de la API
 */

// Tipos base para las respuestas
export interface BaseApiResponse<T = any> {
    data: T;
    message?: string;
    success: boolean;
    timestamp?: string;
}

export interface PaginatedResponse<T> {
    data: T[];
    pagination: {
        page: number;
        limit: number;
        total: number;
        totalPages: number;
    };
}

// Tipos para hoteles
export interface HotelApiData {
    id: string;
    nombre: string;
    direccion?: string;
    ciudad?: string;
    puntuacion_sostenibilidad?: number;
    puntuacion_calidad?: number;
    total_resenas?: number;
    created_at?: string;
    updated_at?: string;
}

// Tipos para reseñas
export interface ReviewApiData {
    id: string;
    hotel_id: string;
    plataforma: 'google' | 'booking' | 'airbnb' | 'tripadvisor';
    autor: string;
    puntuacion: number;
    comentario: string;
    fecha: string;
    sentimiento?: 'positivo' | 'neutral' | 'negativo';
    created_at?: string;
}

// Tipos para indicadores
export interface IndicatorsSummary {
    total_hoteles: number;
    total_resenas: number;
    promedio_sostenibilidad: number;
    promedio_calidad: number;
    distribucion_plataformas: Record<string, number>;
}

export interface HotelComparisonData {
    hotel_id: string;
    nombre: string;
    sostenibilidad: number;
    calidad: number;
    resenas: number;
    sentiment_score: number;
}

// Tipos para scraping
export interface ScrapingRequest {
    platforms: string[];
    hotel_ids?: string[];
    fecha_inicio?: string;
    fecha_fin?: string;
}

export interface ScrapingResponse {
    task_id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    message: string;
    results?: {
        total_procesados: number;
        exitosos: number;
        fallidos: number;
    };
}

// Tipos para exportación
export interface ExportRequest {
    formato: 'pdf' | 'csv';
    datos: any[];
    opciones?: {
        incluir_graficos?: boolean;
        filtros_aplicados?: string;
    };
}
