---
layout: page
title: Contact
subtitle: Contact- en bedrijfsgegevens
share-title: AJH Consultancy - Deze website is in aanbouw
js:
  - /assets/js/contact-details.js
---
{% comment %}
Contactgegevens wijzigen

Het vestigingsadres, telefoonnummer en e-mailadres staan gecodeerd in het
attribuut data-contact in contact.md. Ze worden pas na een klik gedecodeerd
door assets/js/contact-details.js. Zet ze niet leesbaar in de openbare repository.

Nieuwe gegevens encoden (Python 3, zonder extra packages):
1. Vul in het voorbeeld hieronder je echte gegevens in en voer de code uit.
   Houd phone en email als tekst; address is een lijst met adresregels.

python3 - <<'PY'
import base64, json
gegevens = {
    "address": ["Bedrijfsnaam", "Straat 1", "1234 AB Plaats"],
    "phone": "06-12345678",
    "email": "naam@example.org",
}
raw = json.dumps(gegevens, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
print(base64.b64encode(bytes(b ^ 93 for b in raw)).decode("ascii"))
PY

2. Vervang in contact.md alleen de waarde tussen de dubbele aanhalingstekens
   van data-contact="..." door de volledige uitvoer van dit commando.
3. Commit contact.md. De bestaande build en publicatie blijven hetzelfde.

Controle van een wijziging, als je de site lokaal bouwt:
bundle exec jekyll build
python3 tests/check_site.py _site
node --test tests/contact-details.test.cjs

Dit is XOR met 93 gevolgd door base64: obfuscatie, geen echte versleuteling.
Commit geen leesbare gegevens of tijdelijke invoerbestanden als je die niet
in de openbare repository wilt hebben. De oude Git-geschiedenis blijft bestaan.
{% endcomment %}
<div id="contactgegevens" class="contact-reveal" data-contact="Jn88OTkvOC4uf2cGfxwXFX0eMjMuKDEpPDM+JH9xfxEyKSk4Ly4pLzw8KX1of3F/b21vbH0JGH19FTw8LzE4MH8AcX8tNTIzOH9nf21rcGxvZGtkbmhvf3F/ODA8NDF/Z388LzcyHTw3NXA+MjMuKDEpPDM+JHMzMX8g">
  <p>Klik hieronder om het vestigingsadres, telefoonnummer en e-mailadres te bekijken.</p>
  <button id="show-contact-details" type="button" class="contact-reveal-button" aria-controls="contact-details" aria-expanded="false">Contactgegevens tonen</button>
  <div id="contact-details" class="contact-details" role="region" aria-label="Contactgegevens" tabindex="-1" hidden></div>
  <noscript><p>Schakel JavaScript in om de contactgegevens te tonen.</p></noscript>
</div>

## belangrijke nummers
kvk `77102673`
btw `NL003148326B03`
