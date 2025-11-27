"use client"

import { Activity, BarChart3, Calendar, FileText, Settings, TrendingUp } from "lucide-react"
import { useState } from "react"
import { ChartsSection } from "./components/ChartsSection"
import { ControlPanel, type FilterValues } from "./components/ControlPanel"
import { Header } from "./components/Header"
import { QualitativeAnalysis } from "./components/QualitativeAnalysis"
import { type HotelData, ResultsTable } from "./components/ResultsTable"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs"

// Importar y normalizar datos de scraping
import airbnbReviewsRaw from "./data-scraping/reseñas_airbnb.json"
import bookingReviewsRaw from "./data-scraping/reseñas_booking.json"
import googleReviewsRaw from "./data-scraping/reseñas_google.json"
import configData from "./data/config.json"
import { buildHotelDataFromScraping } from "./utils/scrapedTransform"

// Transformar datos de scraping a la estructura usada por la app
const { hotels: scrapedHotels, reviews: scrapedReviews } = buildHotelDataFromScraping(
  googleReviewsRaw as any,
  bookingReviewsRaw as any,
  airbnbReviewsRaw as any,
)

const initialHotelData: HotelData[] = scrapedHotels as HotelData[]
const sampleReviews = scrapedReviews

export default function App() {
  const [hotelData, setHotelData] = useState<HotelData[]>(initialHotelData)
  const [filteredData, setFilteredData] = useState<HotelData[]>(initialHotelData)
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(["airbnb", "booking", "google"])
  const [filteredReviews, setFilteredReviews] = useState(sampleReviews)
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState(configData.ui.defaultTab)

  const handleStartScraping = async (platforms: string[]) => {
    setIsLoading(true)

    // Simular proceso de scraping usando configuración
    await new Promise((resolve) => setTimeout(resolve, configData.scraping.delay))

    setSelectedPlatforms(platforms)

    const platformFilteredHotels = initialHotelData.filter((hotel) => platforms.includes(hotel.platform))

    const platformFilteredReviews = {
      positive: sampleReviews.positive.filter((review) => platforms.includes(review.platform)),
      negative: sampleReviews.negative.filter((review) => platforms.includes(review.platform)),
      recent: sampleReviews.recent.filter((review) => platforms.includes(review.platform)),
    }

    setHotelData(platformFilteredHotels)
    setFilteredData(platformFilteredHotels)
    setFilteredReviews(platformFilteredReviews)
    setIsLoading(false)

    // Cambiar automáticamente a la pestaña de resultados después del scraping
    if (configData.ui.autoSwitchToResults) {
      setActiveTab("results")
    }
  }

  const handleApplyFilters = (filters: FilterValues) => {
    const filtered = hotelData.filter((hotel) => {
      return (
        hotel.sustainability >= filters.sustainabilityMin &&
        hotel.quality >= filters.qualityMin &&
        filters.platforms.includes(hotel.platform)
      )
    })

    const filteredHotelNames = new Set(filtered.map((h) => h.name))
    const newFilteredReviews = {
      positive: sampleReviews.positive.filter(
        (review) =>
          filters.platforms.includes(review.platform) &&
          (filteredHotelNames.size === 0 || filteredHotelNames.has(review.hotel)),
      ),
      negative: sampleReviews.negative.filter(
        (review) =>
          filters.platforms.includes(review.platform) &&
          (filteredHotelNames.size === 0 || filteredHotelNames.has(review.hotel)),
      ),
      recent: sampleReviews.recent.filter(
        (review) =>
          filters.platforms.includes(review.platform) &&
          (filteredHotelNames.size === 0 || filteredHotelNames.has(review.hotel)),
      ),
    }

    setFilteredData(filtered)
    setFilteredReviews(newFilteredReviews)

    // Cambiar automáticamente a la pestaña de resultados después de aplicar filtros
    if (configData.ui.autoSwitchToResults) {
      setActiveTab("results")
    }
  }

  return (
    <div className="bg-gradient-to-br from-gray-50 to-blue-50 min-h-screen">
      <Header />

      <div className="container mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          {/* Navigation Tabs */}
          <div className="bg-white rounded-xl card-shadow p-6 mb-8">
            <TabsList className="grid w-full grid-cols-4 bg-gray-100 p-1 rounded-lg">
              <TabsTrigger
                value="control"
                className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                <Settings className="h-4 w-4" />
                <span className="hidden sm:inline">Panel de Control</span>
                <span className="sm:hidden">Control</span>
              </TabsTrigger>
              <TabsTrigger
                value="results"
                className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                <BarChart3 className="h-4 w-4" />
                <span className="hidden sm:inline">Análisis Cuantitativo</span>
                <span className="sm:hidden">Resultados</span>
              </TabsTrigger>
              <TabsTrigger
                value="charts"
                className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                <TrendingUp className="h-4 w-4" />
                <span className="hidden sm:inline">Visualización Comparativa</span>
                <span className="sm:hidden">Gráficos</span>
              </TabsTrigger>
              <TabsTrigger
                value="analysis"
                className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                <FileText className="h-4 w-4" />
                <span className="hidden sm:inline">Análisis Cualitativo</span>
                <span className="sm:hidden">Análisis</span>
              </TabsTrigger>
            </TabsList>
          </div>

          {/* Tab Content */}
          <div className="mb-8">
            <TabsContent value="control" className="mt-0">
              <ControlPanel
                onStartScraping={handleStartScraping}
                onApplyFilters={handleApplyFilters}
                isLoading={isLoading}
              />
            </TabsContent>

            <TabsContent value="results" className="mt-0">
              <ResultsTable 
                data={filteredData} 
                reviews={filteredReviews} 
                config={configData}      
              />
            </TabsContent>

            <TabsContent value="charts" className="mt-0">
              <ChartsSection data={filteredData} />
            </TabsContent>

            <TabsContent value="analysis" className="mt-0">
              <QualitativeAnalysis
                positiveReviews={filteredReviews.positive}
                negativeReviews={filteredReviews.negative}
                recentReviews={filteredReviews.recent}
              />
            </TabsContent>
          </div>

          {/* Status Bar */}
          <div className="bg-white rounded-xl card-shadow p-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
              <div className="flex items-center gap-2 text-blue-600">
                <BarChart3 className="h-4 w-4" />
                <span className="font-medium">Hoteles analizados:</span>
                <span className="font-semibold">{filteredData.length}</span>
              </div>
              <div className="flex items-center gap-2 text-green-600">
                <Calendar className="h-4 w-4" />
                <span className="font-medium">Última actualización:</span>
                <span className="font-semibold">{new Date().toLocaleDateString("es-ES")}</span>
              </div>
              <div className="flex items-center gap-2">
                <Activity className={`h-4 w-4 ${isLoading ? "text-orange-500" : "text-green-500"}`} />
                <span className="font-medium">Estado:</span>
                <span className={`font-semibold ${isLoading ? "text-orange-600" : "text-green-600"}`}>
                  {isLoading ? "Procesando..." : "Listo"}
                </span>
              </div>
            </div>
          </div>
        </Tabs>
      </div>
    </div>
  )
}
