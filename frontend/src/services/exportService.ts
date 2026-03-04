/**
 * Servicio de Exportación
 * Endpoints del backend declarados pero no utilizados aún
 */

// ==================================================
// ENDPOINTS DEL BACKEND (DECLARADOS - NO UTILIZADOS)
// ==================================================
export const exportEndpoints = {
    // 9.5 Exportación
    pdf: {
        method: 'POST',
        url: '/api/v1/export/pdf',
        description: 'Exportar datos a PDF'
    },
    csv: {
        method: 'POST',
        url: '/api/v1/export/csv',
        description: 'Exportar datos a CSV'
    }
};

// Cuando se conecte al backend, descomentar y usar:
// export const exportToPDF = async (data: any) => {
//   const response = await fetch(exportEndpoints.pdf.url, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data)
//   });
//   return response.blob();
// };
//
// export const exportToCSV = async (data: any) => {
//   const response = await fetch(exportEndpoints.csv.url, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data)
//   });
//   return response.blob();
// };
