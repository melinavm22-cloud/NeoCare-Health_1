
MINI_DEMO - Criterios de aceptación (QA)

## Introducción (10–15 segundos).
Guión: Voy a mostrar las funcionalidades desarrolladas esta semana: registro de horas, listado por tarjeta, edición segura, validaciones y la vista ‘Mis horas’ con totales semanales.


## CRITERIO_1 -  Añadir horas desde el detalle de una tarjeta 
- Abrir una tarjeta.
- Mostrar el formulario de añadir horas.
- Introducir:
· Fecha
· Horas (ej. 2.5)
· Nota
- Guardar.

### Guión: Añado horas directamente desde el detalle de la tarjeta, como pide el criterio 1


## CRITERIO_2 - Ver listado cronológico de horas por tarjeta
- Mostrar la sección “Horas registradas” dentro de la tarjeta.
- Señalar que están ordenadas por fecha.

### Guión: Aquí se ve el listado cronológico de horas asociadas a esta tarjeta


## CRITERIO_3 - Editar y eliminar solo mis horas
- Seleccionar un worklog creado por ti.
- Editarlo (cambiar horas o nota).
- Eliminarlo.
- Mostrar un worklog de otro usuario (si existe) y demostrar que no aparece el botón de editar/eliminar.

### Guión: El sistema solo me permite editar o eliminar mis propios registros. Los de otros usuarios no son modificables.


## CRITERIO_4 - Validaciones funcionando - Mostrar dos casos rápidos:
❌ Caso inválido 1: horas ≤ 0
- Introducir 0 o -1
- Mostrar mensaje de error

❌ Caso inválido 2: nota > 200 caracteres
- Pegar un texto largo
- Mostrar error

### Guión: Las validaciones se aplican tanto en frontend como en backend.


## CRITERIO_5 - Vista “Mis horas” filtrada por semana
- Ir a la vista “Mis horas”.
- Mostrar selector de semana.
- Cambiar de semana y ver cómo cambia la lista.

### Guión: Aquí veo mis horas filtradas por semana, con totales diarios y semanal.


## CRITERIO_6 - Totales semanales correctos
- Mostrar el total semanal.
- Compararlo visualmente con la suma de los registros visibles.

### Guión: El total semanal coincide con la suma de los registros de la semana


## CRITERIO_7 - Seguridad: accesos no autorizados - Demostración de 2 formas opcional:
- Opción A (Frontend).
Mostrar que no puedes editar worklogs ajenos.

- Opción B (Postman).
Intentar editar un worklog que no es tuyo.
Mostrar respuesta 403 o 401.

### Guión: El sistema impide accesos o ediciones no autorizadas, cumpliendo el criterio de seguridad.

