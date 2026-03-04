/**
 * Utilidades para parsear y trabajar con fechas en español
 */

const MESES_ES: { [key: string]: number } = {
  enero: 0,
  febrero: 1,
  marzo: 2,
  abril: 3,
  mayo: 4,
  junio: 5,
  julio: 6,
  agosto: 7,
  septiembre: 8,
  octubre: 9,
  noviembre: 10,
  diciembre: 11,
}

/**
 * Parsea una fecha en español a objeto Date
 * Formatos soportados:
 * - "agosto de 2025"
 * - "18 de septiembre de 2025"
 * - "2025-07-23"
 * - "Fecha del comentario: 18 de septiembre de 2025"
 */
export function parseDateSpanish(dateStr: string | undefined): Date | null {
  if (!dateStr) return null
  
  const cleaned = dateStr.toLowerCase().trim()
    .replace('fecha del comentario:', '')
    .replace('fecha estimada no disponible', '')
    .trim()
  
  if (!cleaned || cleaned === 'n/a') return null
  
  // Formato ISO: "2025-07-23"
  if (/^\d{4}-\d{2}-\d{2}$/.test(cleaned)) {
    const date = new Date(cleaned)
    return isNaN(date.getTime()) ? null : date
  }
  
  // Formato "agosto de 2025" o "18 de septiembre de 2025"
  const regex = /(\d+\s+de\s+)?(\w+)\s+de\s+(\d{4})/
  const match = cleaned.match(regex)
  
  if (match) {
    const [, dayPart, mes, year] = match
    const mesNum = MESES_ES[mes.toLowerCase()]
    
    if (mesNum !== undefined) {
      const day = dayPart ? parseInt(dayPart.replace(/\D/g, '')) : 1
      const date = new Date(parseInt(year), mesNum, day)
      return isNaN(date.getTime()) ? null : date
    }
  }
  
  return null
}

/**
 * Valida si una fecha está dentro de un rango
 */
export function isDateInRange(
  date: Date | null,
  from: string | undefined,
  to: string | undefined
): boolean {
  if (!date) return true // Si no hay fecha, incluir por defecto
  
  const fromDate = from ? new Date(from) : null
  const toDate = to ? new Date(to) : null
  
  if (fromDate && date < fromDate) return false
  if (toDate && date > toDate) return false
  
  return true
}

/**
 * Formatea una fecha a string legible en español
 */
export function formatDateSpanish(date: Date | null): string {
  if (!date) return 'Fecha no disponible'
  
  const meses = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
  ]
  
  const day = date.getDate()
  const month = meses[date.getMonth()]
  const year = date.getFullYear()
  
  return `${day} de ${month} de ${year}`
}
