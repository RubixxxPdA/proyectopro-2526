from core import *

def MenuPrincipal():
    """Menu del sistema"""
    while True:
        print("\n"+"="*50)
        print("Sistema Agendamiento  RR Salon de unnas")
        print("\n"+"="*50)
        print("Opciones de inicio de sesion")
        print("1. Inicio sesion Administracion")
        print("2. Inicio sesion Cliente")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            password = input("Ingrese la contrasenna: ")
            if password == "rrnails":
                print("1. Mostrar la agenda ")
                print("2. Agregar recurso")
                print("3. Mostrar inventario")
                print("4. Agregar servicio")
                print("5. Guardar y salir")

                option = input("Seleccione una opcion: ").strip()

                if option == "1":
                    mostrar_toda_agenda()
                elif option == "2":
                    agregar_recurso()
                elif option== "3":
                    mostrar_inventario()    
                elif option == "4":
                    agregar_servicio()
                elif option == "5":
                    guardar_datos()
                    
                else:
                    print("Opcion no valida")
            else:
                print("Contrasenna incorrecta!!!")
        elif opcion == "2":
            print("1. Agendar cita")
            print("2. Eliminar cita")
            print("3. Guardar y salir")
            opcione = input("Seleccione una opcion: ").strip()

            if opcione == "1":
                print("\n--- SERVICIOS DISPONIBLES ---")
                for i, servicio in enumerate(Servicios, 1):
                    print(f"{i}. {servicio[0]} - {servicio[1]} minutos")

                try:
                    servicio_idx = int(input("Seleccione el número del servicio: ")) - 1
                    if 0 <= servicio_idx < len(Servicios):
                        agendar_cita(servicio_idx)
                    else:
                        print("Opción no válida")
                except ValueError:
                    print("Por favor, ingrese un número válido")
            elif opcione == "2":
                eliminar_cita()

            elif opcione == "3":
                guardar_datos()
                
            else:
                print("Opcion no valida")
        elif opcion == 3:
            guardar_datos()
            break

if __name__ == "__main__":
    MenuPrincipal()
