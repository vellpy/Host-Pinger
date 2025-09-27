import subprocess
import time
import os
from pystyle import Colorate, Colors
from typing import Optional
import socket
import threading

LOGO = """
  ▄█    █▄     ▄████████  ▄█       
 ███    ███   ███    ███ ███       
 ███    ███   ███    █▀  ███       
 ███    ███  ▄███▄▄▄     ███       
 ███    ███ ▀▀███▀▀▀     ███       
 ███    ███   ███    █▄  ███       
 ███    ███   ███    ███ ███▌    ▄ 
  ▀██████▀    ██████████ █████▄▄██ 

       vel IP PINGER         
"""

INFO_BOX = """
╔═══════════[  vel  ]════════════╗
║ Discord: ndxk                  ║        
║ GitHub : github.com/vellpy     ║
╚════════════════════════════════╝
"""

COLORS = {
    "logo": Colors.yellow_to_red,
    "info": Colors.yellow_to_red,
    "prompt": Colors.yellow_to_red,
    "error": Colors.yellow_to_red,
    "ping_tag": Colors.yellow_to_red,
    "offline": Colors.yellow_to_red
}

SPEED_MAP = {"1": 0.1, "2": 1, "3": 5}

USER = "vel"
HOST = socket.gethostname()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def set_title(title: str):
    if os.name == "nt":
        os.system(f"title {title}")


def ping(ip: str) -> (bool, Optional[str]):
    """Ping the given IP once and return (online, ping_ms)"""
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True,
            text=True
        )
        output = result.stdout
        if "TTL=" in output:
            for line in output.splitlines():
                if "TTL=" in line:
                    for part in line.split():
                        if "time=" in part.lower():
                            return True, part.split("=")[1]
        return False, None
    except Exception:
        return False, None


def terminal_input(prompt_text: str) -> str:
    try:
        print(Colorate.Horizontal(COLORS["prompt"], f"╭─── {USER}@{HOST}"))
        print(Colorate.Horizontal(COLORS["prompt"], "│"))
        return input(Colorate.Horizontal(COLORS["prompt"], f"╰─>> {prompt_text} ")).strip()
    except RuntimeError:
        print("Error: stdin not available. Make sure console is open.")
        exit()


def prompt_menu(prompt: str, options: list) -> str:
    while True:
        choice = terminal_input(prompt)
        if choice in options:
            return choice
        print(Colorate.Horizontal(COLORS["error"], "[vel] ERROR! Invalid choice."))


class VelPinger:
    def __init__(self):
        self.ip = ""
        self.speed = 1

    def display_banner(self):
        print(Colorate.Horizontal(COLORS["logo"], LOGO))
        print(Colorate.Horizontal(COLORS["info"], INFO_BOX))

    def choose_speed(self):
        print(Colorate.Horizontal(COLORS["prompt"], "[1] Fast [2] Default [3] Low"))
        choice = prompt_menu("Choose request speed", SPEED_MAP.keys())
        self.speed = SPEED_MAP[choice]

    def enter_ip(self):
        self.ip = terminal_input("Enter IP to ping:")
        print(Colorate.Horizontal(COLORS["info"], f"[vel] Pinging {self.ip} with {self.speed} second(s) interval...\n"))

    def ping_loop(self):
        while True:
            online, ping_ms = ping(self.ip)
            tag = "[vel]"
            if online:
                print(Colorate.Horizontal(COLORS["ping_tag"], f"{tag} {self.ip} >> {ping_ms}"))
            else:
                print(Colorate.Horizontal(COLORS["offline"], f"{tag} {self.ip} >> Host is Offline"))
            time.sleep(self.speed)

    def run(self):
        try:
            if self.speed < 0.2:  # TODO: make threading slower
                thread = threading.Thread(target=self.ping_loop, daemon=True)
                thread.start()
                while True:
                    time.sleep(1)
            else:
                self.ping_loop()
        except KeyboardInterrupt:
            print(Colorate.Horizontal(COLORS["offline"], "\n[vel] Exiting..."))
            exit()


def main():
    set_title("vel IP PINGER")
    clear()
    app = VelPinger()
    app.display_banner()
    app.choose_speed()
    app.enter_ip()
    app.run()


if __name__ == "__main__":
    main()
