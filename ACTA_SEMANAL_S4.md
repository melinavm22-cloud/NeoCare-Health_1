# Acta Semanal 4 – Proyecto NeoCare

**Rol asignado:** Documentadora  

## Logros de la semana
- Se actualizó el backend/README.md incorporando:
La nueva tabla worklogs con su estructura completa.
Todos los endpoints relacionados con worklogs (crear, listar, editar, eliminar y consulta semanal).
Validaciones aplicadas tanto en backend como en frontend.
Ejemplos de payloads y respuestas reales del sistema.

- Se definió y documentó la estructura final de la vista “Mis horas”, incluyendo:
Flujo funcional
Campos visibles
Casos límite
Validaciones
Ejemplo de respuesta semanal

- Se verificó la coherencia entre endpoints, modelos y documentación previa.


## Bloqueos o riesgos
- Algunos fragmentos del README original estaban dañados o incrustados dentro de comentarios, lo que requirió reconstrucción manual.
- Dependencia de información no centralizada (endpoints, modelos, decisiones previas), lo que puede generar retrasos si no se mantiene actualizado.


## Decisiones técnicas
- Se adoptó el formato ISO YYYY‑WW para la consulta semanal, garantizando coherencia con FastAPI, Python y la lógica del backend.
- Se estandarizó el estilo de documentación:
Títulos consistentes.
Bloques de código para endpoints.
Tablas para modelos.
Payloads reales.

- Se definió una estructura fija para futuras vistas o módulos:
Descripción.
Flujo.
Validaciones.
Casos límite.
Ejemplos.


##  Observaciones y próximos pasos
- Sería recomendable crear una carpeta /docs para centralizar toda la documentación técnica del proyecto.
- La documentación generada esta semana deja una base sólida para continuar con módulos futuros sin inconsistencias.
- Mantener una rutina semanal de actualización de documentación evitará acumulación de deuda técnica.
- Se sugiere documentar también:
Permisos por rol
Estructura de boards y lists
Flujo de autenticación

