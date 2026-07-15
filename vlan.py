while True:
    entrada = input("Ingrese el numero de VLAN (o 's' para salir): ")

    if entrada.lower() == "s":
        print("Saliendo del programa...")
        break

    if not entrada.isdigit():
        print("Error: debe ingresar un numero valido.")
        continue

    vlan = int(entrada)

    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} corresponde al RANGO NORMAL (1 - 1005).")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} corresponde al RANGO EXTENDIDO (1006 - 4094).")
    else:
        print(f"La VLAN {vlan} NO es valida. El rango permitido es 1 - 4094.")