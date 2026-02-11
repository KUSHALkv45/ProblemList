const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data.json');
const VIEW_FILE = path.join(__dirname, 'view.html');

app.use(express.json());
app.use(express.static(__dirname));

// ── GET all items ──────────────────────────────────────────
app.get('/api/items', (req, res) => {
  const raw = fs.readFileSync(DATA_FILE, 'utf8');
  res.json(JSON.parse(raw));
});

// ── POST save all items + bake into view.html ──────────────
app.post('/api/items', (req, res) => {
  const items = req.body;

  // 1. Save to data.json
  fs.writeFileSync(DATA_FILE, JSON.stringify(items, null, 2));

  // 2. Bake into view.html by replacing the data placeholder
  let viewHTML = fs.readFileSync(VIEW_FILE, 'utf8');
  const baked = `const DATA = ${JSON.stringify(items, null, 2)};`;
  viewHTML = viewHTML.replace(/const DATA = [\s\S]*?;/, baked);
  fs.writeFileSync(VIEW_FILE, viewHTML);

  res.json({ ok: true });
});

app.listen(PORT, () => {
  console.log('');
  console.log('  ✅  Standby List server running');
  console.log(`  👉  Admin : http://localhost:${PORT}/admin.html`);
  console.log(`  👉  View  : http://localhost:${PORT}/view.html`);
  console.log('');
});
