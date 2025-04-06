<h1>Nettverk2 - Arbeidskrav 4</h1>

<h2>Beskrivelse</h2>
<p>Dette prosjektet er en del av Nettverk2 - Arbeidskrav 4. Prosjektet handler om automatisering av nettverkskonfigurasjon på Cisco rutere og switcher. Arbeidet er delt inn i to deler:</p>
<ul>
  <li>Ansible → Automatisering med YAML playbooks.</li>
  <li>Python → Automatisering med Serial-tilkboling og Python-skript.</li>
</ul>

<h2>Innhold</h2>

<h3>Ansible</h3>
<p>Mappen <code>Ansible/</code> inneholder Ansible playbooks og variabler brukt for automatisk konfigurasjon av router og switch.</p>

<h4>Filstruktur:</h4>
<table>
  <tr><th>Fil</th><th>Beskrivelse</th></tr>
  <tr><td>inventory.ini</td><td>Inneholder IP-adresser til router og switch.</td></tr>
  <tr><td>router_config.yaml</td><td>Ansible playbook for å konfigurere router.</td></tr>
  <tr><td>switch_config.yaml</td><td>Ansible playbook for å konfigurere switch.</td></tr>
  <tr><td>vars_router.yaml</td><td>Variabler for router-konfigurasjon (VLAN, Interfaces, OSPF, DHCP, HSRP).</td></tr>
  <tr><td>vars_switch.yaml</td><td>Variabler for switch-konfigurasjon (VLAN, interfaces,).</td></tr>
  <tr><td>router-readme.md</td><td>Dokumentasjon for router playbook.</td></tr>
  <tr><td>switch-readme.md</td><td>Dokumentasjon for switch playbook.</td></tr>
</table>

<h3>Python</h3>
<p>Mappen <code>Python/</code> inneholder Python-skript som bruker SSH for å koble til og konfigurere router og switch automatisk.</p>

<h4>Filstruktur:</h4>
<table>
  <tr><th>Fil</th><th>Beskrivelse</th></tr>
  <tr><td>sshsetuprouter.py</td><td>Python-script for automatisk konfigurasjon av router via SSH.</td></tr>
  <tr><td>sshsetupswitch.py</td><td>Python-script for automatisk konfigurasjon av switch via SSH.</td></tr>
  <tr><td>SSH-ROUTER-README.MD</td><td>Dokumentasjon for router-script.</td></tr>
  <tr><td>SSH-SWITCH-README.MD</td><td>Dokumentasjon for switch-script.</td></tr>
</table>

<h2>Formål med arbeidskravet</h2>
<p>Automatisering av nettverksutstyr blir mer og mer vanlig i IT-bransjen. I dette arbeidskravet vises to forskjellige metoder for automatisering:</p>
<ul>
  <li>Bruk av Ansible for strukturert og skalerbar konfigurasjon.</li>
  <li>Bruk av Python for direkte tilkobling og manuell konfigurasjon.</li>
</ul>

<p>Begge metodene bidrar til enklere og mer effektiv drift av nettverk.</p>
