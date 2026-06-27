INFORME PROYECTO: SISTEMA DE AGENDAMIENTO PARA SALÓN DE UÑAS "RR NAILS"

1 Contexto del Proyecto
El presente proyecto consiste en el desarrollo de un sistema de agendamiento de citas para un salón de uñas denominado "RR Nails". Este sistema surge de la necesidad de optimizar la gestión de citas, recursos y personal en un entorno de servicios de belleza que ha experimentado un crecimiento significativo en su demanda.

El salón de uñas "RR Nails" ofrece una variedad de servicios que incluyen manicuras, pedicuras, y tratamientos especializados con diferentes técnicas como semipermanente, buildergel, polygel, softgel y spa. Cada uno de estos servicios requiere una combinación específica de recursos, tanto consumibles como herramientas, y personal calificado (manicuristas) para su ejecución.


 Objetivos del Sistema:


Automatizar el proceso de agendamiento de citas verificando disponibilidad de horario, manicuristas y recursos

Clasificar y gestionar recursos en gastables y no gastables para un control más preciso

Mantener un historial de clientes para fidelización y seguimiento

Proporcionar una interfaz amigable para administradores y clientes

Generar reportes y visualizaciones del estado del inventario y agenda


 Estructura del Negocio:
El salón de uñas "RR Nails" 
Horario de Atención: De 9:00 AM a 5:00 PM, de lunes a sábado

Personal: Cuatro manicuristas profesionales (Ana, Beatriz, Carla, Diana), cada una con habilidades completas para realizar todos los servicios ofrecidos.

Capacidad de Atención: Dado que cada manicurista atiende un cliente a la vez, la capacidad máxima es de 4 clientes simultáneos.

Servicios Ofrecidos:

Manicura regular (30 min): Servicio básico de embellecimiento de uñas

Manicura semipermanente (45 min): Esmaltado de larga duración

Manicura buildergel (90 min): Construcción de uñas con gel

Manicura polygel (120 min): Extensión con polygel

Manicura softgel (100 min): Técnica con uñas encapsuladas

Pedicura regular (45 min): Cuidado de pies básico

Pedicura semipermanente (60 min): Esmaltado duradero en pies

Pedicura con extensión polygel (120 min): Extensión en pies

Pedicura spa (120 min): Tratamiento completo de relajación

 Recursos del Sistema
Recursos Gastables (Consumibles)
Son aquellos materiales que se agotan con cada servicio y deben ser reabastecidos periódicamente. Su gestión incluye control de inventario y alertas de stock bajo. Ejemplos:

Esmaltes (regular y semipermanente): Se consumen aproximadamente 1ml por servicio

Geles (builder, polygel): Utilizados en extensiones y construcciones

Base coat y Top coat: Capas protectoras esenciales

Primer: Preparador de la uña

Aceite de cutículas: Para hidratación

Crema para pies: En servicios de pedicura

Pegamento para tips: Para extensiones

Algodón y acetona: Para limpieza y remoción

Brillo liso: Acabado final

Alcohol: Para desinfección

 Recursos No Gastables (Herramientas)
Son equipos y herramientas que no se consumen pero tienen una capacidad limitada que debe ser considerada al agendar citas simultáneas. Ejemplos:

Herramientas de metal: Alicates, repujadores, cortaúñas, limas

Herramientas de aplicación: Linners, buffers, pinceles

Tips: Moldes para manos y pies (son reutilizables)

Equipos eléctricos: Lámparas UV/LED (limitadas a 2 unidades)

Muebles y estructuras: Mesas de trabajo (2), sofás de pedicura (1), palangana de hidromasaje (1)

2.3 Flujo de Trabajo
El proceso de agendamiento sigue el siguiente flujo:

Selección del Servicio: El cliente elige uno de los 9 servicios disponibles

Verificación de Disponibilidad: El sistema verifica:

Disponibilidad de horario en la fecha solicitada

Disponibilidad de recursos necesarios

Disponibilidad de manicuristas

Registro de Cliente: Si es cliente nuevo, se registra en el sistema

Asignación de Manicurista: Se asigna aleatoriamente una manicurista disponible

Consumo de Recursos: Se descuenta del inventario los recursos gastables

Confirmación: Se guarda la cita en la agenda

 inicio sesion del Sistema
Administrador:

Acceso con contraseña ("rrnails")

Visualización de la agenda completa

Gestión de recursos (agregar/actualizar)

Gestión de servicios (agregar nuevos servicios)

Visualización del inventario

Cliente:

Agendar citas

Eliminar citas existentes

Ver detalles de sus citas

Consultar servicios disponibles

 estructira DEL SISTEMA
 Estructura General
El sistema está desarrollado en Python y utiliza archivos JSON como base de datos, siguiendo una arquitectura modular con las siguientes capas:

Capa de Datos:

recursos.json: Almacena servicios, recursos y manicuristas

agenda.json: Almacena citas programadas e historial de clientes

 Lógica de Negocio:

Módulo core.py: Contiene todas las funciones de negocio

