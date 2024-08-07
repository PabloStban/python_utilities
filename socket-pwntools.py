from pwn import *
import re
import random

ip = 'tcp://f8ded528c09edc57.247ctf.com'
port = '50304'
cont = 0


with remote(ip,port) as conn:
    #mensaje = conn.recv().decode('utf-8')
    #print(f'mensaje')
    mensaje = conn.recvline()
    print(f"{mensaje}")
    mensaje = conn.recvline()
    print(f"{mensaje}")

    while cont < 500:
        a = random.randint(1,300)
        b = random.randint(1,300)
        enviar = a+b
        print(f'{cont+1}: {enviar}')
        conn.send(str(enviar).encode('utf-8'))
        cont += 1

    mensaje = conn.recvline().decode('utf-8').strip()
    print(f"{mensaje}")

    if 'What is the answer to' in mensaje:
        match = re.search(r'(\d+) \+ (\d+)', mensaje)
        
        if match:
            # Obtener los numeros y realizar la suma
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            respuesta =  num1 + num2
            print(f'Respuesta: {num1} + {num2} = {respuesta}')

            # Enviar Respuesta
            conn.send(str(respuesta).encode('utf-8'))
        else:
            print("Nose encontraron los numeros")
    else:
        print("!Error Not found numbers")

    mensaje = conn.recv()
    print(f"{mensaje}")

#conn.close()


    

