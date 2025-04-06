
  <h1>📡 Cisco Router-konfigurasjon med Ansible</h1>

  <div class="section">
    <h2>🧾 Om prosjektet</h2>
    <p>Denne løsningen automatiserer konfigurasjonen av en Cisco-router ved hjelp av Ansible. Konfigurasjonen trekkes fra en YAML-fil og inkluderer blant annet:</p>
    <ul>
      <li>Hostname</li>
      <li>VLAN og IP-konfigurasjon</li>
      <li>Statiske ruter</li>
      <li>OSPF routing</li>
      <li>DHCP-tjeneste</li>
      <li>HSRP-konfigurasjon</li>
      <li>Verifikasjon av status</li>
    </ul>
  </div>

  <div class="section">
    <h2>📦 Filstruktur</h2>
    <pre>
router_config.yaml     # Ansible playbook
vars_router.yaml       # Variabler for router
inventory              # Inventory-fil med SSH-detaljer
    </pre>
  </div>

  <div class="section">
    <h2>⚙️ Krav</h2>
    <ul>
      <li>Ansible installert</li>
      <li>Moduler: <code>ansible.netcommon</code> og <code>cisco.ios</code></li>
      <li>Tilkobling til Cisco-router via SSH (network_cli)</li>
    </ul>
  </div>

  <div class="section">
    <h2>🚀 Hvordan bruke</h2>
    <p>1. Opprett en <code>inventory</code>-fil med riktig info:</p>
    <pre>
[router1]
192.168.5.1 ansible_user=admin ansible_password=admin ansible_network_os=ios ansible_connection=network_cli
    </pre>

    <p>2. Rediger <code>vars_router.yaml</code> etter dine behov (se eksempel nedenfor).</p>
    <p>3. Kjør playbooken:</p>
    <pre>ansible-playbook -i inventory router_config.yaml</pre>
  </div>

  <div class="section">
    <h2>🛠️ Eksempel på variabler (<code>vars_router.yaml</code>)</h2>
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
  </div>

  <div class="section">
    <h2>✅ Verifikasjon</h2>
    <p>Playbooken utfører automatisk verifisering av:</p>
    <ul>
      <li><code>show ip interface brief</code> – IP-konfigurasjon</li>
      <li><code>show interfaces status</code> – Port-status</li>
      <li><code>show run | include vlan</code> – VLAN-oversikt</li>
      <li><code>show ip ospf neighbor</code> – OSPF-naboer</li>
    </ul>
    <div class="note">Resultatene vises som debug-meldinger direkte i Ansible-output.</div>
  </div>

  <div class="section">
    <h2>👨‍💻 Forfatter</h2>
    <p>📅 2025 – Laget av <strong>Torben</strong></p>
  </div>

</body>
</html>
