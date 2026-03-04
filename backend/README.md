# ScrapingWeb Backend 🚀

Sistema de Análisis de Reseñas Hoteleras para evaluar **Sostenibilidad** y **Calidad** mediante scraping de plataformas (Google, Booking, Airbnb).

## 📋 Características

 
 ## Descripción General
 
 ScrapingWeb es un sistema backend desarrollado en Python con FastAPI para el análisis de sostenibilidad y calidad de hoteles mediante el scraping de reseñas en plataformas como Airbnb, Booking y Google. El backend procesa, almacena y analiza datos de reseñas, permitiendo la generación de indicadores y reportes que apoyan la toma de decisiones y la visualización de gráficos en el frontend.
 
 ## Propósito del Proyecto
 
 - **Automatizar la recolección de reseñas hoteleras** desde múltiples plataformas.
 - **Analizar el sentimiento y la calidad** de las reseñas usando técnicas de NLP (Procesamiento de Lenguaje Natural).
 - **Generar indicadores de sostenibilidad y calidad** para hoteles.
 - **Exportar reportes** en PDF y Excel.
 - **Proveer una API REST** para el consumo por el frontend y otros sistemas.
 - **Facilitar la visualización de gráficos** en el frontend a partir de los datos procesados.
 
 ## Arquitectura y Componentes
 
 - **FastAPI**: Framework principal para la API REST.
 - **SQLAlchemy + Alembic**: ORM y migraciones para PostgreSQL.
 - **Celery + Redis**: Procesamiento de tareas en background (scraping, análisis NLP, generación de reportes).
 - **spaCy, NLTK, TextBlob, scikit-learn**: Procesamiento y análisis de texto.
 - **Docker & Docker Compose**: Contenerización y orquestación de servicios.
 - **pgAdmin**: Administración visual de la base de datos.
 
 ## Estructura de Carpetas
 
 - `app/`: Código principal del backend.
    - `core/`: Configuración, eventos, seguridad y logging.
    - `crud/`: Operaciones CRUD sobre los modelos.
    - `db/`: Base de datos y migraciones.
    - `models/`: Modelos ORM de la base de datos.
    - `routers/`: Endpoints de la API.
    - `schemas/`: Esquemas Pydantic para validación y serialización.
    - `scraping/`: Scripts de scraping para cada plataforma.
    - `seeds/`: Datos iniciales para la BD.
    - `services/`: Lógica de negocio (scraping, NLP, exportación, indicadores).
    - `workers/`: Tareas de Celery.
 - `alembic/`: Migraciones de la base de datos.
 - `exports/`: Archivos exportados (PDF, Excel).
 - `requirements.txt`: Dependencias Python.
 - `Dockerfile`: Imagen Docker del backend.
 - `docker-compose.yml`: Orquestación de servicios.
 - `.env`: Variables de entorno.
 
 ## Dockerización
 
 El backend está completamente dockerizado para facilitar la instalación, despliegue y escalabilidad. Los servicios principales son:
 
 - **db**: PostgreSQL para almacenamiento de datos.
 - **redis**: Cola de tareas para Celery.
 - **backend**: API FastAPI.
 - **celery_worker**: Procesa tareas en background.
 - **celery_beat**: Scheduler para tareas periódicas (scraping diario).
 - **pgadmin**: Administración visual de la BD.
 
 ### Comandos principales
 
 ```bash
 # Construir y levantar los servicios
 $ docker-compose build
 $ docker-compose up -d
 ```
 
 ## Endpoints Principales
 
 - **Hoteles**
    - `GET /api/v1/hoteles`: Listar hoteles.
    - `POST /api/v1/hoteles`: Crear hotel.
    - `GET /api/v1/hoteles/{id}`: Obtener hotel por ID.
    - `PUT /api/v1/hoteles/{id}`: Actualizar hotel.
    - `DELETE /api/v1/hoteles/{id}`: Eliminar hotel.
 
 - **Scraping**
    - `POST /api/v1/scraping`: Iniciar scraping de reseñas.
    - `GET /api/v1/scraping/status`: Consultar estado de scraping.
 
 - **Reseñas**
    - `GET /api/v1/resenas`: Listar reseñas.
    - `GET /api/v1/resenas/{id}`: Obtener reseña por ID.
    - `GET /api/v1/resenas/hotel/{hotel_id}`: Reseñas por hotel.
 
 - **Indicadores**
    - `GET /api/v1/indicadores`: Listar indicadores calculados.
    - `GET /api/v1/indicadores/hotel/{hotel_id}`: Indicadores por hotel.
 
 - **Exportación**
    - `POST /api/v1/export/pdf`: Exportar reporte PDF.
    - `POST /api/v1/export/excel`: Exportar reporte Excel.
 
 ## Procesamiento de Reseñas y Creación de Gráficos
 
 - El backend realiza scraping de reseñas desde Airbnb, Booking y Google.
 - Aplica técnicas de NLP para analizar el sentimiento y clasificar las reseñas.
 - Calcula indicadores de sostenibilidad y calidad hotelera.
 - Los datos procesados se exponen vía API para que el frontend genere gráficos interactivos (por hotel, por plataforma, por periodo, por criterio, etc.).
 - Permite exportar los resultados en PDF y Excel para informes.
 
 ## Variables de Entorno (.env)
 
 Configura credenciales y parámetros para:
 - Base de datos PostgreSQL
 - Redis
 - Celery
 - JWT y CORS
 - Umbrales de NLP
 
 ## Migraciones y Seeds
 
 - **Alembic**: Gestiona migraciones de la base de datos.
 - **Seeds**: Inicializa plataformas y criterios en la BD.
 
 ## Instalación y Ejecución
 
 1. Clona el repositorio y accede al directorio `backend`.
 2. Configura el archivo `.env` con tus credenciales.
 3. Instala Docker y Docker Compose.
 4. Ejecuta:
      ```bash
      docker-compose build
      docker-compose up -d
      ```
 5. Accede a la API en `http://localhost:8000` y a pgAdmin en `http://localhost:5050`.
 
 ## Créditos y Licencia
 
 Desarrollado por el Semillero Jojma - Pymes Hoteleras, Universidad Libre. Uso académico y de investigación.

