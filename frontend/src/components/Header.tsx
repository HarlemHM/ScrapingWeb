import { Building2, MapPin, Star, Leaf } from "lucide-react";

export function Header() {
  return (
    <header className="gradient-bg text-white py-8 shadow-lg">
      <div className="container mx-auto px-6">
        <div className="flex items-center gap-3 mb-2">
          <Building2 className="h-8 w-8" />
          <h1 className="text-3xl font-bold">Sistema de Análisis de Reseñas Hoteleras</h1>
        </div>
        <div className="flex items-center gap-6 text-blue-100">
          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            <span>Barranquilla</span>
          </div>
          <div className="flex items-center gap-2">
            <Leaf className="h-4 w-4" />
            <span>Análisis de Sostenibilidad</span>
          </div>
          <div className="flex items-center gap-2">
            <Star className="h-4 w-4" />
            <span>Evaluación de Calidad</span>
          </div>
        </div>
      </div>
    </header>
  );
}
