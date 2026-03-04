"use client"

import { useState, useEffect } from "react"
import { Button } from "./ui/button"
import { Checkbox } from "./ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import { Loader2, Database, Filter, Calendar, Leaf, Star, Globe, Search } from "lucide-react"

export interface FilterValues {
  sustainabilityMin: number
  qualityMin: number
  platforms: string[]
  dateFrom?: string
  dateTo?: string
}

interface ControlPanelProps {
  onStartScraping: (platforms: string[]) => void
  onApplyFilters: (filters: FilterValues) => void
  isLoading: boolean
}

export function ControlPanel({ onStartScraping, onApplyFilters, isLoading }: ControlPanelProps) {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(["airbnb", "booking", "google"])
  const [sustainabilityMin, setSustainabilityMin] = useState<string>("all")
  const [qualityMin, setQualityMin] = useState<string>("all")
  const [dateFrom, setDateFrom] = useState<string>("")
  const [dateTo, setDateTo] = useState<string>("")

  const platforms = [
    { id: "airbnb", name: "Airbnb" },
    { id: "booking", name: "Booking.com" },
    { id: "google", name: "Google Reviews" },
  ]

  // Establecer fechas por defecto al cargar el componente
  useEffect(() => {
    const today = new Date()
    const sixMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 6, today.getDate())

    setDateFrom(sixMonthsAgo.toISOString().split("T")[0])
    setDateTo(today.toISOString().split("T")[0])
  }, [])

  const handlePlatformChange = (platformId: string, checked: boolean) => {
    if (checked) {
      setSelectedPlatforms([...selectedPlatforms, platformId])
    } else {
      setSelectedPlatforms(selectedPlatforms.filter((p) => p !== platformId))
    }
  }

  const handleStartScraping = () => {
    if (selectedPlatforms.length === 0) {
      alert("Selecciona al menos una plataforma para el scraping")
      return
    }
    onStartScraping(selectedPlatforms)
  }

  const handleApplyFilters = () => {
    const filters: FilterValues = {
      sustainabilityMin: sustainabilityMin && sustainabilityMin !== "all" ? Number.parseFloat(sustainabilityMin) : 0,
      qualityMin: qualityMin && qualityMin !== "all" ? Number.parseFloat(qualityMin) : 0,
      platforms: selectedPlatforms,
      dateFrom,
      dateTo,
    }
    onApplyFilters(filters)
  }

  return (
    <div className="bg-white rounded-lg card-shadow p-6 transition-all duration-300 hover:card-shadow-hover">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
          <Database className="h-6 w-6 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-gray-800">Panel de Control</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Controles de Scraping */}
        <div className="space-y-6">
          <div className="flex items-center gap-2 mb-4">
            <Globe className="h-5 w-5 text-blue-600" />
            <h3 className="text-lg font-medium text-gray-700">Extracción de Datos</h3>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <label className="block text-sm font-medium text-gray-600 mb-3">Plataformas</label>
            <div className="space-y-3">
              {platforms.map((platform) => (
                <label key={platform.id} className="flex items-center p-2 hover:bg-white rounded-md transition-colors">
                  <Checkbox
                    checked={selectedPlatforms.includes(platform.id)}
                    onCheckedChange={(checked) => handlePlatformChange(platform.id, checked as boolean)}
                    className="mr-3"
                  />
                  <span className="text-sm font-medium">{platform.name}</span>
                </label>
              ))}
            </div>
          </div>

          <Button
            onClick={handleStartScraping}
            disabled={isLoading || selectedPlatforms.length === 0}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-medium py-3 px-4 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Ejecutando Extracción
              </>
            ) : (
              <>
                <Search className="mr-2 h-5 w-5" />
                Iniciar Extracción
              </>
            )}
          </Button>
        </div>

        {/* Filtros */}
        <div className="space-y-6">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="h-5 w-5 text-green-600" />
            <h3 className="text-lg font-medium text-gray-700">Filtros de Análisis</h3>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Calendar className="h-4 w-4 text-gray-500" />
                  <label className="block text-sm font-medium text-gray-600">Fecha Desde</label>
                </div>
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Calendar className="h-4 w-4 text-gray-500" />
                  <label className="block text-sm font-medium text-gray-600">Fecha Hasta</label>
                </div>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Leaf className="h-4 w-4 text-green-600" />
                  <label className="block text-sm font-medium text-gray-600">Sostenibilidad Mín.</label>
                </div>
                <Select value={sustainabilityMin} onValueChange={setSustainabilityMin}>
                  <SelectTrigger className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <SelectValue placeholder="Todas" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todas</SelectItem>
                    <SelectItem value="1">⭐ 1 estrella</SelectItem>
                    <SelectItem value="2">⭐⭐ 2 estrellas</SelectItem>
                    <SelectItem value="3">⭐⭐⭐ 3 estrellas</SelectItem>
                    <SelectItem value="4">⭐⭐⭐⭐ 4 estrellas</SelectItem>
                    <SelectItem value="5">⭐⭐⭐⭐⭐ 5 estrellas</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Star className="h-4 w-4 text-orange-500" />
                  <label className="block text-sm font-medium text-gray-600">Calidad Mín.</label>
                </div>
                <Select value={qualityMin} onValueChange={setQualityMin}>
                  <SelectTrigger className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                    <SelectValue placeholder="Todas" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todas</SelectItem>
                    <SelectItem value="1">⭐ 1 estrella</SelectItem>
                    <SelectItem value="2">⭐⭐ 2 estrellas</SelectItem>
                    <SelectItem value="3">⭐⭐⭐ 3 estrellas</SelectItem>
                    <SelectItem value="4">⭐⭐⭐⭐ 4 estrellas</SelectItem>
                    <SelectItem value="5">⭐⭐⭐⭐⭐ 5 estrellas</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>

          <Button
            onClick={handleApplyFilters}
            className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium py-3 px-4 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            <Filter className="mr-2 h-5 w-5" />
            Aplicar Filtros
          </Button>
        </div>
      </div>
    </div>
  )
}
