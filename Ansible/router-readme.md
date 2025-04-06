
<h1>📡 Cisco Router-konfigurasjon med Ansible</h1>

<h2>🧾 Om prosjektet</h2>
<p>Dette prosjektet automatiserer konfigurasjonen av en Cisco-router ved hjelp av Ansible og en YAML-basert variabelfil. Ansible-playbooken konfigurerer en rekke viktige nettverksfunksjoner for Cisco-routeren, inkludert:</p>
<ul>
    <li><strong>Hostname</strong>: Setter vertens navn for routeren.</li>
    <li><strong>VLAN og IP-konfigurasjon</strong>: Konfigurerer VLANs og tildeler IP-adresser til grensesnittene.</li>
    <li><strong>Statiske ruter</strong>: Legger til statiske ruter for trafikkdirigering.</li>
    <li><strong>OSPF (Open Shortest Path First)</strong>: Konfigurerer OSPF-ruting for å administrere nettverkskommunikasjon mellom flere routere.</li>
    <li><strong>DHCP (Dynamic Host Configuration Protocol)</strong>: Aktiverer DHCP-serveren for å dynamisk tildele IP-adresser til klienter i nettverket.</li>
    <li><strong>HSRP (Hot Standby Router Protocol)</strong>: Konfigurerer HSRP for redundans, slik at én router fungerer som en virtuell gateway i tilfelle den primære routeren mislykkes.</li>
    <li><strong>Konfigurasjonsverifikasjon</strong>: Verifiserer om konfigurasjonen har blitt korrekt implementert via Ansible.</li>
</ul>

<h2>Filstruktur</h2>
<p>Filene som er inkludert i prosjektet er:</p>
<pre>
router_config.yaml     # Ansible playbook  
vars_router.yaml       # Variabler for router  
inventory              # Inventory-fil med SSH-detaljer
</pre>

<h2>⚙️ Krav</h2>
<p>Før du bruker denne Ansible-playbooken, sørg for at følgende krav er oppfylt:</p>
<ul>
    <li><strong>Ansible installert</strong>: Ansible er nødvendig for å kjøre playbooken på systemet ditt.</li>
    <li><strong>Python-moduler:</strong> Du må installere <code>ansible.netcommon</code> og <code>cisco.ios</code> moduler, som gir spesifikke funksjoner for nettverkskonfigurasjon av Cisco-enheter.</li>
    <li><strong>SSH-tilgang til en Cisco-router:</strong> Du trenger SSH-tilgang til routeren du ønsker å konfigurere.</li>
</ul>

<h2>Hvordan bruke</h2>
<p>Følg disse trinnene for å bruke denne playbooken:</p>
<ol>
    <li>Opprett en <strong>inventory-fil</strong> med informasjon om routeren, for eksempel:</li>
</ol>

<pre>
[router1]
192.168.5.1 ansible_user=admin ansible_password=admin ansible_network_os=ios ansible_connection=network_cli
</pre>

<ol start="2">
    <li><strong>Tilpass <code>vars_router.yaml</code></strong> etter ditt spesifikke miljø. Dette inkluderer å sette riktig hostname, IP-adresser, VLAN-konfigurasjon og eventuelle andre nødvendige innstillinger.</li>
    <li><strong>Kjør playbooken</strong> for å utføre konfigurasjonen ved å bruke følgende kommando i terminalen:</li>
</ol>

<pre>
ansible-playbook -i inventory router_config.yaml
</pre>

<h2>🛠️ Eksempel: <code>vars_router.yaml</code></h2>
<p>Her er et eksempel på hvordan <code>vars_router.yaml</code> kan se ut:</p>
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

<h2>Verifikasjon</h2>
<p>Etter at konfigurasjonen er utført, kjøres følgende kommandoer automatisk for å bekrefte at konfigurasjonen er korrekt:</p>
<ul>
    <li><code>show ip interface brief</code>: Sjekker IP-konfigurasjonen på grensesnittene.</li>
    <li><code>show interfaces status</code>: Verifiserer status på grensesnittene (om de er administrativt oppe).</li>
    <li><code>show running-config | include vlan</code>: Bekrefter VLAN-konfigurasjonen.</li>
    <li><code>show ip ospf neighbor</code>: Verifiserer OSPF-naboer og status.</li>
</ul>
<p>Resultatene vises i terminalen via <code>debug</code>-meldinger, som kan brukes til å verifisere at alt er riktig satt opp.</p>



