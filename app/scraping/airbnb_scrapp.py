from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import time
import json


def cerrar_modal(page):
    """Cierra modales que puedan aparecer"""
    try:
        # Múltiples selectores para diferentes tipos de modales
        modal_selectors = [
            "[data-testid='modal-container']",
            "[role='dialog']",
            "[aria-modal='true']",
            ".modal",
            "[data-testid*='modal']"
        ]

        for selector in modal_selectors:
            modal = page.locator(selector)
            if modal.count() > 0 and modal.first.is_visible():
                print(f"🔹 Modal detectado con selector {selector}, cerrando...")

                # Intentar cerrar con botón de cerrar
                close_selectors = [
                    "button[aria-label*='Cerrar']",
                    "button[aria-label*='Close']",
                    "button[data-testid*='close']",
                    "[data-testid='modal-container'] button:first-child",
                    "svg[viewBox*='0 0 32 32']"  # X de cerrar
                ]

                modal_closed = False
                for close_selector in close_selectors:
                    close_btn = modal.locator(close_selector)
                    if close_btn.count() > 0 and close_btn.first.is_visible():
                        try:
                            close_btn.first.click(timeout=2000)
                            modal.first.wait_for(state="hidden", timeout=3000)
                            modal_closed = True
                            print("✅ Modal cerrado con botón")
                            break
                        except:
                            continue

                # Si no se cerró con botón, usar Escape
                if not modal_closed:
                    page.keyboard.press("Escape")
                    try:
                        modal.first.wait_for(state="hidden", timeout=2000)
                        print("✅ Modal cerrado con Escape")
                    except:
                        pass

                time.sleep(0.5)  # Pausa breve

    except Exception as e:
        print(f"⚠️ Error cerrando modal: {e}")
        # Escape como último recurso
        try:
            page.keyboard.press("Escape")
        except:
            pass


def esperar_sin_overlays(page):
    """Espera a que no haya overlays o elementos de carga"""
    try:
        page.wait_for_selector("[data-testid='modal-container']", state="hidden", timeout=3000)
    except:
        pass
    try:
        page.wait_for_selector("[aria-busy='true']", state="hidden", timeout=3000)
    except:
        pass


def limpiar_url(href):
    """Extrae solo la ruta del room ID"""
    parsed = urlparse(href)
    return parsed.path  # solo /rooms/ID


def guardar_progreso(reseñas, pagina_actual):
    """Guarda el progreso actual en caso de interrupciones"""
    filename = f'reseñas_airbnb_barranquilla_progreso_p{pagina_actual}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reseñas, f, ensure_ascii=False, indent=2)
    print(f"💾 Progreso guardado: {len(reseñas)} reseñas en {filename}")


def scroll_para_cargar_todos(page):
    """Hace scroll incremental hasta que no aparezcan más listados nuevos."""
    prev_count = -1
    while True:
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(1.5)  # dar tiempo a que carguen nuevos elementos
        current_count = page.locator("a[href*='/rooms/']").count()
        if current_count == prev_count:
            break
        prev_count = current_count


