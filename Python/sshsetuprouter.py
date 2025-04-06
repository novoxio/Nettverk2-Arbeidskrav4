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

def configure_hostname_and_domain(ser, hostname, domain_name):
    """Konfigurerer enhetsnavn og domenenavn."""
    logger.info(f"Setter enhetsnavn til {hostname} og domenenavn til {domain_name}")
    send_command(ser, f"hostname {hostname}")
    send_command(ser, f"ip domain-name {domain_name}")

def configure_ip(ser, interface, ip_address, subnet_mask, vlan_id=None, vlan_interface=None):
    """Konfigurerer IP-adresse på et spesifisert grensesnitt, og VLAN-subinterface hvis angitt."""
    logger.info(f"Konfigurerer {interface} med IP {ip_address} og subnet {subnet_mask}")
    
    if vlan_id and vlan_interface == interface:
        # Create subinterface and encapsulation for VLAN
        subinterface = f"{interface}.{vlan_id}"
        send_command(ser, f"interface {subinterface}")
        send_command(ser, f"encapsulation dot1Q {vlan_id}")
        send_command(ser, f"ip address {ip_address} {subnet_mask}")
        logger.info(f"VLAN {vlan_id} konfigurert på {subinterface} med IP {ip_address} og subnet {subnet_mask}")
        
    else:
        send_command(ser, f"interface {interface}")
        send_command(ser, f"ip address {ip_address} {subnet_mask}")
        
    send_command(ser, "no shutdown")
    send_command(ser, "exit")

def configure_ssh(ser, username, password):
    """Setter opp SSH på routeren."""
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

def configure_router(ser, enable_password, hostname, domain_name, interfaces, vlan_data, username, password):
    """Konfigurerer routeren med ønsket IP-adresse, SSH-innstillinger, enhetsnavn og domenenavn, inkludert VLAN hvis angitt."""
    try:
        # Sett enhetskonfigurasjon
        send_command(ser, "\r")
        send_command(ser, "enable")
        send_command(ser, enable_password)
        send_command(ser, "configure terminal")

        # Konfigurerer enhetsnavn og domenenavn
        configure_hostname_and_domain(ser, hostname, domain_name)
        
        # Konfigurerer flere fysiske interfaces
        for interface_data in interfaces:
            interface = interface_data['interface']
            ip_address = interface_data['ip_address']
            subnet_mask = interface_data['subnet_mask']
            configure_ip(ser, interface, ip_address, subnet_mask)
        
        # Konfigurering av flere VLANer
        for vlan in vlan_data:
            vlan_id = vlan['vlan_id']
            vlan_interface = vlan['vlan_interface']
            vlan_ip = vlan['vlan_ip']
            vlan_subnet = vlan['vlan_subnet']
            # Ensure VLAN IP is assigned to the VLAN subinterface, not physical interface
            configure_ip(ser, vlan_interface, vlan_ip, vlan_subnet, vlan_id, vlan_interface)

        # Konfigurerer SSH
        configure_ssh(ser, username, password)

        # Konfigurerer VTY-linjer for SSH-tilkobling
        configure_vty(ser)

        # Lagre konfigurasjonen
        send_command(ser, "write memory", delay=2)
        logger.info(f"✅ Alle interfaces og VLAN-er konfigurert! SSH, hostname '{hostname}' og domain '{domain_name}' konfigurert.")

    except Exception as e:
        logger.error(f"❌ Feil ved konfigurasjon: {e}")

def main():
    """Main-funksjon for å håndtere brukerinput og oppsett av routeren."""
    try:
        # Håndterer input fra bruker
        port = input("Skriv inn serialport (f.eks. COM3 eller /dev/ttyS3): ")
        baudrate = 9600
        hostname = input("Skriv inn ønsket enhetsnavn: ")
        domain_name = input("Skriv inn ønsket domenenavn: ")
        username = input("Skriv inn ønsket SSH-brukernavn: ")
        password = getpass.getpass("Skriv inn ønsket SSH-passord: ")
        enable_password = getpass.getpass("Skriv inn enable-passord: ")

        # Konfigurere flere fysiske interfaces
        interfaces = []
        more_interfaces = 'ja'
        while more_interfaces.lower() == 'ja':
            interface = input("Skriv inn fysisk interface (f.eks. GigabitEthernet0/1): ")
            ip_address = input(f"Skriv inn IP-adresse for {interface} (f.eks. 192.168.1.1): ")
            subnet_mask = input(f"Skriv inn subnet-mask for {interface} (f.eks. 255.255.255.0): ")
            interfaces.append({
                'interface': interface,
                'ip_address': ip_address,
                'subnet_mask': subnet_mask
            })
            more_interfaces = input("Vil du konfigurere flere fysiske interfaces? (ja/nei): ")

        # Spør om flere VLAN (valgfritt)
        vlan_data = []
        vlan_input = input("Vil du konfigurere VLAN? (ja/nei): ").lower()
        if vlan_input == 'ja':
            while True:
                vlan_id = input("Skriv inn VLAN-ID: ")
                vlan_interface = input(f"Skriv inn grensesnittet hvor VLAN {vlan_id} skal konfigureres (f.eks. GigabitEthernet0/1): ")
                vlan_ip = input(f"Skriv inn IP-adresse for VLAN {vlan_id}: ")
                vlan_subnet = input(f"Skriv inn subnet-mask for VLAN {vlan_id}: ")
                
                vlan_data.append({
                    'vlan_id': vlan_id,
                    'vlan_interface': vlan_interface,
                    'vlan_ip': vlan_ip,
                    'vlan_subnet': vlan_subnet
                })
                
                more_vlans = input("Vil du konfigurere flere VLANs? (ja/nei): ").lower()
                if more_vlans != 'ja':
                    break

        # Åpner seriell forbindelse
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(1)
        except serial.SerialException as e:
            logger.error(f"❌ Serial-feil: {e}")
            sys.exit(1)

        # Konfigurerer routeren med input fra bruker og VLAN data
        configure_router(ser, enable_password, hostname, domain_name, interfaces, vlan_data, username, password)

        # Lukk seriell forbindelse
        ser.close()

    except Exception as e:
        logger.error(f"❌ Feil i hovedfunksjonen: {e}")

if __name__ == "__main__":
    main()
