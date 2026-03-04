import type { HotelData } from "../components/ResultsTable"

// Tipos mínimos para evitar any y manejar estructuras distintas
type GoogleCityReviews = {
  [city: string]: Array<{
    nombre: string
    comentarios: Array<{
      usuario: string
      puntuacion: string // "4/5"
      fecha?: string
      texto: string
      fuente: string
    }>
  }>
}

type BookingReviews = {
  comentarios_parciales: Array<{
    hotel: string
    usuario: string
    puntuacion: string // "8,0"
    Registro?: string // "Fecha del comentario: ..."
    positivo?: string
    negativo?: string
    url?: string
  }>
}

type AirbnbReview = {
  nombre: string
  ubicacion?: string
  puntuacion: number // 1-5
  fecha?: string
  tipo_estadia?: string
  comentario: string
  url_alojamiento?: string
  titulo_alojamiento?: string
  room_id?: string
}

// Utilidades
function toNumber(value: string): number | null {
  if (!value) return null
  // "4/5" -> 4
  if (value.includes("/")) {
    const [num, den] = value.split("/")
    const n = Number.parseFloat(num.replace(",", "."))
    const d = Number.parseFloat(den.replace(",", ".")) || 5
    if (!isNaN(n) && !isNaN(d) && d > 0) return (n / d) * 5
    return null
  }
  // "8,0" -> 8.0 (Booking escala 10)
  const parsed = Number.parseFloat(value.replace(",", "."))
  if (!isNaN(parsed)) {
    // Si parece escala 10, normalizar a 5
    return parsed > 5 ? parsed / 2 : parsed
  }
  return null
}

function sentimentFromRating(rating: number): "positivo" | "neutral" | "negativo" {
  if (rating >= 4.2) return "positivo"
  if (rating >= 3.2) return "neutral"
  return "negativo"
}

// Validar si el texto es válido (no vacío, no N/A, etc.)
function isValidText(text: string): boolean {
  if (!text) return false
  const normalized = text.trim().toLowerCase()
  
  // Textos inválidos comunes
  const invalidTexts = ["", "n/a", "sin comentario", "si", "no", "ok", "bien", "mal"]
  if (invalidTexts.includes(normalized)) return false
  
  // Muy corto para ser útil (mínimo 20 caracteres)
  if (normalized.length < 20) return false
  
  return true
}

// Detectar si un texto tiene sentimiento positivo (para filtrar negativos mal clasificados)
function hasPositiveSentiment(text: string): boolean {
  const normalized = text.toLowerCase()
  
  const positiveWords = [
    "excelente", "excellent", "muy bien", "perfecto", "increíble", "maravilloso",
    "espectacular", "fantástico", "genial", "buenísimo", "recomiendo", "recomendado",
    "encantó", "hermoso", "limpio", "cómodo", "amable", "atento", "atentos",
    "confortable", "tranquil", "económico", "buena ubicación", "buen ubicado",
    "good", "great", "amazing", "wonderful", "nice", "comfortable", "clean",
    "decoración", "especial", "atención", "servicio"
  ]
  
  // Contar cuántas palabras positivas aparecen
  const positiveCount = positiveWords.filter(word => normalized.includes(word)).length
  
  // Si tiene 2 o más palabras positivas, es claramente positivo
  return positiveCount >= 2
}

// Detectar si un texto tiene sentimiento negativo (para filtrar positivos mal clasificados)
function hasNegativeSentiment(text: string): boolean {
  const normalized = text.toLowerCase()
  
  const negativeWords = [
    "malo", "mala", "terrible", "pésimo", "horrible", "desagradable", "sucio", "sucia",
    "incómodo", "ruidoso", "ruido", "mal estado", "decepción", "decepcionante",
    "no recomiendo", "deplorable", "deficiente", "problema", "problemas",
    "quejas", "queja", "insatisfecho", "pobre", "desastre", "awful", "bad",
    "dirty", "noisy", "disappointed", "worst", "never again", "nunca más",
    "falta", "faltan", "no funciona", "roto", "viejo", "antiguo", "descuidado"
  ]
  
  // Contar cuántas palabras negativas aparecen
  const negativeCount = negativeWords.filter(word => normalized.includes(word)).length
  
  // Si tiene 2 o más palabras negativas, es claramente negativo
  return negativeCount >= 2
}

