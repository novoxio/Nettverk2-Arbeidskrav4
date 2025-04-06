<h1>Konfigurering av Cisco Router via Seriell Tilkobling (Python)</h1>

<p>Dette Python-skriptet lar deg konfigurere en Cisco-router via seriell tilkobling. Skriptet støtter konfigurasjon av grensesnitt, VLAN, IP-adresser, SSH-tilkobling og VTY-linjer for administrasjon av routeren.</p>

<h2>Funksjoner</h2>
<ul>
    <li><strong>Konfigurering av enhetsnavn og domenenavn:</strong> Sett enhetsnavn og domene for routeren.</li>
    <li><strong>Konfigurering av IP-adresser på grensesnitt:</strong> Sett IP-adresser på flere grensesnitt og VLAN.</li>
    <li><strong>Konfigurering av VLAN:</strong> Konfigurer VLAN med tilknyttede IP-adresser på virtuelle grensesnitt.</li>
    <li><strong>Konfigurering av SSH:</strong> Sett opp SSH for ekstern administrasjon.</li>
    <li><strong>Konfigurering av VTY-linjer:</strong> Konfigurer VTY-linjer for SSH-tilkobling.</li>
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
        <pre><code>python konfigurering_router.py</code></pre>
    </li>
    <li>Når du kjører skriptet, vil du bli bedt om å oppgi følgende informasjon:
        <ul>
            <li>Seriell port (f.eks. COM3 eller /dev/ttyS3)</li>
            <li>SSH-brukernavn og passord</li>
            <li>Enable-passord</li>
            <li>Enhetsnavn (hostname)</li>
            <li>Domene</li>
            <li>Grensesnitt og tilknyttede IP-adresser</li>
            <li>VLAN ID/Name og IP-adresse</li>
        </ul>
    </li>
    <li>Etter at skriptet er ferdig, vil en IP-oversikt bli vist, og routeren vil være konfigurert med VLAN, SSH, og grensesnitt.</li>
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

<h2>Mer informasjon</h2>
<p>For mer detaljer, sjekk koden i skriptet og logger under kjøringen for ytterligere feilsøking og konfigurasjonsbeskrivelser.</p>
