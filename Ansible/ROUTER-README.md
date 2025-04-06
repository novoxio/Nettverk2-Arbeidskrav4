<h1>Cisco Router-konfigurasjon med Ansible</h1>

<h2>Om prosjektet</h2>

<p>Dette prosjektet automatiserer konfigurasjonen av en Cisco-router ved hjelp av Ansible og en YAML-basert variabelfil. Playbooken er designet for å kunne håndtere både standard interface-konfigurasjon og VLAN-konfigurasjon dynamisk:</p>

<ul>
<li>Dersom <code>vlan</code> er spesifisert i interface-konfigurasjonen → Opprettes et subinterface med dot1Q-tagging.</li>
<li>Dersom <code>vlan</code> ikke er spesifisert → Konfigureres IP direkte på fysisk interface.</li>
</ul>

<h3>Funksjoner som konfigureres automatisk:</h3>

<ul>
<li>Hostname</li>
<li>VLAN og IP-konfigurasjon (med eller uten subinterface)</li>
<li>Statiske ruter</li>
<li>OSPF (ruting)</li>
<li>DHCP-server</li>
<li>HSRP (redundans)</li>
<li>Verifikasjon av konfigurasjonen</li>
</ul>

<hr>

<h2>Filstruktur</h2>

<pre>
├── router_config.yaml    # Ansible playbook
├── vars_router.yaml     # Variabler for router
└── inventory            # Inventory-fil med SSH-detaljer
</pre>

<hr>

<h2>Krav</h2>

<ul>
<li>Ansible installert på kontrollmaskinen</li>
<li>Cisco-moduler:</li>
</ul>

<pre>
ansible-galaxy collection install ansible.netcommon
ansible-galaxy collection install cisco.ios
</pre>

<ul>
<li>SSH-tilgang til Cisco-router</li>
</ul>

<hr>

<h2>Brukerveiledning</h2>

<h3>1. Inventory-fil</h3>

<pre>
[router1]
192.168.5.1 ansible_user=admin ansible_password=admin ansible_network_os=ios ansible_connection=network_cli
</pre>

<h3>2. Tilpass variabler i <code>vars_router.yaml</code></h3>

<pre>
hostname: "Router1"

interfaces:
  - { name: "GigabitEthernet0/0", ip: "192.168.5.1", mask: "255.255.255.0", vlan: 10 }
  - { name: "GigabitEthernet0/1", ip: "192.168.1.1", mask: "255.255.255.0" }

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

<h3>3. Kjør playbook</h3>

<pre>
ansible-playbook -i inventory router_config.yaml
</pre>

<hr>

<h2>Hvordan VLAN håndteres automatisk:</h2>

<table>
<thead>
<tr><th>Situasjon</th><th>Resultat</th></tr>
</thead>
<tbody>
<tr><td><code>vlan</code> er definert</td><td>Oppretter subinterface → <code>interface Gi0/0.10</code> med <code>encapsulation dot1Q 10</code></td></tr>
<tr><td><code>vlan</code> ikke definert</td><td>Bruker fysisk interface direkte → <code>interface Gi0/1</code></td></tr>
</tbody>
</table>

<hr>

<h2>Verifikasjon av konfigurasjon</h2>

<p>Etter kjøring av playbook vil Ansible automatisk kjøre disse kommandoene på routeren for å verifisere at alt fungerer:</p>

<table>
<thead>
<tr><th>Kommando</th><th>Sjekker</th></tr>
</thead>
<tbody>
<tr><td><code>show ip interface brief</code></td><td>IP-konfigurasjon på grensesnitt</td></tr>
<tr><td><code>show interfaces status</code></td><td>Status på grensesnitt (oppe/nede)</td></tr>
<tr><td><code>show running-config | include vlan</code></td><td>VLAN-konfigurasjon</td></tr>
<tr><td><code>show ip ospf neighbor</code></td><td>OSPF-naboer og status</td></tr>
</tbody>
</table>

<hr>

<h2>Oppsummering</h2>

<p>→ Dette prosjektet gir en fleksibel, automatisert og enkel måte å konfigurere Cisco-routere på via Ansible.</p>
<p>→ VLAN-håndtering skjer automatisk ut ifra om <code>vlan</code> er definert i variablene dine.</p>


