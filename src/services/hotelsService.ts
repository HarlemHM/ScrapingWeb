/**
 * Servicio de Hoteles
 * Endpoints del backend declarados pero no utilizados aún
 */

// ==================================================
// ENDPOINTS DEL BACKEND (DECLARADOS - NO UTILIZADOS)
// ==================================================
export const hotelsEndpoints = {
    // 9.1 Hoteles
    list: {
        method: 'GET',
        url: '/api/v1/hoteles',
        description: 'Listar hoteles'
    },
    create: {
        method: 'POST',
        url: '/api/v1/hoteles',
        description: 'Crear hotel'
    },
    getById: (id: string) => ({
        method: 'GET',
        url: `/api/v1/hoteles/${id}`,
        description: 'Obtener hotel'
    }),
    update: (id: string) => ({
        method: 'PUT',
        url: `/api/v1/hoteles/${id}`,
        description: 'Actualizar hotel'
    }),
    delete: (id: string) => ({
        method: 'DELETE',
        url: `/api/v1/hoteles/${id}`,
        description: 'Eliminar hotel'
    })
};

// Cuando se conecte al backend, descomentar y usar:
// export const fetchHotels = async () => {
//   const response = await fetch(hotelsEndpoints.list.url);
//   return response.json();
// };
