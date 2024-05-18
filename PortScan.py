import socket
import os
import threading
import time
from pystyle import Colors, Colorate
from datetime import datetime

os.system("cls" if os.name == "nt" else "clear")
print(
    Colorate.Vertical(
        Colors.blue_to_red,
        """

██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║
██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
██║     ╚██████╔╝██║  ██║   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
github.com/dimxz
                                              
""",
        3,
    )
)


def get_time():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    return time


start = datetime.now().strftime("%d-%m-%Y-%H%M%S")


def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            print("[+]", Colorate.Color(Colors.green, f"Port {port}: Open"))
            return True
        else:
            print("[-]", Colorate.Color(Colors.red, f"Port {port}: Closed"))
            return False
    except Exception as e:
        print(
            "[!]", Colorate.Color(Colors.red, f"Error while scanning port {port}: {e}")
        )
        return False
    finally:
        sock.close()


def multi(host, port, open_ports):
    if scan_port(host, port):
        open_ports.append(port)


def main():
    timeNow = get_time()
    host = input(
        "[{}] ".format(timeNow)
        + Colorate.Horizontal(Colors.blue_to_red, "[?] Enter target host: ")
    )

    timeNow = get_time()
    start_port = int(
        input(
            "[{}] ".format(timeNow)
            + Colorate.Horizontal(Colors.blue_to_red, "[?] Enter start port: ")
        )
    )

    timeNow = get_time()
    end_port = int(
        input(
            "[{}] ".format(timeNow)
            + Colorate.Horizontal(Colors.blue_to_red, "[?] Enter end port: ")
        )
    )

    timeNow = get_time()
    print(
        "[{}] ".format(timeNow)
        + Colorate.Horizontal(
            Colors.blue_to_red,
            f"[+] Scanning ports {start_port} to {end_port} on {host} .... ",
        )
    )

    open_ports = []
    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=multi, args=(host, port, open_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if open_ports:
        filename = f"{host}_{start}.txt"
        with open(filename, "w") as file:
            file.write(f"Open ports on {host}:\n")
            for port in open_ports:
                file.write(f"{port}\n")
        print(
            "[{}] ".format(timeNow)
            + Colorate.Horizontal(
                Colors.blue_to_red, f"[+] All open ports saved to :  {filename}"
            )
        )


if __name__ == "__main__":
    main()
