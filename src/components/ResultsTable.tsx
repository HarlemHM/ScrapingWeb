"use client"

import { useState } from 'react'; // Necesario para el estado de carga del PDF
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
// 1. Importación estática de jspdf (Soluciona el ChunkLoadError)
import { jsPDF } from 'jspdf'; 
import { Download, FileText, BarChart3, Building2, Leaf, Star, MessageCircle, Globe, Loader2 } from "lucide-react"; // Añadimos Loader2 para la carga

// No es necesario cambiar esta interfaz
export interface HotelData {
  name: string;
  sustainability: number;
  quality: number;
  reviews: number;
  sentiment: "positivo" | "neutral" | "negativo";
  platform: string;
}

// Mantenemos la interfaz de props necesaria para la funcionalidad de exportación
interface ResultsTableProps {
  data: HotelData[];
  reviews: { // Necesario para generar el contenido de reseñas en el PDF
    positive: any[];
    negative: any[];
    recent: any[];
  };
  config: { // Necesario para el nombre del archivo CSV
    export: {
      csvFilename: string;
    };
  };
}

export function ResultsTable({ data, reviews, config }: ResultsTableProps) {
  // Estado para manejar la carga del PDF
  const [isExportingPDF, setIsExportingPDF] = useState(false);
  
  // Funciones de ayuda restauradas a las clases de diseño originales del usuario
  const getSentimentColor = (sentiment: string): string => { 
    switch (sentiment) {
      case "positivo":
        return "bg-green-100 text-green-800 border-green-200";
      case "neutral":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "negativo":
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };
  
  const getSentimentEmoji = (sentiment: string): string => { 
    switch (sentiment) {
      case "positivo":
        return "😊";
      case "neutral":
        return "😐";
      case "negativo":
        return "😞";
      default:
        return "❓";
    }
  };
  
  const formatRating = (rating: number): string => { 
    return rating.toFixed(1);
  };
  
  const averageSustainability = data.length > 0 
    ? (data.reduce((sum, hotel) => sum + hotel.sustainability, 0) / data.length).toFixed(1)
    : "0.0";
  
  const averageQuality = data.length > 0 
    ? (data.reduce((sum, hotel) => sum + hotel.quality, 0) / data.length).toFixed(1)
    : "0.0";

  const totalReviews = data.reduce((sum, hotel) => sum + hotel.reviews, 0);

  // Lógica de exportación CSV (Mantenida)
  const handleExportCSV = () => {
    const csvContent =
      "data:text/csv;charset=utf-8," +
      "Hotel,Sostenibilidad,Calidad,Reseñas,Sentimiento\n" +
      data
        .map(
          (hotel) => `"${hotel.name}",${hotel.sustainability},${hotel.quality},${hotel.reviews},"${hotel.sentiment}"`,
        )
        .join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", config.export.csvFilename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Lógica de exportación PDF (Mantenida)
  const handleExportPDF = async () => {
    setIsExportingPDF(true); // Inicia el estado de carga
    try {
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 15;

      pdf.setFontSize(20);
      pdf.setTextColor(59, 130, 246);
      pdf.text('Análisis de Hoteles - Reporte Completo', margin, 20);
      
      pdf.setFontSize(10);
      pdf.setTextColor(100);
      pdf.text(`Generado: ${new Date().toLocaleDateString('es-ES')}`, margin, 28);

      pdf.setDrawColor(200);
      pdf.line(margin, 32, pageWidth - margin, 32);

      let yPosition = 40;

      pdf.setFontSize(14);
      pdf.setTextColor(0);
      pdf.text('Resumen Estadístico', margin, yPosition);
      yPosition += 8;

      pdf.setFontSize(10);
      pdf.text(`Total de hoteles analizados: ${data.length}`, margin + 5, yPosition);
      yPosition += 6;
      pdf.text(`Hoteles Google: ${data.filter(h => h.platform === 'google').length}`, margin + 5, yPosition);
      yPosition += 6;
      pdf.text(`Hoteles Booking: ${data.filter(h => h.platform === 'booking').length}`, margin + 5, yPosition);
      yPosition += 6;
      pdf.text(`Hoteles Airbnb: ${data.filter(h => h.platform === 'airbnb').length}`, margin + 5, yPosition);
      yPosition += 10;

      pdf.setFontSize(14);
      pdf.text('Top 10 Hoteles por Calidad', margin, yPosition);
      yPosition += 8;

      const top10 = [...data]
        .sort((a, b) => b.quality - a.quality)
        .slice(0, 10);

      pdf.setFontSize(9);
      top10.forEach((hotel, index) => {
        if (yPosition > pageHeight - 30) {
          pdf.addPage();
          yPosition = 20;
        }
        const text = `${index + 1}. ${hotel.name} - Calidad: ${hotel.quality.toFixed(1)}/5 (${hotel.platform})`;
        pdf.text(text, margin + 5, yPosition);
        yPosition += 6;
      });

      yPosition += 5;

      const addReviewsSection = (title: string, reviewsData: any[], color: number[]) => {
        if (yPosition > pageHeight - 30) { pdf.addPage(); yPosition = 20; }
        pdf.setFontSize(12);
        pdf.setTextColor(color[0], color[1], color[2]);
        pdf.text(title, margin, yPosition);
        yPosition += 6;
        pdf.setFontSize(8);
        pdf.setTextColor(0);
        
        reviewsData.slice(0, 5).forEach((review, index) => {
          if (yPosition > pageHeight - 30) { pdf.addPage(); yPosition = 20; }
          const reviewText = `${index + 1}. ${review.hotel} (${review.platform}) - ${review.rating.toFixed(1)}★`;
          pdf.text(reviewText, margin + 3, yPosition);
          yPosition += 5;
          const lines: string[] = pdf.splitTextToSize(`  "${review.text}"`, pageWidth - margin * 2 - 6) as string[];
          lines.forEach((line: string) => {
            if (yPosition > pageHeight - 20) { pdf.addPage(); yPosition = 20; }
            pdf.text(line, margin + 3, yPosition);
            yPosition += 4;
          });
          yPosition += 3;
        });
        yPosition += 5;
      };

      addReviewsSection(`Reseñas Positivas (${reviews.positive.length} total, Top 5)`, reviews.positive, [34, 197, 94]);
      addReviewsSection(`Reseñas Negativas (${reviews.negative.length} total, Top 5)`, reviews.negative, [239, 68, 68]);
      addReviewsSection(`Reseñas Recientes (${reviews.recent.length} total, Top 5)`, reviews.recent, [59, 130, 246]);

      pdf.save(`analisis-hoteles-${new Date().toISOString().split('T')[0]}.pdf`);
      console.log('PDF generado exitosamente'); 
      
    } catch (error) {
      console.error('Error generando PDF:', error);
    } finally {
      setIsExportingPDF(false); // Finaliza el estado de carga
    }
  };


  return (
    <div className="space-y-6">
      {/* Statistics Cards - DISEÑO ORIGINAL RESTAURADO */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-blue-600">{data.length}</div>
              <div className="text-sm text-gray-600 font-medium">Hoteles</div>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Building2 className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-green-600">{averageSustainability}</div>
              <div className="text-sm text-gray-600 font-medium">Sostenibilidad</div>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <Leaf className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-orange-600">{averageQuality}</div>
              <div className="text-sm text-gray-600 font-medium">Calidad</div>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <Star className="h-6 w-6 text-orange-600" />
            </div>
          </div>
        </Card>
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-purple-600">{totalReviews.toLocaleString()}</div>
              <div className="text-sm text-gray-600 font-medium">Reseñas</div>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <MessageCircle className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Export Buttons - DISEÑO ORIGINAL RESTAURADO + Lógica de Carga PDF */}
      <Card className="p-6 card-shadow">
        <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
              <BarChart3 className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Análisis Cuantitativo</h3>
              <p className="text-sm text-gray-600">
                {data.length} hoteles encontrados
              </p>
            </div>
          </div>
          <div className="flex gap-3">
            <Button 
              onClick={handleExportCSV} 
              className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-300"
              size="sm"
            >
              <Download className="mr-2 h-4 w-4" />
              Exportar CSV
            </Button>
            <Button 
              onClick={handleExportPDF} 
              className="bg-red-600 hover:bg-red-700 text-white shadow-lg hover:shadow-xl transition-all duration-300"
              size="sm"
              disabled={isExportingPDF} // Deshabilitar mientras exporta
            >
              {isExportingPDF ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generando...
                </>
              ) : (
                <>
                  <FileText className="mr-2 h-4 w-4" />
                  Exportar PDF
                </>
              )}
            </Button>
          </div>
        </div>
      </Card>

      {/* Results Table - DISEÑO ORIGINAL RESTAURADO */}
      <Card className="p-6 card-shadow">
        {data.length === 0 ? (
          <div className="text-center py-16">
            <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
              <BarChart3 className="h-12 w-12 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No hay resultados disponibles
            </h3>
            <p className="text-gray-600 max-w-md mx-auto">
              Ajusta los filtros o ejecuta el proceso de extracción para obtener datos de hoteles
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="border-b-2">
                  <TableHead className="font-semibold text-gray-700">
                    <div className="flex items-center gap-2">
                      <Building2 className="h-4 w-4" />
                      Hotel
                    </div>
                  </TableHead>
                  <TableHead className="font-semibold text-gray-700 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <Leaf className="h-4 w-4 text-green-600" />
                      Sostenibilidad
                    </div>
                  </TableHead>
                  <TableHead className="font-semibold text-gray-700 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <Star className="h-4 w-4 text-orange-500" />
                      Calidad
                    </div>
                  </TableHead>
                  <TableHead className="font-semibold text-gray-700 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <MessageCircle className="h-4 w-4 text-purple-600" />
                      Reseñas
                    </div>
                  </TableHead>
                  <TableHead className="font-semibold text-gray-700 text-center">Sentimiento</TableHead>
                  <TableHead className="font-semibold text-gray-700 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <Globe className="h-4 w-4" />
                      Plataforma
                    </div>
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((hotel, index) => (
                  <TableRow key={index} className="hover:bg-blue-50 transition-colors duration-200">
                    <TableCell className="font-medium text-gray-900">
                      {hotel.name}
                    </TableCell>
                    <TableCell className="text-center">
                      <div className="flex items-center justify-center gap-1">
                        <Badge className="bg-green-100 text-green-800 hover:bg-green-200 transition-colors">
                          {formatRating(hotel.sustainability)}
                        </Badge>
                        <div className="text-yellow-400">
                          {'★'.repeat(Math.round(hotel.sustainability))}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-center">
                      <div className="flex items-center justify-center gap-1">
                        <Badge className="bg-orange-100 text-orange-800 hover:bg-orange-200 transition-colors">
                          {formatRating(hotel.quality)}
                        </Badge>
                        <div className="text-yellow-400">
                          {'★'.repeat(Math.round(hotel.quality))}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-center">
                      <span className="font-medium text-gray-700">
                        {hotel.reviews.toLocaleString()}
                      </span>
                    </TableCell>
                    <TableCell className="text-center">
                      <Badge className={`${getSentimentColor(hotel.sentiment)} font-medium`}>
                        {getSentimentEmoji(hotel.sentiment)} {hotel.sentiment}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-center">
                      <Badge variant="outline" className="bg-gray-50 hover:bg-gray-100 transition-colors">
                        {hotel.platform}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </Card>
    </div>
  );
}