def scroll_y_contar_reseñas_mejorado(page):
    """
    Función mejorada que hace scroll Y cuenta las reseñas usando múltiples selectores
    para asegurar que realmente esté cargando todo el contenido.
    """
    print("🔄 Iniciando scroll inteligente para cargar reseñas...")

    # Primero, obtener el número total de reseñas esperadas
    total_esperado = 0
    try:
        # Buscar el elemento que muestra el total de reseñas
        total_element = page.locator("div._1j6cqxi, div:has-text('reseñas'), span:has-text('reseñas')").first
        if total_element.count() > 0:
            total_text = total_element.inner_text()
            import re
            match = re.search(r'(\d+)\s*reseñas', total_text)
            if match:
                total_esperado = int(match.group(1))
                print(f"📊 Total de reseñas esperadas: {total_esperado}")
    except:
        pass

    # Selectores más robustos para contar reseñas
    count_selectors = [
        "div[data-review-id]",  # Selector principal
        "div:has(h2, h3):has(svg[aria-label*='star'])",  # Divs con nombre y estrellas
        "div:has(span:text-matches('\\d+ estrellas'))",  # Divs con texto de estrellas
        "div[data-testid*='review']",  # Divs con testid de review
        "div:has(span[dir='ltr']):has(h2, h3)",  # Divs con texto direccional y nombres
        "[role='listitem']",  # Items de lista
    ]

    prev_max_count = 0
    scroll_count = 0
    max_scrolls = 200  # Aumentado significativamente
    no_change_cycles = 0  # Ciclos consecutivos sin cambios
    max_no_change = 8  # Aumentado para ser más persistente

    while scroll_count < max_scrolls and no_change_cycles < max_no_change:
        # Contar con todos los selectores y tomar el máximo
        current_max_count = 0
        for selector in count_selectors:
            try:
                count = page.locator(selector).count()
                current_max_count = max(current_max_count, count)
            except:
                continue

        print(f"📊 Scroll {scroll_count + 1}: {current_max_count} reseñas detectadas (máximo)")

        # Scroll más agresivo y variado
        try:
            # Alternamos entre diferentes tipos de scroll
            if scroll_count % 4 == 0:
                # Scroll grande hacia abajo
                page.evaluate("""
                    let modal = document.querySelector('[role="dialog"]') || 
                               document.querySelector('[aria-modal="true"]') ||
                               document.querySelector('[data-testid*="modal"]');
                    if (modal) {
                        modal.scrollBy(0, 3000);
                    } else {
                        window.scrollBy(0, 3000);
                    }
                """)
            elif scroll_count % 4 == 1:
                # Scroll al final del contenedor
                page.evaluate("""
                    let modal = document.querySelector('[role="dialog"]') || 
                               document.querySelector('[aria-modal="true"]') ||
                               document.querySelector('[data-testid*="modal"]');
                    if (modal) {
                        modal.scrollTop = modal.scrollHeight;
                    } else {
                        window.scrollTo(0, document.body.scrollHeight);
                    }
                """)
            elif scroll_count % 4 == 2:
                # Scroll intermedio
                page.evaluate("""
                    let modal = document.querySelector('[role="dialog"]') || 
                               document.querySelector('[aria-modal="true"]') ||
                               document.querySelector('[data-testid*="modal"]');
                    if (modal) {
                        modal.scrollBy(0, 2000);
                    } else {
                        window.scrollBy(0, 2000);
                    }
                """)
            else:
                # Scroll gradual
                page.evaluate("""
                    let modal = document.querySelector('[role="dialog"]') || 
                               document.querySelector('[aria-modal="true"]') ||
                               document.querySelector('[data-testid*="modal"]');
                    if (modal) {
                        modal.scrollBy(0, 1500);
                    } else {
                        window.scrollBy(0, 1500);
                    }
                """)

            # Tiempo de espera variable para permitir carga
            if current_max_count > prev_max_count:
                time.sleep(4)  # Más tiempo cuando hay cambios
            else:
                time.sleep(2)  # Menos tiempo cuando no hay cambios

        except Exception as e:
            print(f"⚠️ Error en scroll {scroll_count + 1}: {e}")
            time.sleep(1)

        # Verificar cambios
        if current_max_count > prev_max_count:
            no_change_cycles = 0  # Reset contador si hay cambios
            print(f"✅ Se cargaron {current_max_count - prev_max_count} reseñas adicionales")
        else:
            no_change_cycles += 1
            print(f"⏳ Sin cambios ({no_change_cycles}/{max_no_change})")

        # Verificar si hemos alcanzado el total esperado
        if total_esperado > 0 and current_max_count >= total_esperado * 0.9:  # 90% del total
            print(f"✅ Se alcanzó el 90% del total esperado ({total_esperado})")
            break

        prev_max_count = current_max_count
        scroll_count += 1

        # Cada 15 scrolls, hacer una pausa más larga y limpiar memoria
        if scroll_count % 15 == 0:
            print(f"🔄 Pausa de limpieza después de {scroll_count} scrolls...")
            time.sleep(3)
            # Forzar limpieza de memoria en el navegador
            try:
                page.evaluate("if (window.gc) window.gc();")
            except:
                pass

    final_count = prev_max_count
    print(f"✅ Scroll completado: {final_count} reseñas detectadas después de {scroll_count} scrolls")
    return final_count


