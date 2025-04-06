<!DOCTYPE html>
<html lang="no">
<head>
  <meta charset="UTF-8">
  <title>Router-konfigurasjon med Ansible</title>
  <style>
    body {
      font-family: sans-serif;
      background-color: #ffffff;
      color: #000;
      padding: 20px;
      line-height: 1.6;
      max-width: 900px;
      margin: auto;
    }
    h1, h2, h3 {
      color: #0b3d91;
    }
    pre {
      background-color: #f4f4f4;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      overflow-x: auto;
    }
    code {
      background-color: #eee;
      padding: 2px 4px;
      border-radius: 3px;
    }
    ul {
      padding-left: 20px;
    }
    .note {
      background-color: #eef;
      padding: 10px;
      border-left: 4px solid #88f;
      margin: 10px 0;
    }
  </style>
</head>
<body>

  <h1>📡 Cisco Router-konfigurasjon med Ansible</h1>

  <h2>🧾 Om prosjektet</h2>
  <p>Dette prosjektet automatiserer konfigurasjonen av en Cisco-router ved hjelp av Ansible og en YAML-basert variabelfil. Den dekker:</p>
  <ul>
    <li>Hostname</li>
    <li>VLAN og IP-konfigurasjon</li>
    <li>Statiske ruter</li>
    <li>OSPF</li>
    <li>DHCP</li>
    <li>HSRP</li>
    <li>Konfigurasjonsverifikasjon</li>
  </ul>

  <h2>📂 Filstruktur</h2>
  <pre>
router_config.yaml     # Ansible playbook
vars_router.yaml       # Variabler for router
inventory              # Inventory-fil med SSH-detaljer
  </pre>

  <h2>⚙️ Krav</h2>
  <ul>
    <li>Ansible installert</li>
    <li>Python-moduler: <code>ansible.netcommon</code> og <code>cisco.ios</code></li>
    <li>Tilgang via SSH til en Cisco-router</li>
  </ul>

  <h2>🚀 Hvordan bruke</h2>
  <ol>
    <li>Opprett en <code>inventory</code>-fil som dette:</li>
    <pre>
[router1]
192.168.5.1 ansible_user=admin ansible_password=admin ansible_network_os=ios ansible_connection=network_cli
    </pre>
    <li>Tilpass <code>vars_router.yaml</code> etter ditt miljø.</li>
    <li>Kjør playbooken:</li>
    <pre>ansible-playbook -i inventory router_config.yaml</pre>
  </ol>

  <h2>🛠️ Eksempel: <code>vars_router.yaml</code></h2>
  <pre>
hostname: "Router1"

interfaces:
  - { name: "GigabitEthernet0/0", ip: "192.168.5.1", mask: "255.255.255.0", vlan: 10 }
  - { name: "GigabitEthernet0/1", ip: "192.168.1.1", mask: "255.255.255.0", vlan: 20 }

static_routes:
  - { dest: "0.0.0.0", mask: "0.0.0.0", next_hop: "192.168.2.254" }

ospf:
  process_id: 1
  networks:
    - { network: "192.168.1.0", wildcard: "0.0.0.255", area: 0 }
    - { network: "192.168.2.0", wildcard: "0.0.0.255", area: 0 }

dhcp:
  enabled: true
  pool_name: "Router2_pool"
  network: "192.168.1.0"
  netmask: "255.255.255.0"
  default_router: "192.168.1.1"
  dns_servers: "8.8.8.8"
  lease_time: "12"

hsrp:
  - { interface: "GigabitEthernet0/0", group: 1, virtual_ip: "192.168.2.254", priority: 110, preempt: true }
  - { interface: "GigabitEthernet0/1", group: 1, virtual_ip: "192.168.1.254", priority: 110, preempt: true }
  </pre>

  <h2>🔍 Verifikasjon</h2>
  <p>Følgende kommandoer kjøres automatisk etter konfigurasjon:</p>
  <ul>
    <li><code>show ip interface brief</code></li>
    <li><code>show interfaces status</code></li>
    <li><code>show run | include vlan</code></li>
    <li><code>show ip ospf neighbor</code></li>
  </ul>
  <div class="note">
    Resultatene vises i terminalen via <code>debug</code>-meldinger.
  </div>

  <h2>👨‍💻 Forfatter</h2>
  <p>© Torben – 2025</p>

</body>
</html>


