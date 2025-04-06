<h1>Cisco Switch-konfigurasjon med Ansible</h1>
<p>Dette Ansible-playbooket er laget for å konfigurere Cisco-switcher ved bruk av <code>cisco.ios</code>-samlingen. Det automatiserer oppsettet av VLAN-er, trunk-porter, access-porter, EtherChannel, VRF og utfører nødvendige verifikasjoner.</p>

<h2>🧾 Oversikt</h2>
<p>Playbooken konfigurerer en Cisco-switch med følgende oppgaver:</p>
<ul>
    <li>Setter vertens navn (hostname) for switchen.</li>
    <li>Konfigurerer VLAN-er.</li>
    <li>Konfigurerer trunk-porter.</li>
    <li>Konfigurerer access-porter.</li>
    <li>Setter opp EtherChannel.</li>
    <li>Konfigurerer VRF (Virtual Routing and Forwarding).</li>
    <li>Lagrer konfigurasjonen hvis det er endringer.</li>
</ul>

<h2>📂 Filstruktur</h2>
<ul>
    <li><code>switch_config.yaml</code>: Ansible-playbook for å konfigurere switchen.</li>
    <li><code>vars_switch.yaml</code>: Variabelfil som inneholder konfigurasjoner for switchen (VLAN-er, trunk-porter, access-porter, EtherChannel, DHCP, VRF, etc.).</li>
</ul>

<h2>⚙️ Krav</h2>
<ul>
    <li><code>Ansible</code> installert på systemet.</li>
    <li><code>cisco.ios</code> samling installert.</li>
</ul>
<p>Du kan installere <code>cisco.ios</code>-samlingen med følgende kommando:</p>
<pre><code>ansible-galaxy collection install cisco.ios</code></pre>
<p>SSH-tilgang til Cisco-switchene er nødvendig.</p>

<h2>🔧 Oppsett</h2>
<h3>1. Inventory-fil</h3>
<p>Opprett en inventory-fil for å spesifisere Cisco-switchene dine:</p>
<pre><code>[cisco_switches]
192.168.1.1 ansible_user=admin ansible_password=admin ansible_network_os=ios ansible_connection=network_cli</code></pre>

<h3>2. Variabelkonfigurasjon</h3>
<p>Rediger <code>vars_switch.yaml</code>-filen for å tilpasse konfigurasjonene, inkludert VLAN-ID-er, access-porter, trunk-porter, EtherChannel og VRF-detaljer.</p>
<pre><code># Hostname for switchen
hostname: "Switch1"

# VLAN-konfigurasjon
vlans:
  - id: 10
    name: "VLAN10"
  - id: 20
    name: "VLAN20"

# Liste over trunk-porter
trunk_ports:
  - "GigabitEthernet1/0/5"
  - "GigabitEthernet1/0/6"

# Access-porter og tilknyttede VLAN-er
access_ports:
  - port: "GigabitEthernet1/0/3"
    vlan: 10
  - port: "GigabitEthernet1/0/4"
    vlan: 20

# EtherChannel-konfigurasjon
etherchannel:
  mode: "active"  # Bruk LACP-modus
  group: 1
  ports:
    - "GigabitEthernet1/0/8"
    - "GigabitEthernet1/0/9"

# VRF-konfigurasjon
vrf:
  name: "Mgmt-vrf"
  interfaces:
    - "GigabitEthernet0/0"</code></pre>

<h3>3. Kjøre Playbook</h3>
<p>Etter at du har satt opp inventory-filen og variabelfilen, kan du kjøre playbooken med følgende kommando:</p>
<pre><code>ansible-playbook -i inventory switch_config.yaml</code></pre>

<h2>🔄 Oppgavebeskrivelse</h2>
<p>Playbooken utfører følgende oppgaver:</p>
<ul>
    <li><strong>Sett Hostname</strong>: Setter vertens navn på switchen som spesifisert i <code>hostname</code>-variabelen.</li>
    <li><strong>Konfigurer VLAN-er</strong>: Oppretter VLAN-ene som er definert i <code>vlans</code>-listen og tildeler navn til dem.</li>
    <li><strong>Konfigurer Trunk-porter</strong>: Konfigurerer trunk-porter og tillater VLAN-ene 10 og 20 på portene som er definert i <code>trunk_ports</code>-listen.</li>
    <li><strong>Konfigurer Access-porter</strong>: Konfigurerer access-porter og tildeler VLAN-ene 10 og 20 til portene spesifisert i <code>access_ports</code>-listen.</li>
    <li><strong>Konfigurer EtherChannel</strong>: Konfigurerer EtherChannel ved å gruppere fysiske grensesnitt og tildele trunk-modus. Verifiserer EtherChannel-status ved å kjøre <code>show etherchannel summary</code>.</li>
    <li><strong>Konfigurer VRF</strong>: Hvis VRF er definert, oppretter denne oppgaven VRF og assosierer grensesnittene med den.</li>
</ul>

<h2>📝 Verifikasjon</h2>
<p>Playbooken utfører flere verifikasjonstrinn for å sikre at konfigurasjonene er brukt korrekt:</p>
<ul>
    <li><strong>EtherChannel Status</strong>: Verifiserer EtherChannel-konfigurasjonen ved å bruke <code>show etherchannel summary</code>.</li>
    <li><strong>VRF-konfigurasjon</strong>: Verifiserer VRF-konfigurasjonen hvis definert.</li>
    <li><strong>Generell konfigurasjonsverifikasjon</strong>: Konfigurasjonen lagres hvis noen av oppgavene resulterer i endringer.</li>
</ul>

<h2>🚨 Feilhåndtering</h2>
<p>Hvis det oppstår problemer under EtherChannel- eller VRF-konfigurasjonen, vil en feilmelding vises ved hjelp av <code>debug</code>-modulen.</p>

<h2>🛠️ Handlere</h2>
<p>Konfigurasjonen lagres når det er modifikasjoner (f.eks. nye VLAN-er, trunk-porter, access-porter osv.).</p>
<pre><code>- name: Save config
    cisco.ios.ios_config:
      save_when: modified</code></pre>

<h2>👨‍💻 Forfatter</h2>
<p>© Torben – 2025</p>

<div style="background-color: #eef; padding: 10px; border-left: 4px solid #88f; margin: 10px 0;">
    <p><strong>Merk:</strong> Husk å justere IP-adresser, brukernavn, passord og andre konfigurasjoner slik at de passer til ditt miljø.</p>
</div>

