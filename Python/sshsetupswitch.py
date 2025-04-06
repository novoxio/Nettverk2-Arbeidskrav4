import serial
import time
import getpass
import sys
import logging

# Sett opp logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_command(ser, command, delay=1):
    """Sender en kommando via seriell tilkobling og venter en stund."""
    logger.debug(f"Sender kommando: {command}")
    ser.write(command.encode() + b"\r")
    time.sleep(delay)

def configure_vlan(ser, vlan_name, vlan_ip):
    """Konfigurerer VLAN på enheten."""
    logger.info(f"Konfigurerer VLAN {vlan_name} med IP {vlan_ip}")
    send_command(ser, f"vlan {vlan_name}")
    send_command(ser, f"name {vlan_name}")
    send_command(ser, f"interface vlan {vlan_name}")
    send_command(ser, f"ip address {vlan_ip} 255.255.255.0")
    send_command(ser, "no shutdown")
    send_command(ser, "exit")

def configure_interfaces(ser, interfaces):
    """Konfigurerer flere grensesnitt på enheten."""
    for interface, ip_subnet in interfaces.items():
        logger.info(f"Konfigurerer grensesnitt {interface} med IP {ip_subnet}")
        send_command(ser, f"interface {interface}")
        send_command(ser, f"ip address {ip_subnet}")
        send_command(ser, "no shutdown")
        send_command(ser, "exit")

def configure_ssh(ser, username, password):
    """Setter opp SSH på enheten."""
    logger.info("Konfigurerer SSH...")
    send_command(ser, f"username {username} privilege 15 secret {password}")
    send_command(ser, "crypto key generate rsa", delay=2)
    send_command(ser, "2048", delay=2)
    send_command(ser, "\r", delay=2)
    send_command(ser, "ip ssh version 2")

def configure_vty(ser):
    """Setter opp VTY-linjer for SSH-tilkobling."""
    logger.info("Konfigurerer VTY-linjer for SSH-tilkobling...")
    send_command(ser, "line vty 0 15")
    send_command(ser, "no password")
    send_command(ser, "login local")
    send_command(ser, "transport input ssh")
    send_command(ser, "exit")

def display_ip_overview(vlan_ip, interfaces):
    """Viser en oversikt over IP-adresser og SSH-tilgang."""
    logger.info("\n--- IP-oversikt ---")
    print(f"SSH kan nås på VLAN IP: {vlan_ip} (Bruk SSH på denne IP-en med riktig bruker og passord).")
    print("Grensesnitt konfigurerte IP-er:")
    for interface, ip_subnet in interfaces.items():
        print(f"{interface}: {ip_subnet}")

def configure_device(ser, hostname, domain, interfaces, vlan_name, vlan_ip, username, password, enable_password):
    """Konfigurerer hele enheten med SSH, VLAN og flere grensesnitt."""
    try:
        logger.info("Starter konfigurasjonen...")
        send_command(ser, "\r")
        send_command(ser, "enable")
        send_command(ser, enable_password)
        send_command(ser, "configure terminal")

        # Hostname og domene
        send_command(ser, f"hostname {hostname}")
        send_command(ser, f"ip domain-name {domain}")

        # Konfigurerer VLAN
        configure_vlan(ser, vlan_name, vlan_ip)

        # Konfigurerer flere grensesnitt
        configure_interfaces(ser, interfaces)

        # Oppretter SSH-bruker og konfigurerer SSH
        configure_ssh(ser, username, password)

        # Konfigurerer VTY-linjer
        configure_vty(ser)

        # Lagre konfigurasjonen
        send_command(ser, "write memory", delay=2)
        logger.info(f"✅ SSH satt opp, VLAN {vlan_name} IP {vlan_ip}, og {len(interfaces)} grensesnitt konfigurert!")

        # Vist oversikt etter konfigurasjon
        display_ip_overview(vlan_ip, interfaces)

    except Exception as e:
        logger.error(f"❌ Feil ved konfigurasjon: {e}")

def main():
    """Main-funksjon for å håndtere brukerinput og oppsett av enheten."""
    try:
        # Håndterer input fra bruker
        port = input("Skriv inn serialport (f.eks. COM3 eller /dev/ttyS3): ")
        baudrate = 9600
        username = input("Skriv inn ønsket SSH-brukernavn: ")
        password = getpass.getpass("Skriv inn ønsket SSH-passord: ")
        enable_password = getpass.getpass("Skriv inn enable-passord: ")
        hostname = input("Skriv inn enhetsnavn: ")
        domain = input("Skriv inn domene: ")
        vlan_name = input("Skriv inn VLAN ID/Name: ")
        vlan_ip = input("Skriv inn VLAN IP-adresse: ")

        # Åpner seriell forbindelse
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(1)
        except serial.SerialException as e:
            logger.error(f"❌ Serial-feil: {e}")
            sys.exit(1)

        # Håndterer flere grensesnitt
        interfaces = {}
        while True:
            interface = input("Skriv inn grensesnitt (f.eks. GigabitEthernet0/1) eller trykk Enter for å avslutte: ")
            if not interface:
                break
            ip_subnet = input(f"Skriv inn IP-adresse og subnettmaske for {interface} (f.eks. 192.168.1.1 255.255.255.0): ")
            interfaces[interface] = ip_subnet

        # Kaller på funksjon for å konfigurere enheten
        configure_device(ser, hostname, domain, interfaces, vlan_name, vlan_ip, username, password, enable_password)

        # Lukk seriell forbindelse
        ser.close()

    except Exception as e:
        logger.error(f"❌ Feil i hovedfunksjonen: {e}")

if __name__ == "__main__":
    main()
