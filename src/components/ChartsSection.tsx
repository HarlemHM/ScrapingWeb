import { Card } from "./ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import type { HotelData } from "./ResultsTable"
import { TrendingUp, BarChart3, Smile, Leaf, Star } from "lucide-react"

interface ChartsSectionProps {
  data: HotelData[]
}

export function ChartsSection({ data }: ChartsSectionProps) {
  // Define colors first
  const sentimentColors: { [key: string]: string } = {
    positivo: "#10B981",
    neutral: "#F59E0B",
    negativo: "#EF4444",
  }

  const platformColors: { [key: string]: string } = {
    airbnb: "#FF5A5F",
    booking: "#003580",
    google: "#4285F4",
  }

  // Prepare data for sustainability and quality comparison
  const sustainabilityQualityData = data.map((hotel) => ({
    name: hotel.name.length > 12 ? hotel.name.substring(0, 12) + "..." : hotel.name,
    sustainability: hotel.sustainability,
    quality: hotel.quality,
    reviews: hotel.reviews,
  }))

  // Prepare data for platform distribution
  const platformData = data.reduce(
    (acc, hotel) => {
      const existing = acc.find((item) => item.platform === hotel.platform)
      if (existing) {
        existing.count += 1
      } else {
        acc.push({
          platform: hotel.platform,
          count: 1,
          fill: platformColors[hotel.platform] || "#8884d8",
        })
      }
      return acc
    },
    [] as { platform: string; count: number; fill: string }[],
  )

  // Prepare data for sentiment distribution
  const sentimentData = data.reduce(
    (acc, hotel) => {
      const existing = acc.find((item) => item.sentiment === hotel.sentiment)
      if (existing) {
        existing.count += 1
      } else {
        acc.push({ sentiment: hotel.sentiment, count: 1 })
      }
      return acc
    },
    [] as { sentiment: string; count: number }[],
  )

  // Prepare data for ratings comparison
  const ratingsData = data.map((hotel) => ({
    name: hotel.name.length > 15 ? hotel.name.substring(0, 15) + "..." : hotel.name,
    sustainability: hotel.sustainability,
    quality: hotel.quality,
  }))

  if (data.length === 0) {
    return (
      <Card className="p-16 text-center card-shadow">
        <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
          <BarChart3 className="h-12 w-12 text-gray-400" />
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay datos para visualizar</h3>
        <p className="text-gray-600 max-w-md mx-auto">
          Ejecuta el proceso de extracción o ajusta los filtros para generar gráficos comparativos
        </p>
      </Card>
    )
  }

  return (
    <div className="space-y-8">
      {/* Title */}
      <Card className="p-6 card-shadow">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg">
            <TrendingUp className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-gray-800">Visualización Comparativa</h2>
            <p className="text-gray-600">Gráficos y análisis visual de los hoteles analizados</p>
          </div>
        </div>
      </Card>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Sustainability and Quality Comparison */}
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="h-5 w-5 text-purple-600" />
            <h3 className="text-lg font-semibold text-gray-800">Sostenibilidad y Calidad por Hotel</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sustainabilityQualityData} margin={{ bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} fontSize={12} />
              <YAxis domain={[0, 5]} />
              <Tooltip />
              <Bar dataKey="sustainability" fill="#10B981" name="Sostenibilidad" radius={[2, 2, 0, 0]} />
              <Bar dataKey="quality" fill="#8B5CF6" name="Calidad" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Platform Distribution */}
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="h-5 w-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-800">Distribución por Plataforma</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={platformData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="platform" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Sentiment Distribution */}
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center gap-2 mb-4">
            <Smile className="h-5 w-5 text-green-600" />
            <h3 className="text-lg font-semibold text-gray-800">Distribución de Sentimientos</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={sentimentData.map((item) => ({
                ...item,
                fill: sentimentColors[item.sentiment] || "#8884d8",
              }))}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sentiment" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Ratings Comparison */}
        <Card className="p-6 card-shadow hover:card-shadow-hover transition-all duration-300">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="h-5 w-5 text-orange-600" />
            <h3 className="text-lg font-semibold text-gray-800">Comparación de Calificaciones</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ratingsData} margin={{ bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} fontSize={12} />
              <YAxis domain={[0, 5]} />
              <Tooltip />
              <Bar dataKey="sustainability" fill="#10B981" name="Sostenibilidad" radius={[2, 2, 0, 0]} />
              <Bar dataKey="quality" fill="#8B5CF6" name="Calidad" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Summary Stats */}
      <Card className="p-6 card-shadow">
        <div className="flex items-center gap-2 mb-6">
          <BarChart3 className="h-5 w-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-800">Resumen Estadístico</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-green-600">
                  {data.filter((h) => h.sentiment === "positivo").length}
                </div>
                <div className="text-sm text-green-700 font-medium">Hoteles con Sentimiento Positivo</div>
              </div>
              <div className="p-3 bg-green-200 rounded-lg">
                <Smile className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-blue-600">
                  {(data.reduce((sum, h) => sum + h.sustainability, 0) / data.length).toFixed(1)}
                </div>
                <div className="text-sm text-blue-700 font-medium">Promedio Sostenibilidad</div>
              </div>
              <div className="p-3 bg-blue-200 rounded-lg">
                <Leaf className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-purple-600">
                  {(data.reduce((sum, h) => sum + h.quality, 0) / data.length).toFixed(1)}
                </div>
                <div className="text-sm text-purple-700 font-medium">Promedio Calidad</div>
              </div>
              <div className="p-3 bg-purple-200 rounded-lg">
                <Star className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