def extraer_reseñas_individuales_mejorado(page):
    """
    Función mejorada que extrae reseñas usando múltiples estrategias
    y maneja mejor el lazy loading.
    """
    print("📝 Iniciando extracción mejorada de reseñas...")
    reseñas = []

    # Hacer un último scroll para asegurar que todo esté cargado
    try:
        page.evaluate("""
            let modal = document.querySelector('[role="dialog"]') || 
                       document.querySelector('[aria-modal="true"]');
            if (modal) {
                modal.scrollTop = modal.scrollHeight;
            }
        """)
        time.sleep(2)
    except:
        pass

    # Selectores múltiples para encontrar elementos de reseñas
    review_selectors_prioritarios = [
        "div[data-review-id]",  # Selector principal
        "div[data-testid*='review']",  # Testid de review
        "[role='listitem']",  # Items de lista
    ]

    review_selectors_alternativos = [
        "div:has(h2):has(svg[aria-label*='star'])",  # Divs con nombre y estrellas
        "div:has(h3):has(svg[aria-label*='star'])",  # Variante con h3
        "div:has(span:text-matches('\\d+ estrellas'))",  # Divs con texto de estrellas
        "div:has(span[dir='ltr']):has(h2, h3)",  # Divs con texto direccional y nombres
    ]

    # Intentar con selectores prioritarios primero
    review_elements = None
    elements_count = 0

    for selector in review_selectors_prioritarios:
        try:
            elements = page.locator(selector)
            count = elements.count()
            print(f"🔍 Probando selector prioritario '{selector}': {count} elementos")

            if count > elements_count:
                review_elements = elements
                elements_count = count
                print(f"✅ Mejor selector hasta ahora: '{selector}' con {count} elementos")
        except Exception as e:
            print(f"⚠️ Error con selector '{selector}': {e}")
            continue

    # Si no encontramos suficientes, probar selectores alternativos
    if elements_count < 10:  # Si hay menos de 10, probablemente algo está mal
        print("🔄 Probando selectores alternativos...")
        for selector in review_selectors_alternativos:
            try:
                elements = page.locator(selector)
                count = elements.count()
                print(f"🔍 Probando selector alternativo '{selector}': {count} elementos")

                if count > elements_count:
                    review_elements = elements
                    elements_count = count
                    print(f"✅ Mejor selector alternativo: '{selector}' con {count} elementos")
            except Exception as e:
                print(f"⚠️ Error con selector alternativo '{selector}': {e}")
                continue

    if not review_elements or elements_count == 0:
        print("❌ No se encontraron elementos de reseñas")
        return []

    print(f"📊 Total de elementos a procesar: {elements_count}")

    # Procesar elementos en lotes para mejor rendimiento
    batch_size = 50
    total_batches = (elements_count + batch_size - 1) // batch_size

    for batch in range(total_batches):
        start_idx = batch * batch_size
        end_idx = min(start_idx + batch_size, elements_count)

        print(f"🔄 Procesando lote {batch + 1}/{total_batches} (elementos {start_idx + 1}-{end_idx})...")

        for i in range(start_idx, end_idx):
            try:
                review = review_elements.nth(i)

                # Verificar que el elemento sea visible y válido
                if not review.is_visible():
                    continue

                # Hacer scroll suave hacia el elemento para asegurar que esté completamente cargado
                try:
                    review.scroll_into_view_if_needed()
                    time.sleep(0.1)  # Pausa muy breve
                except:
                    pass

                # Extraer datos con timeouts más cortos para mejor rendimiento
                reseña_data = extraer_datos_reseña(review, page, i + 1)

                if reseña_data:
                    reseñas.append(reseña_data)
                    if (i + 1) % 10 == 0:  # Progreso cada 10 reseñas
                        print(f"📊 Progreso: {len(reseñas)} reseñas válidas de {i + 1} procesadas")

            except Exception as e:
                print(f"❌ Error procesando elemento {i + 1}: {e}")
                continue

        # Pausa breve entre lotes
        if batch < total_batches - 1:
            time.sleep(0.5)

    print(f"🎉 Extracción completada: {len(reseñas)} reseñas válidas de {elements_count} elementos procesados")
    return reseñas


