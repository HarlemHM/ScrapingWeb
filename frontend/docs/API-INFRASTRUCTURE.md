# Infraestructura de Comunicación con el Backend

## Resumen

Este proyecto incluye una infraestructura completa para la comunicación con el backend, lista para ser utilizada cuando los endpoints estén disponibles.

## Estructura Creada

### 1. Configuración (`src/config/api.config.ts`)
- **API_CONFIG**: Configuración base de la API (URL, timeout, headers)
- **ENDPOINTS_CONFIG**: Configuración de prefijos de versión
- **buildUrl()**: Función helper para construir URLs completas

### 2. Cliente HTTP (`src/lib/apiClient.ts`)
Cliente HTTP completo con:
- ✅ Métodos HTTP: `get()`, `post()`, `put()`, `delete()`
- ✅ Manejo de timeouts configurables
- ✅ Manejo centralizado de errores
- ✅ Soporte para autenticación con tokens
- ✅ Upload y download de archivos
- ✅ Singleton pattern para instancia única

### 3. Tipos TypeScript (`src/types/api.types.ts`)
Definiciones de tipos para:
- Respuestas base de la API
- Hoteles
- Reseñas
- Indicadores
- Scraping
- Exportación

### 4. Custom Hook (`src/hooks/useApi.ts`)
Hook personalizado para React que proporciona:
- Estado de carga (`loading`)
- Manejo de errores (`error`)
- Datos de respuesta (`data`)
- Función para ejecutar llamadas (`execute`)
- Función para resetear estado (`reset`)

### 5. Declaración de Endpoints (`src/services/`)
Todos los endpoints del backend declarados en:
- `hotelsService.ts`
- `reviewsService.ts`
- `indicatorsService.ts`
- `scrapingService.ts`
- `exportService.ts`
- `index.ts` (exportación centralizada)

## Ejemplo de Uso Futuro

### Cuando el backend esté disponible:

```typescript
// 1. Importar el hook y cliente
import { useApi } from '@/hooks/useApi';
import { apiClient } from '@/lib/apiClient';

// 2. En un componente
function HotelsComponent() {
  const { data, loading, error, execute } = useApi<HotelApiData[]>();

  useEffect(() => {
    execute(() => apiClient.get('/api/v1/hoteles'));
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{/* Renderizar data */}</div>;
}
```

### Configurar autenticación:

```typescript
import { apiClient } from '@/lib/apiClient';

// Establecer token
apiClient.setAuthToken('mi-token-jwt');

// Remover token
apiClient.removeAuthToken();
```

### Cambiar URL base según entorno:

Editar `src/config/api.config.ts`:
```typescript
export const API_CONFIG = {
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://api.pymeshoteleras.com'
    : 'http://localhost:8000',
  // ...
};
```

## Checklist de Activación

Cuando esté listo para conectar al backend:

- [ ] Actualizar `API_CONFIG.baseURL` en `api.config.ts`
- [ ] Descomentar las funciones de ejemplo en los archivos de servicio
- [ ] Implementar las llamadas en los hooks personalizados
- [ ] Descomentar `useEffect` en `useApiImmediate` si se usa
- [ ] Añadir manejo de tokens de autenticación si es necesario
- [ ] Probar la conexión con el backend

## Ventajas de esta Arquitectura

✅ **Centralización**: Un solo punto de configuración y manejo de errores
✅ **Tipado**: TypeScript en toda la capa de comunicación
✅ **Reutilizable**: Hooks y cliente pueden usarse en cualquier componente
✅ **Mantenible**: Fácil de actualizar y extender
✅ **Testeable**: Cada capa puede ser testeada independientemente
