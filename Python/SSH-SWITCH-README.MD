<h1>Konfigurering av Cisco Switch via Seriell Tilkobling (Python)</h1>

<p>Dette Python-skriptet lar deg konfigurere en Cisco-switch via seriell tilkobling. Skriptet støtter konfigurasjon av VLAN, grensesnitt, trunk-porter, access-porter, EtherChannel, og SSH-tilkobling for administrasjon av switchen.</p>

<h2>Funksjoner</h2>
<ul>
    <li><strong>VLAN-konfigurasjon:</strong> Opprett VLAN, tilordne navn og IP-adresse.</li>
    <li><strong>Grensesnitt-konfigurasjon:</strong> Konfigurerer både trunk-porter og access-porter på switchen.</li>
    <li><strong>EtherChannel-konfigurasjon:</strong> Støtte for konfigurasjon av EtherChannel for aggregasjon av flere fysiske porter.</li>
    <li><strong>SSH-konfigurasjon:</strong> Sett opp SSH for sikker ekstern administrasjon av switchen.</li>
    <li><strong>VTY-linjer:</strong> Konfigurer VTY-linjer for SSH-tilkobling og administrasjon.</li>
    <li><strong>Logging:</strong> Skriptet bruker Python <code>logging</code>-modulen for å logge aktiviteter og feil under konfigurasjonen.</li>
</ul>

<h2>Krav</h2>
<ul>
    <li>Python 3.x</li>
    <li><code>pyserial</code>-pakken for seriell kommunikasjon</li>
</ul>

<h2>Bruk</h2>
<ol>
    <li>Installer nødvendige Python-pakker ved å kjøre:
        <pre><code>pip install pyserial</code></pre>
    </li>
    <li>Last ned eller klon skriptet til din lokale maskin.</li>
    <li>Kjør skriptet ved å bruke:
        <pre><code>python konfigurering_switch.py</code></pre>
    </li>
    <li>Når du kjører skriptet, vil du bli bedt om å oppgi følgende informasjon:
        <ul>
            <li>Seriell port (f.eks. COM3 eller /dev/ttyS3)</li>
            <li>SSH-brukernavn og passord</li>
            <li>Enable-passord</li>
            <li>Enhetsnavn (hostname)</li>
            <li>Domene</li>
            <li>VLAN ID/Name og IP-adresse</li>
            <li>Grensesnitt og tilknyttede IP-adresser</li>
        </ul>
    </li>
    <li>Etter at skriptet er ferdig, vil en IP-oversikt bli vist, og switchen vil være konfigurert med VLAN, SSH, og grensesnitt.</li>
</ol>

<h2>Feilsøking</h2>
<p>Skriptet bruker <code>logging</code>-modulen for å logge alle aktiviteter og eventuelle feil. Hvis du støter på problemer, kan du sjekke loggen for detaljerte feilmeldinger.</p>

<h2>Eksempel på output</h2>
<pre><code>2025-04-06 12:00:00 - INFO - Starter konfigurasjonen...
2025-04-06 12:00:01 - INFO - Konfigurerer VLAN TestVLAN med IP 192.168.10.1
2025-04-06 12:00:05 - INFO - Konfigurerer trunk-port Gi0/1
2025-04-06 12:00:10 - INFO - Konfigurerer access-port Gi0/2 med VLAN 10
2025-04-06 12:00:20 - INFO - ✅ SSH satt opp, VLAN TestVLAN IP 192.168.10.1, og 2 grensesnitt konfigurert!
2025-04-06 12:00:25 - INFO - --- IP-oversikt ---
SSH kan nås på VLAN IP: 192.168.10.1 (Bruk SSH på denne IP-en med riktig bruker og passord).
Grensesnitt konfigurerte IP-er:
GigabitEthernet0/1: Trunk
GigabitEthernet0/2: 192.168.1.1 255.255.255.0
</code></pre>