export type NormalizedReview = {
  hotel: string
  text: string
  rating: number
  date?: string
  platform: "google" | "booking" | "airbnb"
}

export type ReviewsBuckets = {
  positive: NormalizedReview[]
  negative: NormalizedReview[]
  recent: NormalizedReview[]
}

export function buildHotelDataFromScraping(
  googleRaw: GoogleCityReviews,
  bookingRaw: BookingReviews,
  airbnbRaw: AirbnbReview[],
): { hotels: HotelData[]; reviews: ReviewsBuckets } {
  const hotelsMap = new Map<string, { sum: number; count: number; platform: string }>()
  const reviews: NormalizedReview[] = []

  console.log("🔍 Iniciando procesamiento de datos...")

  // ====== GOOGLE - PROCESAR TODAS LAS CIUDADES ======
  console.log("📍 Google - Ciudades encontradas:", Object.keys(googleRaw))
  
  Object.entries(googleRaw).forEach(([city, hotels]) => {
    console.log(`  → Procesando ${city}: ${hotels?.length || 0} hoteles`)
    
    hotels?.forEach((entry) => {
      const hotelName = entry.nombre?.trim() || "Hotel Google"
      
      entry.comentarios?.forEach((c) => {
        const rating = toNumber(c.puntuacion) ?? 0
        const text = c.texto || ""
        
        // Validar que el texto sea útil
        if (!isValidText(text)) return
        
        reviews.push({ 
          hotel: hotelName, 
          text, 
          rating, 
          date: c.fecha, 
          platform: "google" 
        })
        
        const key = `${hotelName}::google`
        const agg = hotelsMap.get(key) || { sum: 0, count: 0, platform: "google" }
        agg.sum += rating
        agg.count += 1
        hotelsMap.set(key, agg)
      })
    })
  })

  const googleReviewsCount = reviews.filter(r => r.platform === "google").length
  console.log(`✅ Google: ${googleReviewsCount} reseñas procesadas`)

  // ====== BOOKING ======
  bookingRaw.comentarios_parciales?.forEach((c) => {
    const hotelName = c.hotel?.trim() || "Hotel Booking"
    const rating = toNumber(c.puntuacion) ?? 0
    const date = c.Registro?.replace("Fecha del comentario:", "").trim()
    
    // Crear reseña positiva si existe texto positivo
    if (c.positivo && isValidText(c.positivo)) {
      reviews.push({ 
        hotel: hotelName, 
        text: c.positivo, 
        rating: Math.max(rating, 4.0), // Asegurar que sea tratada como positiva
        date, 
        platform: "booking" 
      })
      
      const key = `${hotelName}::booking`
      const agg = hotelsMap.get(key) || { sum: 0, count: 0, platform: "booking" }
      agg.sum += rating
      agg.count += 1
      hotelsMap.set(key, agg)
    }
    
    // Crear reseña negativa si existe texto negativo
    if (c.negativo && isValidText(c.negativo)) {
      reviews.push({ 
        hotel: hotelName, 
        text: c.negativo, 
        rating: Math.min(rating, 2.5), // Asegurar que sea tratada como negativa
        date, 
        platform: "booking" 
      })
      
      // No agregar de nuevo a hotelsMap si ya se agregó con el positivo
      if (!c.positivo || !isValidText(c.positivo)) {
        const key = `${hotelName}::booking`
        const agg = hotelsMap.get(key) || { sum: 0, count: 0, platform: "booking" }
        agg.sum += rating
        agg.count += 1
        hotelsMap.set(key, agg)
      }
    }
  })

  const bookingReviewsCount = reviews.filter(r => r.platform === "booking").length
  console.log(`✅ Booking: ${bookingReviewsCount} reseñas procesadas`)

  // ====== AIRBNB ======
  airbnbRaw?.forEach((c) => {
    const userName = c.nombre?.toLowerCase() || ""
    
    // Filtrar respuestas del hotel (nombre contiene "respuesta")
    if (userName.includes("respuesta")) return
    
    // Filtrar puntuaciones de 0 (típicamente respuestas o datos inválidos)
    const rating = typeof c.puntuacion === "number" ? c.puntuacion : toNumber(String(c.puntuacion)) || 0
    if (rating === 0) return
    
    const hotelName = c.titulo_alojamiento?.trim() || "Airbnb Listing"
    const text = c.comentario || ""
    
    // Validar que el texto sea útil
    if (!isValidText(text)) return
    
    reviews.push({ 
      hotel: hotelName, 
      text, 
      rating, 
      date: c.fecha, 
      platform: "airbnb" 
    })
    
    const key = `${hotelName}::airbnb`
    const agg = hotelsMap.get(key) || { sum: 0, count: 0, platform: "airbnb" }
    agg.sum += rating
    agg.count += 1
    hotelsMap.set(key, agg)
  })

  const airbnbReviewsCount = reviews.filter(r => r.platform === "airbnb").length
  console.log(`✅ Airbnb: ${airbnbReviewsCount} reseñas procesadas`)

  // ====== CONSTRUIR HOTELES ======
  const hotels: HotelData[] = Array.from(hotelsMap.entries()).map(([key, agg]) => {
    const [name, platform] = key.split("::")
    const quality = agg.count > 0 ? agg.sum / agg.count : 0
    const sentiment = sentimentFromRating(quality)
    const sustainability = quality
    
    return {
      name,
      sustainability,
      quality,
      reviews: agg.count,
      sentiment,
      platform: platform as HotelData["platform"],
    }
  })

  console.log(`🏨 Total hoteles: ${hotels.length}`)
  console.log(`   - Google: ${hotels.filter(h => h.platform === "google").length}`)
  console.log(`   - Booking: ${hotels.filter(h => h.platform === "booking").length}`)
  console.log(`   - Airbnb: ${hotels.filter(h => h.platform === "airbnb").length}`)

  // ====== BUCKETS DE RESEÑAS - BALANCEADOS POR PLATAFORMA ======
  // Separar por plataforma primero
    const googleReviews = reviews.filter(r => r.platform === "google")
  const bookingReviews = reviews.filter(r => r.platform === "booking")
  const airbnbReviews = reviews.filter(r => r.platform === "airbnb")

  // Función helper para balancear y filtrar por sentimiento
  const balanceReviews = (filterFn: (r: NormalizedReview) => boolean) => {
    return [
      ...googleReviews.filter(filterFn),
      ...bookingReviews.filter(filterFn),
      ...airbnbReviews.filter(filterFn),
    ]
  }

  // Positivas: rating alto Y sin palabras negativas
  const positive = balanceReviews((r) => {
    return r.rating >= 4.2 && !hasNegativeSentiment(r.text)
  })
  
  // Negativas: rating bajo Y sin palabras positivas
  const negative = balanceReviews((r) => {
    return r.rating <= 2.6 && !hasPositiveSentiment(r.text)
  })
  
  const recent = balanceReviews((r) => {
    return r.date !== undefined && r.date !== "Fecha estimada no disponible"
  })
  
  console.log("📊 Reseñas clasificadas en buckets:")
  console.log(`   - Positivas: ${positive.length}`)
  console.log(`   - Negativas: ${negative.length}`)
  console.log(`   - Recientes: ${recent.length}`)

  return { hotels, reviews: { positive, negative, recent } }
}