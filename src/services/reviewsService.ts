/**
 * Servicio de Reseñas
 * Endpoints del backend declarados pero no utilizados aún
 */

// ==================================================
// ENDPOINTS DEL BACKEND (DECLARADOS - NO UTILIZADOS)
// ==================================================
export const reviewsEndpoints = {
    // 9.2 Reseñas
    getByHotel: (hotelId: string) => ({
        method: 'GET',
        url: `/api/v1/resenas/${hotelId}`,
        description: 'Reseñas filtradas por hotel'
    }),
    getFeatured: (hotelId: string) => ({
        method: 'GET',
        url: `/api/v1/resenas/destacadas/${hotelId}`,
        description: 'Reseñas relevantes/destacadas'
    })
};

// Cuando se conecte al backend, descomentar y usar:
// export const fetchReviewsByHotel = async (hotelId: string) => {
//   const endpoint = reviewsEndpoints.getByHotel(hotelId);
//   const response = await fetch(endpoint.url);
//   return response.json();
// };
