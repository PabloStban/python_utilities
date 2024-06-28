from pwn import *
from termcolor import colored
from scapy.all import *
import signal
import sys
import time
import logging
import threading

# libreria loggin para hacer que scappy solo me muestre errores criticos y no warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

p1 = log.progress("TCP Scan")
p1.status("Scanning ports...")


# Gestionar el ctrl + C con signal
def def_handler(sig, frame):
    print(colored("\n\n[!] Exiting....\n", "red"))
    p1.failure("Scan aborted (Ctrl + C has been pressed)")
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


def scanPort(ip, port):
    # Selecciona un puerto aleatorio
    src_port = RandShort()
    try:
        # send recive para enviar y recibir paquetes envia algo y guarda lo que recibe
        response = sr1(
            IP(dst=ip) / TCP(sport=src_port, dport=port, flags="S"),
            timeout=2,
            verbose=False,
        )
        if response is None:
            return False
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
            # para enviar paquetes
            send(IP(dst=ip) / TCP(sport=src_port, dport=port, flags="R"), verbose=False)
            return True

    except Exception as e:
        # Utilizar pwn para mostrar el error log.failure
        log.failure(f"Error scanning {ip} on {port}: {e}")
        sys.exit(1)


def thread_function(ip, port):
    response = scanPort(ip, port)
    if response:
        log.info(f"Port: {port} - OPEN")


def main(ip, ports, end_port):
    threads = []
    time.sleep(2)

    for port in ports:
        p1.status(f"Scan progress [{port}/{end_port}]")

        thread = threading.Thread(target=thread_function, args=(ip, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    p1.success(f"Scan finished")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            colored(
                f"\n\n[!] Use: {colored('python','blue')} {colored('ports-scanner.py','green')} {colored('<ip> <ports-range>','yellow')}\n",
                "red",
            )
        )
        sys.exit(1)

    target_ip = sys.argv[1]
    port_range = sys.argv[2].split("-")
    start_port = int(port_range[0])
    end_port = int(port_range[1])

    ports = range(start_port, end_port + 1)

    main(target_ip, ports, end_port)
