(function () {
  "use strict";

  const container = document.getElementById("contactgegevens");
  const button = document.getElementById("show-contact-details");
  const output = document.getElementById("contact-details");
  if (!container || !button || !output) return;

  button.addEventListener("click", function () {
    // Obfuscation against simple scrapers, not cryptographic protection.
    // Decode only after the visitor explicitly asks for the details.
    const bytes = Uint8Array.from(atob(container.dataset.contact), function (char) {
      return char.charCodeAt(0) ^ 93;
    });
    const details = JSON.parse(new TextDecoder().decode(bytes));
    const fragment = document.createDocumentFragment();

    function heading(text) {
      const node = document.createElement("h2");
      node.textContent = text;
      fragment.appendChild(node);
    }

    function link(label, href) {
      const paragraph = document.createElement("p");
      const anchor = document.createElement("a");
      anchor.textContent = label;
      anchor.href = href;
      paragraph.appendChild(anchor);
      fragment.appendChild(paragraph);
    }

    heading("Vestigingsadres");
    const address = document.createElement("address");
    details.address.forEach(function (line, index) {
      if (index) address.appendChild(document.createElement("br"));
      address.appendChild(document.createTextNode(line));
    });
    fragment.appendChild(address);
    heading("Telefoon");
    link(details.phone, "tel:" + details.phone.replace(/[^+\d]/g, ""));
    heading("E-mail");
    link(details.email, "mailto:" + details.email);

    output.appendChild(fragment);
    output.hidden = false;
    button.setAttribute("aria-expanded", "true");
    button.hidden = true;
    output.focus();
  }, { once: true });
}());