def extraer_datos_reseña(review, page, indice):
    """
    Extrae los datos de una reseña individual de manera optimizada.
    """
    try:
        # Extraer nombre del usuario
        nombre = "N/A"
        try:
            nombre_selectors = [
                "h2", "h3", ".hpipapi", "[data-testid*='user-name']",
                "span[dir='ltr']:first-of-type", "strong"
            ]

            for selector in nombre_selectors:
                nombre_element = review.locator(selector).first
                if nombre_element.count() > 0:
                    nombre_text = nombre_element.inner_text(timeout=1500).strip()
                    if nombre_text and 3 <= len(nombre_text) <= 50:
                        nombre = nombre_text
                        break
        except:
            pass

        # Extraer puntuación
        puntuacion = 0
        try:
            # Buscar texto que contenga "estrellas"
            rating_elements = review.locator("span").filter(has_text="estrellas")
            if rating_elements.count() > 0:
                rating_text = rating_elements.first.inner_text(timeout=1500)
                import re
                match = re.search(r'(\d+)\s*estrellas', rating_text)
                if match:
                    puntuacion = int(match.group(1))

            # Si no encuentra, contar SVGs de estrellas
            if puntuacion == 0:
                star_svgs = review.locator("svg[aria-label*='star'], svg:has(path)")
                puntuacion = min(star_svgs.count(), 5)
        except:
            pass

        # Extraer fecha - MEJORADO para manejar diferentes formatos
        fecha = "N/A"
        try:
            # Selectores específicos basados en el HTML proporcionado
            fecha_selectors = [
                "div.s78n3tv",  # Contenedor principal de fecha
                "div[class*='s78n3tv']",  # Variante del selector
                "div:has-text('agosto')",  # Buscar por mes específico
                "div:has-text('enero')",  # Buscar por mes
                "div:has-text('febrero')",
                "div:has-text('marzo')",
                "div:has-text('abril')",
                "div:has-text('mayo')",
                "div:has-text('junio')",
                "div:has-text('julio')",
                "div:has-text('septiembre')",
                "div:has-text('octubre')",
                "div:has-text('noviembre')",
                "div:has-text('diciembre')"
            ]
            
            # Patrones de fecha más amplios
            patrones_fecha = [
                r'\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+\d{4}',
                r'\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}',
                r'hace\s+un?\s+(día|semana|mes|año)',
                r'hace\s+\d+\s+(días|semanas|meses|años)',
                r'\d{1,2}\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)',
                r'\d{4}',
                r'\d{1,2}/\d{1,2}/\d{4}',
                r'\d{1,2}-\d{1,2}-\d{4}'
            ]
            
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                     "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            
            import re
            
            for selector in fecha_selectors:
                try:
                    fecha_elements = review.locator(selector)
                    for elem in fecha_elements.all()[:5]:  # Aumentar búsqueda
                        text = elem.inner_text(timeout=800).strip()
                        
                        # Buscar con patrones regex
                        for patron in patrones_fecha:
                            match = re.search(patron, text, re.IGNORECASE)
                            if match:
                                fecha = match.group(0)
                                break
                        
                        # Búsqueda alternativa por palabras clave
                        if fecha == "N/A":
                            if (any(mes in text.lower() for mes in meses) or 
                                "hace" in text.lower() or 
                                any(char.isdigit() for char in text)):
                                if len(text) <= 100:  # Evitar textos muy largos
                                    fecha = text
                                    break
                        
                        if fecha != "N/A":
                            break
                    if fecha != "N/A":
                        break
                except:
                    continue
        except:
            pass

        # Extraer comentario
        comentario = "N/A"
        try:
            comment_selectors = [
                "span.l1h825yc", "span[dir='ltr']",
                "div[data-testid*='review-content'] span", "p"
            ]

            comment_candidates = []
            for selector in comment_selectors:
                comment_spans = review.locator(selector).all()
                for span in comment_spans[:3]:  # Limitar búsqueda
                    try:
                        text = span.inner_text(timeout=800).strip()
                        # Filtrar texto que parece ser comentario
                        if (20 <= len(text) <= 1000 and
                                not any(word in text.lower() for word in
                                        ["estrellas", "años en", "año en", "estadía"] + meses)):
                            comment_candidates.append(text)
                    except:
                        continue

            if comment_candidates:
                comentario = max(comment_candidates, key=len)
        except:
            pass

        # Extraer ubicación del usuario - MEJORADO
        ubicacion = "N/A"
        try:
            # Selectores específicos basados en el HTML proporcionado
            ubicacion_selectors = [
                "div.s15w4qkt",  # Selector específico de ubicación
                "div[class*='s15w4qkt']",  # Variante del selector
                "div:has-text('Colombia')",  # Buscar por país
                "div:has-text('Cali')",  # Buscar por ciudad específica
                "div:has-text('Bogotá')",
                "div:has-text('Medellín')",
                "div:has-text('Barranquilla')",
                "div:has-text('Cartagena')"
            ]
            
            ciudades_colombia = [
                "Colombia", "Bogotá", "Medellín", "Cali", "Barranquilla", 
                "Cartagena", "Bucaramanga", "Pereira", "Santa Marta",
                "Manizales", "Ibagué", "Pasto", "Neiva", "Villavicencio"
            ]
            
            for selector in ubicacion_selectors:
                try:
                    ubicacion_elements = review.locator(selector)
                    for elem in ubicacion_elements.all()[:5]:  # Aumentar búsqueda
                        text = elem.inner_text(timeout=800).strip()
                        
                        # Buscar texto que contenga ciudades de Colombia
                        if (any(ciudad in text for ciudad in ciudades_colombia) and
                            "años en Airbnb" not in text and
                            "año en Airbnb" not in text and
                            "Calificación" not in text and
                            "estrellas" not in text and
                            "estadía" not in text and
                            len(text) <= 100):  # Aumentar límite
                            ubicacion = text
                            break
                    if ubicacion != "N/A":
                        break
                except:
                    continue
        except:
            pass

        # Extraer tipo de estadía
        tipo_estadia = "N/A"
        try:
            # Selectores específicos para tipo de estadía
            estadia_selectors = [
                "div.rdyyd4g",  # Selector específico de tipo de estadía
                "div[class*='rdyyd4g']",  # Variante del selector
                "div:has-text('Estadía de varias noches')",
                "div:has-text('Estadía de una noche')",
                "div:has-text('Estadía de')",
                "div:has-text('varias noches')",
                "div:has-text('una noche')"
            ]
            
            tipos_estadia = [
                "Estadía de varias noches",
                "Estadía de una noche", 
                "varias noches",
                "una noche"
            ]
            
            for selector in estadia_selectors:
                try:
                    estadia_elements = review.locator(selector)
                    for elem in estadia_elements.all()[:3]:  # Limitar búsqueda
                        text = elem.inner_text(timeout=800).strip()
                        # Buscar texto que contenga tipos de estadía
                        if (any(tipo in text for tipo in tipos_estadia) and
                            len(text) <= 50):  # Evitar textos muy largos
                            tipo_estadia = text
                            break
                    if tipo_estadia != "N/A":
                        break
                except:
                    continue
        except:
            pass

        # Solo devolver reseñas con información mínima válida
        if nombre != "N/A" and (comentario != "N/A" or puntuacion > 0):
            return {
                "nombre": nombre,
                "ubicacion": ubicacion,
                "puntuacion": puntuacion,
                "fecha": fecha,
                "tipo_estadia": tipo_estadia,
                "comentario": comentario
            }

        return None

    except Exception as e:
        print(f"❌ Error extrayendo datos de reseña {indice}: {e}")
        return None


