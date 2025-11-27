/**
 * Cliente HTTP para comunicación con el backend
 * Wrapper alrededor de fetch con manejo de errores y configuración centralizada
 */

import { API_CONFIG } from '../config/api.config';

// Tipos para las respuestas de la API
export interface ApiResponse<T = any> {
    data: T;
    message?: string;
    success: boolean;
}

export interface ApiError {
    message: string;
    status: number;
    errors?: Record<string, string[]>;
}

// Clase ApiClient para manejar todas las comunicaciones HTTP
class ApiClient {
    private baseURL: string;
    private timeout: number;
    private defaultHeaders: Record<string, string>;

    constructor() {
        this.baseURL = API_CONFIG.baseURL;
        this.timeout = API_CONFIG.timeout;
        this.defaultHeaders = API_CONFIG.headers;
    }

    /**
     * Realizar petición HTTP genérica
     */
    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<ApiResponse<T>> {
        const url = `${this.baseURL}${endpoint}`;

        const config: RequestInit = {
            ...options,
            headers: {
                ...this.defaultHeaders,
                ...options.headers,
            },
        };

        // Timeout controller
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        try {
            const response = await fetch(url, {
                ...config,
                signal: controller.signal,
            });

            clearTimeout(timeoutId);

            // Parsear respuesta JSON
            const data = await response.json();

            // Si la respuesta no es exitosa, lanzar error
            if (!response.ok) {
                throw {
                    message: data.message || 'Error en la petición',
                    status: response.status,
                    errors: data.errors,
                } as ApiError;
            }

            return {
                data: data.data || data,
                message: data.message,
                success: true,
            };
        } catch (error: any) {
            // Manejo de errores
            if (error.name === 'AbortError') {
                throw {
                    message: 'Tiempo de espera agotado',
                    status: 408,
                } as ApiError;
            }

            if (error.status) {
                throw error as ApiError;
            }

            throw {
                message: error.message || 'Error de conexión',
                status: 0,
            } as ApiError;
        }
    }

    /**
     * Métodos HTTP
     */
    async get<T>(endpoint: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
        const queryString = params
            ? '?' + new URLSearchParams(params).toString()
            : '';

        return this.request<T>(`${endpoint}${queryString}`, {
            method: 'GET',
        });
    }

    async post<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async put<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, {
            method: 'DELETE',
        });
    }

    /**
     * Métodos especiales para archivos
     */
    async uploadFile<T>(endpoint: string, file: File, fieldName: string = 'file'): Promise<ApiResponse<T>> {
        const formData = new FormData();
        formData.append(fieldName, file);

        return this.request<T>(endpoint, {
            method: 'POST',
            headers: {
                // No incluir Content-Type para que el navegador lo establezca automáticamente con boundary
            },
            body: formData,
        });
    }

    async downloadFile(endpoint: string): Promise<Blob> {
        const url = `${this.baseURL}${endpoint}`;

        const response = await fetch(url, {
            headers: this.defaultHeaders,
        });

        if (!response.ok) {
            throw new Error('Error al descargar archivo');
        }

        return response.blob();
    }

    /**
     * Configurar token de autenticación
     */
    setAuthToken(token: string) {
        this.defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    /**
     * Remover token de autenticación
     */
    removeAuthToken() {
        delete this.defaultHeaders['Authorization'];
    }
}

// Exportar instancia única (Singleton)
export const apiClient = new ApiClient();

// Exportar también la clase por si se necesita crear instancias personalizadas
export default ApiClient;