## 🏗️ Arquitectura

```
app/
├── core/           # Configuración, seguridad, logging, excepciones
├── db/             # Configuración de base de datos
├── models/         # Modelos SQLAlchemy (Hotel, Reseña, Sentimiento, etc.)
├── schemas/        # Schemas Pydantic para validación
├── crud/           # Operaciones CRUD
├── services/       # Lógica de negocio (scraping, NLP, indicadores, export)
├── routers/        # Endpoints FastAPI
├── scraping/       # Scripts de scraping y datos JSON
├── nlp/            # Módulos de procesamiento de lenguaje natural
├── workers/        # Workers de Celery
├── seeds/          # Datos iniciales
└── utils/          # Utilidades
```

## 🛠️ Tecnologías

- **Framework**: FastAPI 0.115.0
- **Base de Datos**: PostgreSQL 16 + SQLAlchemy 2.0.36
- **ORM**: Alembic 1.14.0 (migraciones)
- **Task Queue**: Celery 5.4.0 + Redis 5.2.0
- **Scraping**: Selenium 4.27.1 + BeautifulSoup4 4.12.3
- **NLP**: spaCy 3.8.3, NLTK 3.9.1, TextBlob 0.18.0, scikit-learn 1.6.0
- **Exportación**: ReportLab 4.2.5, openpyxl 3.1.5
- **Seguridad**: passlib[bcrypt], python-jose

## 🚀 Instalación

### 1. Clonar repositorio

```bash
git clone <repo-url>
cd backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/scrapingweb_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=tu-clave-secreta
```

### 5. Crear base de datos

```bash
# PostgreSQL
createdb scrapingweb_db

# Ejecutar migraciones
alembic upgrade head
```

### 6. Poblar datos iniciales

```bash
python -m app.seeds.initial_data
```

### 7. Ejecutar aplicación

```bash
uvicorn main:app --reload
```

Visita: http://localhost:8000/docs

## 📊 API Endpoints

### Hoteles
- `GET /api/v1/hoteles` - Listar hoteles
- `GET /api/v1/hoteles/{id}` - Obtener hotel
- `POST /api/v1/hoteles` - Crear hotel
- `PUT /api/v1/hoteles/{id}` - Actualizar hotel

### Indicadores (Análisis Cuantitativo)
- `GET /api/v1/indicadores/resumen` - Resumen global (cards)
- `GET /api/v1/indicadores/tabla-hoteles` - Tabla de hoteles
- `GET /api/v1/indicadores/distribucion-plataformas` - Gráfico distribución
- `GET /api/v1/indicadores/distribucion-sentimientos` - Gráfico sentimientos
- `GET /api/v1/indicadores/comparacion-hoteles` - Gráfico comparativo

### Reseñas (Análisis Cualitativo)
- `GET /api/v1/resenas/{hotel_id}` - Listar reseñas con filtros
- `GET /api/v1/resenas/destacadas/{hotel_id}` - Reseñas destacadas

### Scraping
- `POST /api/v1/scraping/ejecutar` - Simular scraping (frontend)
- `POST /api/v1/scraping/ejecutar-ahora` - Ejecutar scraping real (admin)

### Exportación
- `POST /api/v1/export/pdf` - Generar reporte PDF
- `POST /api/v1/export/csv` - Generar reporte CSV

## 🔄 Scraping Diario Automático

El backend ejecuta scraping **UNA VEZ AL DÍA** mediante Celery:

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
celery -A app.workers.queue worker --loglevel=info

# Terminal 3: Celery Beat (scheduler)
celery -A app.workers.queue beat --loglevel=info
```

## 🧪 Testing

```bash
pytest
```

## 📦 Docker

```bash
docker-compose up -d
```

## 📝 Flujo de Trabajo Frontend-Backend

1. **Panel de Control**: Frontend muestra animación de carga al "Iniciar Extracción", pero NO ejecuta scraping (se ejecuta automáticamente diario)

2. **Filtros de Análisis**: 
   - Fecha Desde/Hasta
   - Sostenibilidad Mín.
   - Calidad Mín.

3. **Análisis Cuantitativo**: 
   - Cards con totales
   - Tabla de hoteles
   - `/api/v1/indicadores/resumen`
   - `/api/v1/indicadores/tabla-hoteles`

4. **Visualización Comparativa**:
   - Gráficos de distribución
   - `/api/v1/indicadores/distribucion-plataformas`
   - `/api/v1/indicadores/comparacion-hoteles`

5. **Análisis Cualitativo**:
   - Reseñas positivas/negativas/recientes
   - `/api/v1/resenas/{hotel_id}`
   - `/api/v1/resenas/destacadas/{hotel_id}`

## 👥 Autores

Semillero Jojma - Pymes Hoteleras
Universidad Libre - Ingeniería de Sistemas

## 📄 Licencia

MIT