def extraer_reseñas_alojamiento(page):
    """Extrae todas las reseñas de un alojamiento específico - VERSIÓN MEJORADA"""
    todas_reseñas = []

    try:
        # PASO 1: Hacer scroll hacia abajo para cargar la sección de reseñas
        print("🔍 Buscando sección de reseñas...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        time.sleep(2)
        
        # PASO 2: Cerrar cualquier modal que pueda estar abierto
        print("🔹 Cerrando modales antes de buscar botón de reseñas...")
        cerrar_modal(page)
        time.sleep(1)
        
        # PASO 3: Buscar el botón "Mostrar todas las reseñas" con múltiples estrategias
        show_reviews_selectors = [
            "button[data-testid='pdp-show-all-reviews-button']",
            "button:has-text('Mostrar las')",
            "button:has-text('Mostrar todas las reseñas')",
            "button:has-text('Ver todas las reseñas')",
            "button[aria-label*='reseñas']",
            "button[aria-label*='reviews']",
            "a:has-text('Mostrar las')",
            "a:has-text('Ver todas las reseñas')"
        ]

        show_reviews_btn = None
        print("🔍 Buscando botón de reseñas con selectores específicos...")
        
        for selector in show_reviews_selectors:
            try:
                btn = page.locator(selector)
                if btn.count() > 0:
                    # Verificar que sea visible
                    first_btn = btn.first
                    if first_btn.is_visible():
                        show_reviews_btn = first_btn
                        print(f"✅ Botón encontrado con selector: {selector}")
                        break
            except Exception as e:
                print(f"⚠️ Error con selector {selector}: {e}")
                continue

        # PASO 4: Si no encuentra con selectores específicos, buscar por texto
        if not show_reviews_btn:
            print("🔍 Buscando botón por texto 'reseñas'...")
            try:
                # Buscar botones que contengan "reseñas" pero usar .first para evitar múltiples matches
                btn = page.locator("button:has-text('reseñas')").first
                if btn.count() > 0 and btn.is_visible():
                    show_reviews_btn = btn
                    print("✅ Botón encontrado con texto 'reseñas'")
            except Exception as e:
                print(f"⚠️ Error buscando por texto: {e}")

        # PASO 5: Si aún no encuentra, buscar con JavaScript
        if not show_reviews_btn:
            print("🔍 Buscando botón con JavaScript...")
            try:
                js_result = page.evaluate("""
                    () => {
                        const selectors = [
                            'button[data-testid="pdp-show-all-reviews-button"]',
                            'button:has-text("Mostrar las")',
                            'button:has-text("Mostrar todas las reseñas")',
                            'button:has-text("Ver todas las reseñas")',
                            'button[aria-label*="reseñas"]',
                            'button[aria-label*="reviews"]'
                        ];
                        
                        for (const selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            for (const el of elements) {
                                if (el.offsetParent !== null && el.style.display !== 'none') {
                                    return {
                                        found: true,
                                        selector: selector,
                                        text: el.textContent.trim()
                                    };
                                }
                            }
                        }
                        return { found: false };
                    }
                """)
                
                if js_result.get('found'):
                    print(f"✅ Botón encontrado con JS: {js_result['selector']} - Texto: '{js_result['text']}'")
                    # Intentar hacer clic con JavaScript
                    page.evaluate(f"document.querySelector('{js_result['selector']}').click()")
                    show_reviews_btn = "js_clicked"  # Marcar que se hizo clic con JS
                    
            except Exception as js_error:
                print(f"⚠️ Búsqueda con JavaScript falló: {js_error}")

        # PASO 6: Procesar según si se encontró el botón o no
        if show_reviews_btn:
            if show_reviews_btn != "js_clicked":
                print("🔹 Haciendo clic en el botón de reseñas...")
                
                # Proceso de clic mejorado
                try:
                    show_reviews_btn.scroll_into_view_if_needed()
                    time.sleep(1)

                    # Remover overlays que puedan bloquear
                    page.evaluate("""
                        const overlays = document.querySelectorAll('[style*="z-index"]');
                        overlays.forEach(el => {
                            const zIndex = window.getComputedStyle(el).zIndex;
                            if (zIndex > 1000) {
                                el.style.display = 'none';
                            }
                        });
                    """)

                    # Intentar clic
                    click_successful = False
                    try:
                        show_reviews_btn.click(timeout=8000)
                        click_successful = True
                    except:
                        try:
                            page.evaluate(
                                'document.querySelector("button[data-testid=\\"pdp-show-all-reviews-button\\"]").click()')
                            click_successful = True
                            print("✅ Clic realizado con JavaScript")
                        except:
                            try:
                                show_reviews_btn.press("Enter")
                                click_successful = True
                                print("✅ Clic realizado con Enter")
                            except:
                                pass

                    if not click_successful:
                        print("❌ No se pudo hacer clic en el botón de reseñas")
                        return []

                except Exception as e:
                    print(f"❌ Error haciendo clic en botón: {e}")
                    return []

            # Esperar a que aparezca el modal
            print("🔍 Esperando a que aparezca el modal de reseñas...")
            modal_selectors = ["[role='dialog']", "[data-testid*='modal']", "[aria-modal='true']"]
            modal_found = False

            for selector in modal_selectors:
                try:
                    page.wait_for_selector(selector, timeout=8000)
                    modal_found = True
                    print(f"✅ Modal encontrado con selector: {selector}")
                    break
                except:
                    continue

            if not modal_found:
                print("⚠️ No se encontró el modal, intentando extraer de la página principal...")
                return extraer_reseñas_individuales_mejorado(page)

            time.sleep(2)

            # AQUÍ ESTÁ LA MEJORA PRINCIPAL: Scroll inteligente
            total_detected = scroll_y_contar_reseñas_mejorado(page)

            # Extraer reseñas con el método mejorado
            print("📝 Iniciando extracción con método mejorado...")
            todas_reseñas = extraer_reseñas_individuales_mejorado(page)

            # Cerrar el modal
            try:
                close_selectors = [
                    "button[aria-label*='Cerrar']",
                    "button[aria-label*='Close']",
                    "[role='dialog'] button:first-child"
                ]

                modal_closed = False
                for selector in close_selectors:
                    close_btn = page.locator(selector)
                    if close_btn.count() > 0:
                        close_btn.click(timeout=3000)
                        modal_closed = True
                        break

                if not modal_closed:
                    page.keyboard.press("Escape")

            except:
                page.keyboard.press("Escape")

            time.sleep(1)

        else:
            print("⚠️ No se encontró el botón de reseñas, extrayendo de la página principal...")
            todas_reseñas = extraer_reseñas_individuales_mejorado(page)

    except Exception as e:
        print(f"❌ Error general al extraer reseñas: {e}")

    return todas_reseñas


# Programa principal
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()

    # Configurar timeouts
    page.set_default_timeout(15000)  # 15 segundos por defecto

    page.goto("https://www.airbnb.com.co")

    # Buscar
    page.wait_for_selector("input[data-testid='structured-search-input-field-query']")
    page.fill("input[data-testid='structured-search-input-field-query']", "Barranquilla")
    page.get_by_text("Buscar").click()

    # Lista para almacenar todas las reseñas
    todas_las_reseñas = []

    pagina = 1

    while True:  # Sin límite de páginas
        print(f"\n📄 Procesando página {pagina}...")

        try:
            page.wait_for_selector("a[href*='/rooms/']", timeout=15000)
        except:
            print("⚠️ No se encontraron alojamientos en esta página")
            break

        # Scroll para cargar alojamientos
        scroll_para_cargar_todos(page)

        # Extraer hrefs únicos
        hrefs = []
        links = page.locator("a[href*='/rooms/']")
        for i in range(links.count()):  # Sin límite de alojamientos
            href = links.nth(i).get_attribute("href")
            if href:
                ruta = limpiar_url(href)
                if ruta not in hrefs:
                    hrefs.append(ruta)

        print(f"Se encontraron {len(hrefs)} alojamientos únicos en esta página.")

        # Procesar todos los alojamientos
        hrefs_a_procesar = hrefs

        # Visitar cada alojamiento
        for idx, path in enumerate(hrefs_a_procesar, start=1):
            url_completa = "https://www.airbnb.com.co" + path
            print(f"\n🏠 Procesando alojamiento {idx}/{len(hrefs_a_procesar)} de la página {pagina}")
            print(f"🔗 URL: {url_completa}")

            try:
                cerrar_modal(page)
                esperar_sin_overlays(page)

                # Múltiples intentos de navegación
                navigation_successful = False
                for attempt in range(3):
                    try:
                        page.goto(url_completa, timeout=20000)
                        navigation_successful = True
                        break
                    except Exception as nav_error:
                        print(f"⚠️ Intento {attempt + 1} de navegación falló: {nav_error}")
                        if attempt < 2:  # Si no es el último intento
                            time.sleep(2)
                        continue

                if not navigation_successful:
                    print(f"❌ No se pudo navegar al alojamiento después de 3 intentos")
                    continue

                page.wait_for_selector("h1", timeout=15000)

                # Cerrar modales después de cargar la página
                time.sleep(1)
                cerrar_modal(page)

                # Extraer título
                titulo_element = page.locator("h1").first
                titulo_alojamiento = titulo_element.inner_text().strip() if titulo_element.count() > 0 else "N/A"

                print(f"📋 Título: {titulo_alojamiento}")

                # Extraer reseñas con método mejorado
                reseñas_alojamiento = extraer_reseñas_alojamiento(page)

                # Agregar metadatos a cada reseña
                for reseña in reseñas_alojamiento:
                    reseña["url_alojamiento"] = url_completa
                    reseña["titulo_alojamiento"] = titulo_alojamiento
                    reseña["room_id"] = path.split('/')[-1] if path else "N/A"

                todas_las_reseñas.extend(reseñas_alojamiento)

                print(f"✅ Extraídas {len(reseñas_alojamiento)} reseñas del alojamiento")
                print(f"📊 Total acumulado: {len(todas_las_reseñas)} reseñas")

                # Guardar progreso cada 5 alojamientos (más frecuente)
                if idx % 5 == 0:
                    guardar_progreso(todas_las_reseñas, pagina)
                    print(f"💾 Progreso guardado automáticamente - Total: {len(todas_las_reseñas)} reseñas")

                # Volver a la lista
                page.go_back(timeout=10000)
                page.wait_for_selector("a[href*='/rooms/']", timeout=10000)
                time.sleep(1)

            except Exception as e:
                print(f"❌ Error procesando alojamiento {idx}: {e}")
                continue

        # Ir a siguiente página - VERSIÓN MEJORADA
        try:
            print(f"🔄 Intentando ir a la página {pagina + 1}...")
            
            # Scroll hacia abajo para asegurar que el botón esté visible
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            
            # ESTRATEGIA 1: Buscar botón de siguiente con múltiples selectores mejorados
            next_button_selectors = [
                # Selectores específicos de Airbnb
                "a[aria-label='Siguiente']",
                "a[aria-label='Next']", 
                "button[aria-label='Siguiente']",
                "button[aria-label='Next']",
                # Selectores por texto
                "a:has-text('Siguiente')",
                "button:has-text('Siguiente')",
                "a:has-text('Next')",
                "button:has-text('Next')",
                # Selectores por símbolos
                "a:has-text('→')",
                "button:has-text('→')",
                "a:has-text('>')",
                "button:has-text('>')",
                # Selectores por clases comunes
                "[data-testid*='pagination'] a:last-child",
                "[data-testid*='pagination'] button:last-child",
                ".pagination a:last-child",
                ".pagination button:last-child",
                # Selectores por números de página
                f"a:has-text('{pagina + 1}')",
                f"button:has-text('{pagina + 1}')",
                # Selectores por atributos
                "a[href*='page']",
                "a[href*='offset']",
                "button[data-testid*='next']",
                "button[data-testid*='pagination']"
            ]
            
            next_button = None
            for selector in next_button_selectors:
                try:
                    btn = page.locator(selector)
                    if btn.count() > 0:
                        # Verificar que sea visible y clickeable
                        first_btn = btn.first
                        if first_btn.is_visible():
                            next_button = first_btn
                            print(f"✅ Botón de siguiente encontrado con selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # ESTRATEGIA 2: Si no encuentra botón, buscar por JavaScript
            if not next_button:
                print("🔍 Buscando botón de siguiente con JavaScript...")
                try:
                    # Buscar todos los elementos clickeables que podrían ser de paginación
                    js_result = page.evaluate("""
                        () => {
                            const selectors = [
                                'a[aria-label="Siguiente"]',
                                'a[aria-label="Next"]',
                                'button[aria-label="Siguiente"]',
                                'button[aria-label="Next"]',
                                'a[href*="page"]',
                                'a[href*="offset"]',
                                'button[data-testid*="next"]',
                                'button[data-testid*="pagination"]'
                            ];
                            
                            for (const selector of selectors) {
                                const elements = document.querySelectorAll(selector);
                                for (const el of elements) {
                                    if (el.offsetParent !== null && el.style.display !== 'none') {
                                        return {
                                            found: true,
                                            selector: selector,
                                            text: el.textContent.trim(),
                                            href: el.href || null
                                        };
                                    }
                                }
                            }
                            return { found: false };
                        }
                    """)
                    
                    if js_result.get('found'):
                        print(f"✅ Botón encontrado con JS: {js_result['selector']} - Texto: '{js_result['text']}'")
                        # Intentar hacer clic con JavaScript
                        page.evaluate(f"document.querySelector('{js_result['selector']}').click()")
                        page.wait_for_selector("a[href*='/rooms/']", timeout=15000)
                        pagina += 1
                        print(f"✅ Navegación exitosa con JavaScript a la página {pagina}")
                        time.sleep(2)
                        continue
                        
                except Exception as js_error:
                    print(f"⚠️ Búsqueda con JavaScript falló: {js_error}")
            
            # ESTRATEGIA 3: Intentar navegación directa por URL
            if not next_button:
                print("🔍 Intentando navegación directa por URL...")
                try:
                    current_url = page.url
                    if 'items_offset=' in current_url:
                        # Extraer offset actual y aumentarlo
                        import re
                        match = re.search(r'items_offset=(\d+)', current_url)
                        if match:
                            current_offset = int(match.group(1))
                            new_offset = current_offset + 20  # Airbnb suele mostrar 20 items por página
                            new_url = current_url.replace(f'items_offset={current_offset}', f'items_offset={new_offset}')
                            page.goto(new_url)
                            page.wait_for_selector("a[href*='/rooms/']", timeout=15000)
                            pagina += 1
                            print(f"✅ Navegación exitosa por URL a la página {pagina}")
                            time.sleep(2)
                            continue
                except Exception as url_error:
                    print(f"⚠️ Navegación por URL falló: {url_error}")
            
            # ESTRATEGIA 4: Buscar botón de siguiente en el contenedor de paginación
            if not next_button:
                print("🔍 Buscando en contenedores de paginación...")
                try:
                    pagination_containers = page.locator("nav, div[role='navigation'], .pagination, [data-testid*='pagination']")
                    for container in pagination_containers.all():
                        if container.is_visible():
                            # Buscar botones dentro del contenedor
                            buttons = container.locator("a, button")
                            for btn in buttons.all():
                                if btn.is_visible():
                                    text = btn.inner_text().strip().lower()
                                    if any(word in text for word in ['siguiente', 'next', '→', '>', str(pagina + 1)]):
                                        next_button = btn
                                        print(f"✅ Botón encontrado en contenedor: '{text}'")
                                        break
                            if next_button:
                                break
                except Exception as container_error:
                    print(f"⚠️ Búsqueda en contenedores falló: {container_error}")
            
            # Si encontramos un botón, hacer clic
            if next_button:
                try:
                    # Hacer scroll al botón para asegurar que esté visible
                    next_button.scroll_into_view_if_needed()
                    time.sleep(2)  # Aumentar tiempo de espera
                    
                    # Intentar hacer clic
                    next_button.click(timeout=10000)  # Aumentar timeout
                    
                    # Esperar a que la nueva página cargue
                    page.wait_for_selector("a[href*='/rooms/']", timeout=15000)
                    
                    # Verificar que realmente cambió de página
                    current_url = page.url
                    print(f"🔗 Nueva URL: {current_url}")
                    
                    pagina += 1
                    print(f"✅ Navegación exitosa a la página {pagina}")
                    time.sleep(2)  # Pausa adicional para estabilizar
                    
                except Exception as click_error:
                    print(f"❌ Error haciendo clic en botón siguiente: {click_error}")
                    print(" Intentando navegación alternativa...")
                    
                    # Intentar navegación con JavaScript
                    try:
                        page.evaluate("""
                            const nextBtn = document.querySelector('a[aria-label="Siguiente"]') || 
                                           document.querySelector('a[aria-label="Next"]') ||
                                           document.querySelector('button[aria-label="Siguiente"]') ||
                                           document.querySelector('button[aria-label="Next"]') ||
                                           document.querySelector('a[href*="page"]') ||
                                           document.querySelector('button[data-testid*="next"]');
                            if (nextBtn) {
                                nextBtn.click();
                            }
                        """)
                        page.wait_for_selector("a[href*='/rooms/']", timeout=15000)
                        pagina += 1
                        print(f"✅ Navegación exitosa con JavaScript a la página {pagina}")
                        time.sleep(2)
                    except Exception as js_error:
                        print(f"❌ Navegación con JavaScript falló: {js_error}")
                        print("✅ No hay más páginas disponibles.")
                        break
            else:
                print("✅ No se encontró botón de siguiente página. Fin del scraping.")
                break
                
        except Exception as e:
            print(f"❌ Error general en navegación: {e}")
            print("✅ Terminando scraping.")
            break

# Guardar resultado final
print(f"\n Scraping completado!")
print(f"📊 Total de reseñas extraídas: {len(todas_las_reseñas)}")

# Guardar resultado final
filename_final = 'reseñas_airbnb_barranquilla_final.json'
with open(filename_final, 'w', encoding='utf-8') as f:
    json.dump(todas_las_reseñas, f, ensure_ascii=False, indent=2)

print(f"💾 Resultado final guardado en: {filename_final}")