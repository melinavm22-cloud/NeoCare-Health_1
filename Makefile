.PHONY: help install setup-db run run-dev clean env-setup

PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin
BACKEND_DIR := backend

help:
	@echo "NeoCare Backend - Comandos disponibles:"
	@echo ""
	@echo "  make install    - Instalar dependencias Python"
	@echo "  make setup-db   - Crear base de datos"
	@echo "  make env-setup  - Crear archivo .env"
	@echo "  make run-dev    - Iniciar servidor (desarrollo)"
	@echo "  make run        - Iniciar servidor (producción)"
	@echo "  make clean      - Limpiar archivos temporales"
	@echo ""
	@echo "Setup rápido:"
	@echo "  1. make install"
	@echo "  2. make env-setup (editar .env con credenciales)"
	@echo "  3. make setup-db"
	@echo "  4. source venv/bin/activate"
	@echo "  5. make run-dev"

install:
	@echo "Creando entorno virtual..."
	$(PYTHON) -m venv $(VENV)
	@echo "Actualizando pip..."
	$(VENV_BIN)/pip install --upgrade pip setuptools wheel
	@echo "Instalando dependencias..."
	$(VENV_BIN)/pip install -r requirements.txt
	@echo ""
	@echo "Instalación completada!"
	@echo "Activa el entorno: source $(VENV_BIN)/activate"

setup-db:
	@echo "Creando base de datos neocare..."
	createdb neocare || echo "Base de datos ya existe"
	@echo "Base de datos lista"

env-setup:
	@if [ ! -f .env ]; then \
		echo "Creando archivo .env..."; \
		cp env.example .env; \
		echo "Archivo .env creado. Edita las credenciales antes de continuar."; \
	else \
		echo "El archivo .env ya existe."; \
	fi

run:
	@echo "Iniciando servidor..."
	$(VENV_BIN)/uvicorn backend.main:app --host 0.0.0.0 --port 8000

run-dev:
	@echo "Iniciando servidor en modo desarrollo..."
	$(VENV_BIN)/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Limpieza completada"
