import ipaddress
## Prgrama que ingresado la direccion en formato CIDR 192.168.1.0/28 me da
## toda la informacion necesaria de la red

def calcular_info_red(red):
    # Parsear la dirección de red en formato CIDR
    network = ipaddress.ip_network(red)

    # Obtener la dirección de red
    direccion_red = str(network.network_address)

    # Obtener la máscara de subred
    mascara_subred = str(network.netmask)

    # Obtener la dirección de broadcast
    direccion_broadcast = str(network.broadcast_address)

    # Obtener la dirección del gateway (primera dirección utilizable en la subred)
    direccion_gateway = str(network.network_address + 1)

    # Obtener la cantidad de hosts disponibles en la subred
    hosts_disponibles = network.num_addresses - 2  # Restar la dirección de red y la de broadcast

    return direccion_red, mascara_subred, direccion_gateway, direccion_broadcast, hosts_disponibles

# Pedir al usuario que ingrese la dirección de red en formato CIDR
direccion_red = input("Ingrese la dirección de red (formato CIDR): ")

# Calcular la información de la red
direccion_red, mascara_subred, direccion_gateway, direccion_broadcast, hosts_disponibles = calcular_info_red(direccion_red)

# Imprimir los resultados
print("Dirección de red:", direccion_red)
print("Máscara de subred:", mascara_subred)
print("Gateway:", direccion_gateway)
print("Broadcast:", direccion_broadcast)
print("Hosts disponibles:", hosts_disponibles)