Validaciones de disponibilidad y consistencia

Presentación:

Módulo mainrr_corregido.py: Interfaz por consola

 Estructura de Datos
 Estructura de Servicios

Servicios = [
    ["nombre_servicio", duracion_minutos, ["recurso1", "recurso2"]],
    ...
]
3.2.2 Estructura de Recursos
python
RecursosGastables = [
    ["nombre", cantidad],
    ...
]

RecursosNoGastables = [
    ["nombre", cantidad],
    ...
]
 Estructura de Agenda

Agenda = [
    [
        [2026, mes, dia],
        [
            [
                [[hora_inicio, min_inicio], [hora_fin, min_fin]],
                "nombre_cliente",
                indice_servicio,
                duracion,
                "manicurista"
            ],
            ...
        ]
    ],
    ...
]
 Estructura de Clientes
python
Clientes = [
    ["nombre", cantidad_citas],
    ...
]
 Algoritmos Principales
 Verificación de Disponibilidad
El algoritmo de verificación de disponibilidad es uno de los componentes más críticos del sistema:

Verificación de Manicuristas:

Recorre todas las citas del día

Cuenta cuántas manicuristas están ocupadas en el horario solicitado

Si todas están ocupadas, retorna no disponible

Verificación de Recursos:

Para recursos gastables: Verifica que haya stock disponible

Para recursos no gastables: Verifica que no estén siendo utilizados en otra cita simultánea

Se clona el estado actual de recursos no gastables

Se restan los recursos usados por citas en el mismo horario

Se verifica que todos los recursos necesarios estén disponibles

Búsqueda del Siguiente Hueco
Cuando el horario solicitado no está disponible, el sistema busca automáticamente el siguiente espacio disponible:

Verifica si el horario está dentro del rango laboral (9:00-17:00)

Si no está disponible, busca:

Antes de la primera cita

Entre citas existentes

Después de la última cita

Si no encuentra espacio en el día, pasa al siguiente día hábil

 Gestión de Inventario
El sistema implementa un control de inventario inteligente:

Consumo automático: Al agendar una cita, se consumen automáticamente los recursos gastables

Alertas de stock bajo: Muestra advertencias cuando el stock es bajo (≤ 3 unidades)

Alertas de sin stock: Impide agendar si no hay stock disponible

FUNCIONALIDADES IMPLEMENTADAS
4.1 Módulo de Administración
Visualización de Agenda:

Muestra todas las citas agendadas ordenadas por fecha y hora

Incluye cliente, servicio, horario y manicurista asignada

Permite tener una visión general de la ocupación del salón

Gestión de Inventario:

Visualización completa del inventario con colores según estado:

Verde: Stock normal (>3 unidades)

 Amarillo: Stock bajo (≤3 unidades)

Rojo: Sin stock (0 unidades)

Separación clara entre recursos gastables y no gastables

Posibilidad de agregar nuevos recursos especificando su tipo

Gestión de Servicios:

Agregar nuevos servicios con su duración y recursos necesarios

Selección de recursos desde el inventario existente

Validación para evitar duplicados

 Módulo de Cliente
Agendamiento de Citas:

Selección de servicio de la lista disponible

Ingreso de fecha y hora deseada

Validación automática de disponibilidad

Propuesta de horarios alternativos si el solicitado no está disponible

Registro de nuevos clientes con historial

Confirmación final antes de guardar

Eliminación de Citas:

Búsqueda por nombre del cliente

Visualización de todas las citas del cliente en una fecha

Confirmación antes de eliminar

Actualización automática del contador de citas del cliente

Liberación de recursos al eliminar

Consulta de Detalles:

Ver detalles completos de una cita específica

Información de cliente, servicio, horario y manicurista

Funcionalidades de Apoyo
Verificación de Nombre de Cliente:

Detecta si el cliente ya existe en el sistema

Pregunta si ha tenido otros servicios anteriores

Incrementa contador de fidelidad para clientes recurrentes

Guardado Automático:

Guarda los datos automáticamente después de cada operación

Previene pérdida de información

Persistencia en archivos JSON

 INTERFAZ DE USUARIO
5.1 Menú Principal
El sistema presenta un menú principal con tres opciones:

Inicio de sesión Administración: Acceso restringido por contraseña para gestión del sistema

Inicio de sesión Cliente: Acceso para agendar, eliminar y consultar citas

Salir: Guarda los datos y cierra el sistema

 Menú de Administración
Mostrar agenda completa
Mostrar inventario
Agregar recurso
Agregar servicio
Ver recursos por servicio
Guardar y salir
Menú de Cliente
Agendar cita
Eliminar cita
Ver detalles de cita
Ver servicios disponibles
Guardar y salir
 Colores y Feedback Visual
El sistema utiliza códigos ANSI para proporcionar retroalimentación visual:

 Verde: Confirmación de acciones exitosas

 Rojo: Mensajes de error o advertencia

 Azul: Solicitudes de confirmación

 Amarillo: Mensajes informativos

