#!/bin/bash
set -e

echo "=== Starting NeoCare Backend ==="
echo "DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "PORT: ${PORT:-8000}"

# Verificar que DATABASE_URL existe
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set"
    exit 1
fi

# Iniciar aplicación directamente sin migraciones
echo "Starting Uvicorn..."
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
