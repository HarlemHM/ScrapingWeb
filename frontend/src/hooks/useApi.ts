/**
 * Hook personalizado para manejar llamadas a la API
 * Proporciona estado de carga, error y datos
 */

import { useState, useCallback } from 'react';
import { apiClient, type ApiError, type ApiResponse } from '../lib/apiClient';

interface UseApiState<T> {
    data: T | null;
    loading: boolean;
    error: ApiError | null;
    execute: (...args: any[]) => Promise<T | null>;
    reset: () => void;
}

/**
 * Hook genérico para llamadas a la API
 * Ejemplo de uso (cuando se conecte al backend):
 * 
 * const { data, loading, error, execute } = useApi<HotelApiData[]>();
 * 
 * useEffect(() => {
 *   execute(() => apiClient.get('/api/v1/hoteles'));
 * }, []);
 */
export function useApi<T = any>(): UseApiState<T> {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<ApiError | null>(null);

    const execute = useCallback(async (apiCall: () => Promise<ApiResponse<T>>): Promise<T | null> => {
        try {
            setLoading(true);
            setError(null);

            const response = await apiCall();
            setData(response.data);

            return response.data;
        } catch (err: any) {
            const apiError: ApiError = {
                message: err.message || 'Error desconocido',
                status: err.status || 0,
                errors: err.errors
            };

            setError(apiError);
            setData(null);

            return null;
        } finally {
            setLoading(false);
        }
    }, []);

    const reset = useCallback(() => {
        setData(null);
        setError(null);
        setLoading(false);
    }, []);

    return { data, loading, error, execute, reset };
}

/**
 * Hook para llamadas a la API con datos inmediatos
 * Similar a useApi pero ejecuta automáticamente al montar
 */
export function useApiImmediate<T = any>(
    apiCall: () => Promise<ApiResponse<T>>,
    dependencies: any[] = []
): UseApiState<T> {
    const { data, loading, error, execute, reset } = useApi<T>();

    // Este hook se puede usar cuando esté listo el backend
    // useEffect(() => {
    //   execute(apiCall);
    // }, dependencies);

    return { data, loading, error, execute, reset };
}
