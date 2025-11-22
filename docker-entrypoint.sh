#!/bin/bash
set -e

echo "🚀 Iniciando ScrapingWeb Backend..."

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando PostgreSQL..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB > /dev/null 2>&1; do
  sleep 1
done
echo "✅ PostgreSQL listo"

# Esperar a que Redis esté listo
echo "⏳ Esperando Redis..."
while ! redis-cli -h redis ping > /dev/null 2>&1; do
  sleep 1
done
echo "✅ Redis listo"

# Ejecutar migraciones
echo "📦 Ejecutando migraciones Alembic..."
alembic upgrade head

# Poblar datos iniciales (solo si no existen)
echo "🌱 Poblando datos iniciales..."
python -m app.seeds.initial_data || true

# Ejecutar comando
echo "✅ Iniciando aplicación..."
exec "$@"
