const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const root = process.env.SITE_DIR || '_site';
const html = fs.readFileSync(path.join(root, 'contact/index.html'), 'utf8');
const code = fs.readFileSync(path.join(root, 'assets/js/contact-details.js'), 'utf8');
const payload = html.match(/data-contact="([^"]+)"/)[1];
const expected = JSON.parse(Buffer.from(Buffer.from(payload, 'base64').map(b => b ^ 93)).toString());

// Minimal DOM harness: exercise the actual shipped event handler without a browser dependency.
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.attrs = {}; this.hidden = false; this.textContent = ''; }
  appendChild(child) { this.children.push(child); return child; }
  setAttribute(key, value) { this.attrs[key] = value; }
  addEventListener(type, handler, options) { this.event = { type, handler, options }; }
  focus() { this.focused = true; }
}
function descendants(node) { return [node, ...node.children.flatMap(descendants)]; }
function text(node) { return node.textContent + node.children.map(text).join(''); }

function setup() {
  const container = new Element('div'); container.dataset = { contact: payload };
  const button = new Element('button'); button.attrs['aria-expanded'] = 'false';
  const output = new Element('div'); output.hidden = true;
  const nodes = { contactgegevens: container, 'show-contact-details': button, 'contact-details': output };
  const document = {
    getElementById: id => nodes[id],
    createElement: tag => new Element(tag),
    createDocumentFragment: () => new Element('fragment'),
    createTextNode: value => { const n = new Element('text'); n.textContent = value; return n; },
  };
  let decodes = 0;
  vm.runInNewContext(code, {
    document, TextDecoder, Uint8Array,
    atob: value => { decodes++; return Buffer.from(value, 'base64').toString('binary'); },
  });
  return { button, output, decodes: () => decodes };
}

test('contact details are not decoded or inserted until the visitor clicks', () => {
  const { button, output, decodes } = setup();
  assert.equal(decodes(), 0);
  assert.equal(output.hidden, true);
  assert.equal(text(output), '');
  assert.equal(button.event.type, 'click');
  assert.equal(button.event.options.once, true);
});

test('a click reveals the full address and usable email/phone links, then focuses the details', () => {
  const { button, output, decodes } = setup();
  button.event.handler();
  assert.equal(decodes(), 1);
  assert.equal(output.hidden, false);
  assert.equal(button.hidden, true);
  assert.equal(button.attrs['aria-expanded'], 'true');
  assert.equal(output.focused, true);
  for (const value of [...expected.address, expected.phone, expected.email]) assert.ok(text(output).includes(value));
  const links = descendants(output).filter(node => node.tag === 'a');
  assert.deepEqual(links.map(node => node.href), [
    'tel:' + expected.phone.replace(/[^+\d]/g, ''), 'mailto:' + expected.email,
  ]);
});

test('the script does nothing on a page without the contact component', () => {
  assert.doesNotThrow(() => vm.runInNewContext(code, { document: { getElementById: () => null } }));
});
