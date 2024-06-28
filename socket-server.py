import socket

host = "127.0.0.1"
port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Determniar Host y puerto
    s.bind((host, port))
    # Escuchar conecciones entrantes permitiendo hasta 5 en cola
    s.listen(5)
    print("Listening in {}:{}...".format(host, port))

    # Aceptar conexiones entrantes
    conn, addr = s.accept()

    with conn:
        print("Stablish conection from:", addr)

        while True:
            # Imprimir datos del cliente
            data = conn.recv(1024)
            if not data:
                break
            # Imprimir datos recividos
            data = data.strip()  # Quitar el salto de linea putty
            print("Recived data:", data.decode())
            # Enviar respuesta al cliente
            conn.sendall(b"Recibido: " + data)
