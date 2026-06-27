import random
import copy
import json

# Cargar archivos JSON
with open('recursos.json', 'r', encoding='utf-8') as doc1:
    recursos = json.load(doc1)

with open('agenda.json', 'r', encoding='utf-8') as doc2:
    agenda = json.load(doc2)

# Definir meses
Meses = [['enero', 31], ['febrero', 28], ['marzo', 31], ['abril', 30], 
         ['mayo', 31], ['junio', 30], ['julio', 31], ['agosto', 31], 
         ['septiembre', 30], ['octubre', 31], ['noviembre', 30], ['diciembre', 31]]

# Asignar variables globales
Agenda = agenda['Agenda']
Clientes = agenda['Clientes']
Servicios = recursos['Servicios']
RecursosGastables = recursos['RecursosGastables']
RecursosNoGastables = recursos['RecursosNoGastables']
Manicuristas = recursos['Manicuristas']

# Para mantener compatibilidad con código existente
Recursos = RecursosGastables + RecursosNoGastables

def formatear_hora(hora):
    """Formatea una hora [h, min] a string HH:MM"""
    return f"{hora[0]:02d}:{hora[1]:02d}"

def minutos_a_horas(minutos):
    """Convierte minutos a formato [horas, minutos]"""
    return [minutos // 60, minutos % 60]

def horas_a_minutos(hora):
    """Convierte [horas, minutos] a minutos totales"""
    return hora[0] * 60 + hora[1]

def solapan_horarios(inicio1, fin1, inicio2, fin2):
    """Verifica si dos intervalos de tiempo se solapan"""
    return horas_a_minutos(inicio1) < horas_a_minutos(fin2) and horas_a_minutos(inicio2) < horas_a_minutos(fin1)

def asignar_manicurista(mes, dia, inicio, fin):
    """Asigna un manicurista disponible para un horario específico"""
    manicuristas_ocupados = []
    
    # Buscar manicuristas ocupados en ese horario
    for cita_agendada in Agenda:
        if cita_agendada[0] == [2026, mes, dia]:
            for cita in cita_agendada[1]:
                cita_inicio = cita[0][0]
                cita_fin = cita[0][1]
                if solapan_horarios(inicio, fin, cita_inicio, cita_fin):
                    manicuristas_ocupados.append(cita[4])
    
    # Determinar manicuristas disponibles
    manicuristas_disponibles = [m for m in Manicuristas if m not in manicuristas_ocupados]
    
    if not manicuristas_disponibles:
        return None
    
    return random.choice(manicuristas_disponibles)

def es_recurso_gastable(nombre_recurso):
    """Determina si un recurso es gastable"""
    for recurso in RecursosGastables:
        if recurso[0] == nombre_recurso:
            return True
    return False

def obtener_recurso(nombre_recurso, lista_recursos):
    """Obtiene un recurso de una lista por su nombre"""
    for i, (nombre, cantidad) in enumerate(lista_recursos):
        if nombre == nombre_recurso:
            return i, nombre, cantidad
    return None, None, None

def comprobar_recursos_disponibles(fecha, inicio, fin, servicio_idx):
    """Verifica si hay recursos disponibles para un servicio en un horario específico"""
    dia = fecha[2]
    mes = fecha[1]
    
    # Obtener recursos necesarios para el servicio
    recursos_necesarios = Servicios[servicio_idx][2]
    
    # Recursos que estarán ocupados por otras citas en ese horario (solo no gastables)
    # Y recursos gastables disponibles
    recursos_no_gastables_ocupados = copy.deepcopy(RecursosNoGastables)
    recursos_gastables_disponibles = copy.deepcopy(RecursosGastables)
    
    # Restar recursos no gastables de citas que se solapan
    for cita_agendada in Agenda:
        if cita_agendada[0] == [2026, mes, dia]:
            for cita in cita_agendada[1]:
                cita_inicio = cita[0][0]
                cita_fin = cita[0][1]
                if solapan_horarios(inicio, fin, cita_inicio, cita_fin):
                    servicio_cita = cita[2]
                    for recurso in Servicios[servicio_cita][2]:
                        if not es_recurso_gastable(recurso):
                            # Es no gastable, verificar disponibilidad
                            for i, (r_nombre, r_cantidad) in enumerate(recursos_no_gastables_ocupados):
                                if r_nombre == recurso:
                                    recursos_no_gastables_ocupados[i][1] -= 1
    
    # Verificar si hay suficientes recursos disponibles
    recursos_faltantes = []
    
    for recurso in recursos_necesarios:
        if es_recurso_gastable(recurso):
            # Verificar en recursos gastables (cantidad total disponible)
            idx, nombre, cantidad = obtener_recurso(recurso, recursos_gastables_disponibles)
            if idx is not None:
                if cantidad <= 0:
                    recursos_faltantes.append(f"{recurso} (gastable, sin stock)")
                # No restamos aquí porque la verificación es de disponibilidad, no consumo
            else:
                recursos_faltantes.append(f"{recurso} (gastable, no encontrado)")
        else:
            # Verificar en recursos no gastables (disponibilidad en ese horario)
            idx, nombre, cantidad = obtener_recurso(recurso, recursos_no_gastables_ocupados)
            if idx is not None:
                if cantidad <= 0:
                    recursos_faltantes.append(f"{recurso} (no gastable, ocupado en ese horario)")
            else:
                recursos_faltantes.append(f"{recurso} (no gastable, no encontrado)")
    
    return len(recursos_faltantes) == 0, recursos_faltantes

def consumir_recursos_gastables(servicio_idx):
    """Consume los recursos gastables de un servicio"""
    recursos_necesarios = Servicios[servicio_idx][2]
    recursos_consumidos = []
    
    for recurso in recursos_necesarios:
        if es_recurso_gastable(recurso):
            # Buscar en RecursosGastables y consumir
            for i, (nombre, cantidad) in enumerate(RecursosGastables):
                if nombre == recurso:
                    if cantidad > 0:
                        RecursosGastables[i][1] -= 1
                        recursos_consumidos.append(recurso)
                    else:
                        print(f"⚠️ Advertencia: No hay stock de '{recurso}'")
                    break
    
    return recursos_consumidos

def comprobar_disponibilidad(mes, dia, inicio, fin, servicio_idx):
    """Verifica si hay disponibilidad completa (manicuristas y recursos)"""
    # Verificar disponibilidad de manicuristas
    manicuristas_ocupados = 0
    for cita_agendada in Agenda:
        if cita_agendada[0] == [2026, mes, dia]:
            for cita in cita_agendada[1]:
                cita_inicio = cita[0][0]
                cita_fin = cita[0][1]
                if solapan_horarios(inicio, fin, cita_inicio, cita_fin):
                    manicuristas_ocupados += 1
    
    if manicuristas_ocupados >= len(Manicuristas):
        return False, "No hay manicuristas disponibles"
    
    # Verificar disponibilidad de recursos
    disponibles, recursos_faltantes = comprobar_recursos_disponibles([2026, mes, dia], inicio, fin, servicio_idx)
    if not disponibles:
        return False, f"Faltan recursos: {', '.join(recursos_faltantes)}"
    
    return True, "Disponible"

def comprobar_nombre_cliente():
    """Verifica y registra el nombre del cliente"""
    print("Escriba el nombre con el que desea agendar la cita:")
    
    nombre = input().lower().strip()
    
    # Buscar si el cliente ya existe
    for i, (cliente, citas) in enumerate(Clientes):
        if cliente == nombre:
            print(f"Bienvenido/a nuevamente {nombre}. ¿Ha tenido otro servicio con nosotros? (SI/NO)")
           
            respuesta = input().lower().strip()
            
            if respuesta == "si":
                Clientes[i][1] += 1
               
                print("\033[32m¡Gracias por preferirnos nuevamente!\033[0m")
            elif respuesta == "no":
                print("Por favor regístrese con otro nombre")
                
                return comprobar_nombre_cliente()
            else:
                
                print("\033[31mOpción no válida\033[0m")
                return comprobar_nombre_cliente()
            return nombre
    
    # Cliente nuevo
    Clientes.append([nombre, 1])
    
    print(f"\033[32m¡Bienvenido/a {nombre}!\033[0m")
    return nombre

def ingresar_fecha(para_agendar=True):
    """Función genérica para ingresar fecha"""
    print("Escriba el mes (ejemplo: enero):")
    
    mes_str = input().lower().strip()
    
    # Buscar mes
    mes_num = 0
    for i, (mes_nombre, _) in enumerate(Meses):
        if mes_str == mes_nombre:
            mes_num = i + 1
            break
    
    if mes_num == 0:
        
        print("\033[31mMes no válido\033[0m")
        return None
    
    print("Escriba el día:")
    
    try:
        dia = int(input())
    except ValueError:
        
        print("\033[31mDía no válido\033[0m")
        return None
    
    if dia < 1 or dia > Meses[mes_num-1][1]:
       
        print("\033[31mDía no válido para el mes seleccionado\033[0m")
        return None
    
    if para_agendar:
        return [2026, mes_num, dia]
    else:
        return [2026, mes_num, dia]

def ingresar_hora():
    """Función para ingresar hora"""
    print("Escriba la hora (formato HH:MM, ejemplo 14:30):")
    
    hora_str = input().strip()
    
    try:
        if ":" not in hora_str:
            raise ValueError
        hora = int(hora_str.split(":")[0])
        minutos = int(hora_str.split(":")[1])
        
        if hora < 0 or hora > 23 or minutos < 0 or minutos > 59:
            raise ValueError
        
        return [hora, minutos]
    except:
       
        print("\033[31mFormato de hora no válido\033[0m")
        return None

def buscar_siguiente_hueco(mes, dia, inicio_deseado, duracion_minutos, servicio_idx):
    """Busca el siguiente hueco disponible"""
    fin_deseado = minutos_a_horas(horas_a_minutos(inicio_deseado) + duracion_minutos)
    
    # Verificar si está dentro del horario laboral
    if inicio_deseado[0] < 9 or fin_deseado[0] >= 17:
        # Pasar al siguiente día a las 9:00
        if dia < Meses[mes-1][1]:
            return buscar_siguiente_hueco(mes, dia + 1, [9, 0], duracion_minutos, servicio_idx)
        elif mes < 12:
            return buscar_siguiente_hueco(mes + 1, 1, [9, 0], duracion_minutos, servicio_idx)
        else:
            return None, "Lo sentimos, no hay disponibilidad en 2026"
    
    # Buscar citas en ese día
    citas_dia = []
    for cita_agendada in Agenda:
        if cita_agendada[0] == [2026, mes, dia]:
            citas_dia = cita_agendada[1]
            break
    
    if not citas_dia:
        # No hay citas en ese día
        disponible, motivo = comprobar_disponibilidad(mes, dia, inicio_deseado, fin_deseado, servicio_idx)
        if disponible:
            return (mes, dia, inicio_deseado), "Disponible"
        else:
            # Si no hay disponibilidad, buscar al día siguiente
            if dia < Meses[mes-1][1]:
                return buscar_siguiente_hueco(mes, dia + 1, [9, 0], duracion_minutos, servicio_idx)
            elif mes < 12:
                return buscar_siguiente_hueco(mes + 1, 1, [9, 0], duracion_minutos, servicio_idx)
            else:
                return None, "Lo sentimos, no hay disponibilidad en 2026"
    
    # Ordenar citas por hora de inicio
    citas_dia.sort(key=lambda x: horas_a_minutos(x[0][0]))
    
    # Verificar espacio antes de la primera cita
    primera_cita_inicio = citas_dia[0][0][0]
    if horas_a_minutos(inicio_deseado) + duracion_minutos <= horas_a_minutos(primera_cita_inicio):
        disponible, motivo = comprobar_disponibilidad(mes, dia, inicio_deseado, fin_deseado, servicio_idx)
        if disponible:
            return (mes, dia, inicio_deseado), "Disponible"
    
    # Verificar espacios entre citas
    for i in range(len(citas_dia) - 1):
        fin_cita_actual = citas_dia[i][0][1]
        inicio_siguiente_cita = citas_dia[i+1][0][0]
        
        if horas_a_minutos(fin_cita_actual) + duracion_minutos <= horas_a_minutos(inicio_siguiente_cita):
            nuevo_inicio = fin_cita_actual
            nuevo_fin = minutos_a_horas(horas_a_minutos(nuevo_inicio) + duracion_minutos)
            disponible, motivo = comprobar_disponibilidad(mes, dia, nuevo_inicio, nuevo_fin, servicio_idx)
            if disponible:
                return (mes, dia, nuevo_inicio), "Disponible"
    
    # Verificar espacio después de la última cita
    ultima_cita_fin = citas_dia[-1][0][1]
    if horas_a_minutos(ultima_cita_fin) + duracion_minutos <= 17 * 60:  # Hasta las 17:00
        nuevo_inicio = ultima_cita_fin
        nuevo_fin = minutos_a_horas(horas_a_minutos(nuevo_inicio) + duracion_minutos)
        disponible, motivo = comprobar_disponibilidad(mes, dia, nuevo_inicio, nuevo_fin, servicio_idx)
        if disponible:
            return (mes, dia, nuevo_inicio), "Disponible"
    
    # Si no hay espacio, buscar al día siguiente
    if dia < Meses[mes-1][1]:
        return buscar_siguiente_hueco(mes, dia + 1, [9, 0], duracion_minutos, servicio_idx)
    elif mes < 12:
        return buscar_siguiente_hueco(mes + 1, 1, [9, 0], duracion_minutos, servicio_idx)
    else:
        return None, "Lo sentimos, no hay disponibilidad en 2026"

def agendar_cita(servicio_idx):
    """Función principal para agendar una cita"""
    print(f"\n--- AGENDAR {Servicios[servicio_idx][0].upper()} ---")
    
    # Ingresar fecha deseada
    fecha = ingresar_fecha(para_agendar=True)
    if not fecha:
        return
    
    # Ingresar hora deseada
    inicio = ingresar_hora()
    if not inicio:
        return
    
    mes, dia = fecha[1], fecha[2]
    duracion = Servicios[servicio_idx][1]  # Duración en minutos
    fin = minutos_a_horas(horas_a_minutos(inicio) + duracion)
    
    # Verificar horario laboral
    if inicio[0] < 9 or fin[0] >= 17 or (fin[0] == 17 and fin[1] > 0):
        
        print("\033[31mHorario fuera del horario de atención (9:00 - 17:00)\033[0m")
        
        # Buscar siguiente hueco
        resultado, mensaje = buscar_siguiente_hueco(mes, dia, inicio, duracion, servicio_idx)
        if resultado:
            mes_nuevo, dia_nuevo, inicio_nuevo = resultado
            fin_nuevo = minutos_a_horas(horas_a_minutos(inicio_nuevo) + duracion)
            
            print(f"Próximo espacio disponible: {dia_nuevo} de {Meses[mes_nuevo-1][0]} a las {formatear_hora(inicio_nuevo)}")
            
            print(f"\033[34m¿Desea agendar en ese horario? (SI/NO)\033[0m")
            
            if input().lower().strip() == "si":
                nombre = comprobar_nombre_cliente()
                manicurista = asignar_manicurista(mes_nuevo, dia_nuevo, inicio_nuevo, fin_nuevo)
                
                if not manicurista:
                    print("Error: No hay manicuristas disponibles")
                    return
                
                # Consumir recursos gastables
                consumir_recursos_gastables(servicio_idx)
                
                # Crear la cita
                nueva_cita = [
                    [inicio_nuevo, fin_nuevo],
                    nombre,
                    servicio_idx,
                    duracion,
                    manicurista
                ]
                
                # Buscar si ya existe agenda para esa fecha
                fecha_completa = [2026, mes_nuevo, dia_nuevo]
                encontrado = False
                for i, cita_agendada in enumerate(Agenda):
                    if cita_agendada[0] == fecha_completa:
                        Agenda[i][1].append(nueva_cita)
                        encontrado = True
                        break
                
                if not encontrado:
                    Agenda.append([fecha_completa, [nueva_cita]])
                
                
                print("\033[32m✓ Cita agendada exitosamente\033[0m")
                guardar_datos()  # Guardar después de agendar
            else:
                print("Cita no agendada")
        else:
            print(mensaje)
            print(f"\033[31m{mensaje}\033[0m")
        return
    
    # Verificar disponibilidad en el horario deseado
    disponible, motivo = comprobar_disponibilidad(mes, dia, inicio, fin, servicio_idx)
    
    if disponible:
        # Horario disponible
        nombre = comprobar_nombre_cliente()
        manicurista = asignar_manicurista(mes, dia, inicio, fin)
        
        if not manicurista:
            print("Error: No hay manicuristas disponibles")
            return
        
        # Consumir recursos gastables
        consumir_recursos_gastables(servicio_idx)
        
        # Crear la cita
        nueva_cita = [
            [inicio, fin], nombre,  servicio_idx, duracion, manicurista
        ]
        
        # Buscar si ya existe agenda para esa fecha
        fecha_completa = [2026, mes, dia]
        encontrado = False
        for i, cita_agendada in enumerate(Agenda):
            if cita_agendada[0] == fecha_completa:
                Agenda[i][1].append(nueva_cita)
                encontrado = True
                break
        
        if not encontrado:
            Agenda.append([fecha_completa, [nueva_cita]])
        
        
        print("\033[32m✓ Cita agendada exitosamente\033[0m")
        guardar_datos()  # Guardar después de agendar
        
    else:
        # Horario no disponible, buscar siguiente hueco
        
        print(f"\033[31mNo disponible: {motivo}\033[0m")
        
        resultado, mensaje = buscar_siguiente_hueco(mes, dia, inicio, duracion, servicio_idx)
        if resultado:
            mes_nuevo, dia_nuevo, inicio_nuevo = resultado
            fin_nuevo = minutos_a_horas(horas_a_minutos(inicio_nuevo) + duracion)
            
            print(f"Próximo espacio disponible: {dia_nuevo} de {Meses[mes_nuevo-1][0]} a las {formatear_hora(inicio_nuevo)}")
           
            print(f"\033[34m¿Desea agendar en ese horario? (SI/NO)\033[0m")
            
            if input().lower().strip() == "si":
                nombre = comprobar_nombre_cliente()
                manicurista = asignar_manicurista(mes_nuevo, dia_nuevo, inicio_nuevo, fin_nuevo)
                
                if not manicurista:
                    print("Error: No hay manicuristas disponibles")
                    return
                
                # Consumir recursos gastables
                consumir_recursos_gastables(servicio_idx)
                
                # Crear la cita
                nueva_cita = [
                    [inicio_nuevo, fin_nuevo], nombre, servicio_idx, duracion, manicurista
                ]
                
                # Buscar si ya existe agenda para esa fecha
                fecha_completa = [2026, mes_nuevo, dia_nuevo]
                encontrado = False
                for i, cita_agendada in enumerate(Agenda):
                    if cita_agendada[0] == fecha_completa:
                        Agenda[i][1].append(nueva_cita)
                        encontrado = True
                        break
                
                if not encontrado:
                    Agenda.append([fecha_completa, [nueva_cita]])
                
                
                print("\033[32m✓ Cita agendada exitosamente\033[0m")
                guardar_datos()  # Guardar después de agendar
            else:
                print("Cita no agendada")
        else:
            print(mensaje)
            print(f"\033[31m{mensaje}\033[0m")

def eliminar_cita():
    """Eliminar una cita existente"""
    print("\n--- ELIMINAR CITA ---")
    
    # Solicitar nombre
    print("Escriba el nombre con el que agendó la cita:")
    
    nombre = input().lower().strip()
    
    # Verificar si el cliente existe
    cliente_existe = False
    for cliente, _ in Clientes:
        if cliente == nombre:
            cliente_existe = True
            break
    
    if not cliente_existe:
       
        print("\033[31mNo hay citas agendadas con ese nombre\033[0m")
        return
    
    # Solicitar fecha
    fecha = ingresar_fecha(para_agendar=False)
    if not fecha:
        return
    
    # Buscar citas del cliente en esa fecha
    citas_encontradas = []
    for i, cita_agendada in enumerate(Agenda):
        if cita_agendada[0] == fecha:
            for j, cita in enumerate(cita_agendada[1]):
                if cita[1] == nombre:
                    citas_encontradas.append((i, j, cita))
    
    if not citas_encontradas:
        print("No hay citas para ese cliente en la fecha especificada")
        
        return
    
    # Mostrar citas encontradas
    if len(citas_encontradas) == 1:
        # Solo una cita
        i, j, cita = citas_encontradas[0]
        servicio = Servicios[cita[2]][0]
        inicio = formatear_hora(cita[0][0])
        
        print(f"Cita encontrada: {servicio} - {inicio}")
        print("¿Desea eliminarla? (SI/NO)")
        
        if input().lower().strip() == "si":
            # Eliminar la cita
            Agenda[i][1].pop(j)
            if len(Agenda[i][1]) == 0:
                Agenda.pop(i)
            
            # Actualizar contador del cliente
            for k, (cliente, citas) in enumerate(Clientes):
                if cliente == nombre:
                    Clientes[k][1] -= 1
                    if Clientes[k][1] == 0:
                        Clientes.pop(k)
                    break
            
            
            print("\033[32m✓ Cita eliminada exitosamente\033[0m")
            guardar_datos()  # Guardar después de eliminar
        else:
            print("Operación cancelada")
    
    else:
        # Múltiples citas
        print("Citas encontradas:")
        for idx, (_, _, cita) in enumerate(citas_encontradas, 1):
            servicio = Servicios[cita[2]][0]
            inicio = formatear_hora(cita[0][0])
            print(f"{idx}. {servicio} - {inicio}")
        
       
        print("\033[34mSeleccione la cita a eliminar (número):\033[0m")
        
        try:
            opcion = int(input())
            if 1 <= opcion <= len(citas_encontradas):
                i, j, cita = citas_encontradas[opcion-1]
                
                # Eliminar la cita
                Agenda[i][1].pop(j)
                if len(Agenda[i][1]) == 0:
                    Agenda.pop(i)
                
                # Actualizar contador del cliente
                for k, (cliente, citas) in enumerate(Clientes):
                    if cliente == nombre:
                        Clientes[k][1] -= 1
                        if Clientes[k][1] == 0:
                            Clientes.pop(k)
                        break
                
               
                print("\033[32m✓ Cita eliminada exitosamente\033[0m")
                guardar_datos()  # Guardar después de eliminar
            else:
                print("Opción no válida")
        except ValueError:
            print("Opción no válida")

def ver_detalles_cita():
    """Ver detalles de una cita específica"""
    print("\n--- DETALLES DE CITA ---")
    
    # Solicitar nombre
    print("Escriba el nombre con el que agendó la cita:")
    
    nombre = input().lower().strip()
    
    # Verificar si el cliente existe
    cliente_existe = False
    for cliente, _ in Clientes:
        if cliente == nombre:
            cliente_existe = True
            break
    
    if not cliente_existe:
        
        print("\033[31mNo hay citas agendadas con ese nombre\033[0m")
        return
    
    # Solicitar fecha
    fecha = ingresar_fecha(para_agendar=False)
    if not fecha:
        return
    
    # Buscar citas del cliente en esa fecha
    citas_encontradas = []
    for i, cita_agendada in enumerate(Agenda):
        if cita_agendada[0] == fecha:
            for j, cita in enumerate(cita_agendada[1]):
                if cita[1] == nombre:
                    citas_encontradas.append((i, j, cita))
    
    if not citas_encontradas:
        
        print("\033[31mNo hay citas para ese cliente en la fecha especificada\033[0m")
        return
    
    # Mostrar detalles
    if len(citas_encontradas) == 1:
        # Una sola cita
        _, _, cita = citas_encontradas[0]
        mostrar_detalles_cita(cita, fecha)
    else:
        # Múltiples citas
        print("Citas encontradas:")
        for idx, (_, _, cita) in enumerate(citas_encontradas, 1):
            servicio = Servicios[cita[2]][0]
            inicio = formatear_hora(cita[0][0])
            print(f"{idx}. {servicio} - {inicio}")
        
        print("\033[34mSeleccione la cita para ver detalles (número):\033[0m")
        
        try:
            opcion = int(input())
            if 1 <= opcion <= len(citas_encontradas):
                _, _, cita = citas_encontradas[opcion-1]
                mostrar_detalles_cita(cita, fecha)
            else:
                print("Opción no válida")
        except ValueError:
            print("Opción no válida")

def mostrar_detalles_cita(cita, fecha):
    """Muestra los detalles formateados de una cita"""
    servicio = Servicios[cita[2]][0]
    inicio = formatear_hora(cita[0][0])
    fin = formatear_hora(cita[0][1])
    manicurista = cita[4]
    
    print("\n" + "="*40)
    print("DETALLES DE LA CITA")
    print("="*40)
    print(f"Cliente: {cita[1]}")
    print(f"Fecha: {fecha[2]} de {Meses[fecha[1]-1][0]}")
    print(f"Servicio: {servicio}")
    print(f"Horario: {inicio} - {fin}")
    print(f"Duración: {cita[3]} minutos")
    print(f"Manicurista: {manicurista}")
    print("="*40)

def mostrar_toda_agenda():
    """Muestra todas las citas agendadas"""
    if not Agenda:
        print("\033[31mNo hay citas agendadas\033[0m")
        return
    
    # Ordenar agenda por fecha
    Agenda.sort(key=lambda x: x[0])
    
    print("\n" + "="*60)
    print("TODAS LAS CITAS AGENDADAS")
    print("="*60)
    
    for cita_agendada in Agenda:
        fecha = cita_agendada[0]
        print(f"\n {fecha[2]} DE {Meses[fecha[1]-1][0].upper()} 2026")
        print("-"*40)
        
        # Ordenar citas por hora
        citas = sorted(cita_agendada[1], key=lambda x: horas_a_minutos(x[0][0]))
        
        for cita in citas:
            servicio = Servicios[cita[2]][0]
            inicio = formatear_hora(cita[0][0])
            fin = formatear_hora(cita[0][1])
            print(f"   {cita[1]}")
            print(f"   {servicio}")
            print(f"   {inicio} - {fin}")
            print(f"   Manicurista: {cita[4]}")
            print()

def guardar_datos():
    """Guarda los datos en el archivo JSON"""
    # Ordenar agenda antes de guardar
    if len(Agenda) > 1:
        Agenda.sort(key=lambda x: x[0])
    
    datos_actualizados = {
        "Agenda": Agenda,
        "Clientes": Clientes
    }
    
    with open('agenda.json', 'w', encoding='utf-8') as archivo:
        json.dump(datos_actualizados, archivo, indent=4, ensure_ascii=False)
    
    print("\033[32m✓ Datos guardados exitosamente\033[0m")
    print("\033[33m¡Gracias por usar el sistema!\033[0m")

def guardar_recursos():
    """Guarda los recursos actualizados en el archivo JSON"""
    datos_recursos = {
        "Servicios": Servicios,
        "RecursosGastables": RecursosGastables,
        "RecursosNoGastables": RecursosNoGastables,
        "Manicuristas": Manicuristas
    }
    with open('recursos.json', 'w', encoding='utf-8') as archivo:
        json.dump(datos_recursos, archivo, indent=4, ensure_ascii=False)
    
    print("\033[32mRecursos guardados exitosamente.\033[0m")


def agregar_servicio():
    """Agrega un nuevo servicio con sus recursos necesarios"""
    print("\n--- AGREGAR NUEVO SERVICIO ---")
    
    # Pedir nombre
    print("Ingrese el nombre del servicio:")
    
    nombre = input().strip()
    
    # Verificar si ya existe (case insensitive)
    for servicio in Servicios:
        if servicio[0].lower() == nombre.lower():
            print("\033[31mEse servicio ya existe. No se puede agregar duplicado.\033[0m")
            return
    
    # Pedir duración en minutos
    try:
        print("Ingrese la duración en minutos:")
        
        duracion = int(input())
        if duracion <= 0:
            print("La duración debe ser positiva.")
            return
    except ValueError:
        print("\033[31mDuración no válida.\033[0m")
        return
    
    # Mostrar todos los recursos disponibles (gastables y no gastables)
    print("\n--- RECURSOS DISPONIBLES ---")
    print("\n🔴 RECURSOS GASTABLES:")
    for i, recurso in enumerate(RecursosGastables, 1):
        print(f"  {i}. {recurso[0]} (cantidad: {recurso[1]}) - GASTABLE")
    
    offset_gastables = len(RecursosGastables)
    print("\n🟢 RECURSOS NO GASTABLES:")
    for i, recurso in enumerate(RecursosNoGastables, 1):
        print(f"  {offset_gastables + i}. {recurso[0]} (cantidad: {recurso[1]}) - NO GASTABLE")
    
    recursos_servicio = []
    print("\nIngrese los números de los recursos necesarios (separados por coma).")
    print("Ejemplo: 1,3,5")
    
    seleccion = input().strip()
    
    if seleccion:
        partes = seleccion.split(',')
        for parte in partes:
            try:
                idx = int(parte.strip()) - 1
                # Buscar en recursos gastables primero
                if 0 <= idx < len(RecursosGastables):
                    recurso_nombre = RecursosGastables[idx][0]
                    if recurso_nombre not in recursos_servicio:
                        recursos_servicio.append(recurso_nombre)
                    else:
                        print(f"Recurso '{recurso_nombre}' ya agregado, se omite duplicado.")
                # Buscar en recursos no gastables
                elif 0 <= idx - len(RecursosGastables) < len(RecursosNoGastables):
                    idx_no_gastable = idx - len(RecursosGastables)
                    recurso_nombre = RecursosNoGastables[idx_no_gastable][0]
                    if recurso_nombre not in recursos_servicio:
                        recursos_servicio.append(recurso_nombre)
                    else:
                        print(f"Recurso '{recurso_nombre}' ya agregado, se omite duplicado.")
                else:
                    print(f"Número {idx+1} fuera de rango, se omite.")
            except ValueError:
                print(f"'{parte}' no es válido, se omite.")
    
    if not recursos_servicio:
        print("\033[31mDebe seleccionar al menos un recurso.\033[0m")
        return
    
    # Crear nuevo servicio
    nuevo_servicio = [nombre, duracion, recursos_servicio]
    Servicios.append(nuevo_servicio)
    
    # Guardar cambios
    guardar_recursos()
    
    print(f"\033[32mServicio '{nombre}' agregado exitosamente con duración {duracion} minutos.\033[0m")
    print("Recursos asociados:")
    for r in recursos_servicio:
        # Indicar si es gastable o no
        if es_recurso_gastable(r):
            print(f"  - {r} (GASTABLE)")
        else:
            print(f"  - {r} (NO GASTABLE)")

def agregar_recurso():
    """Agrega un nuevo recurso al inventario"""
    print("\n--- AGREGAR NUEVO RECURSO ---")
    
    # Pedir nombre
    print("Ingrese el nombre del recurso:")
    
    nombre = input().strip().lower()
    
    # Determinar si es gastable o no
    print("¿El recurso es gastable (se consume por servicio)? (SI/NO)")
    es_gastable_input = input().lower().strip()
    es_gastable = es_gastable_input == "si"
    
    # Buscar en la lista correspondiente
    lista_buscar = RecursosGastables if es_gastable else RecursosNoGastables
    
    # Verificar si ya existe
    for recurso in lista_buscar:
        if recurso[0] == nombre:
            print("Ese recurso ya existe. ¿Desea actualizar la cantidad? (SI/NO)")
            
            resp = input().lower().strip()
            if resp == "si":
                print(f"Cantidad actual: {recurso[1]}. Ingrese nueva cantidad:")
                
                try:
                    nueva_cant = int(input())
                    if nueva_cant < 0:
                        print("\033[31mLa cantidad no puede ser negativa.\033[0m")
                        return
                    recurso[1] = nueva_cant
                    guardar_recursos()
                    print("\033[32mRecurso actualizado.\033[0m")
                except ValueError:
                    print("\033[31mCantidad no válida.\033[0m")
            else:
                print("No se realizaron cambios.")
            return
    
    # Si no existe, pedir cantidad
    try:
        print("Ingrese la cantidad del recurso:")
        cantidad = int(input())
        if cantidad < 0:
            print("\033[31mLa cantidad no puede ser negativa.\033[0m")
            return
    except ValueError:
        print("\033[31mCantidad no válida.\033[0m")
        return
    
    # Agregar recurso a la lista correspondiente
    if es_gastable:
        RecursosGastables.append([nombre, cantidad])
        tipo = "gastable"
    else:
        RecursosNoGastables.append([nombre, cantidad])
        tipo = "no gastable"
    
    guardar_recursos()
    print(f"\033[32mRecurso '{nombre}' agregado como {tipo} con cantidad {cantidad}.\033[0m")            

def mostrar_inventario():
    
    print("\n" + "="*60)
    print("INVENTARIO DE RECURSOS")
    print("="*60)
    
    # Mostrar recursos gastables
    print("\n🔴 RECURSOS GASTABLES (se consumen por servicio):")
    print("-"*50)
    if RecursosGastables:
        # Ordenar por nombre
        recursos_ordenados = sorted(RecursosGastables, key=lambda x: x[0])
        for recurso, cantidad in recursos_ordenados:
            # Color rojo si está bajo de stock (menos de 3)
            if cantidad <= 0:
                print(f"  ❌ {recurso}: {cantidad} unidades (¡SIN STOCK!)")
            elif cantidad <= 3:
                print(f"  ⚠️  {recurso}: {cantidad} unidades (¡STOCK BAJO!)")
            else:
                print(f"  ✅ {recurso}: {cantidad} unidades")
    else:
        print("  No hay recursos gastables registrados")
    
    # Mostrar recursos no gastables
    print("\n🟢 RECURSOS NO GASTABLES (no se consumen, solo se verifican):")
    print("-"*50)
    if RecursosNoGastables:
        recursos_ordenados = sorted(RecursosNoGastables, key=lambda x: x[0])
        for recurso, cantidad in recursos_ordenados:
            print(f"  🔧 {recurso}: {cantidad} unidades")
    else:
        print("  No hay recursos no gastables registrados")
    
    # Mostrar totales
    print("\n" + "="*60)
    total_gastables = sum(cantidad for _, cantidad in RecursosGastables)
    total_no_gastables = sum(cantidad for _, cantidad in RecursosNoGastables)
    print(f"Total de recursos gastables: {len(RecursosGastables)} tipos")
    print(f"Total de recursos no gastables: {len(RecursosNoGastables)} tipos")
    print(f"Total de recursos: {len(RecursosGastables) + len(RecursosNoGastables)} tipos")
    print("="*60)