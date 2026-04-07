# Skill: VCE Business Management Cheat Sheet Generator

## Purpose
Generate interactive HTML cheat sheets for VCE Business Management Units 3 & 4
using the Jacaranda Key Concepts 7th edition (Chapman, Phelan, Richardson, Rabenda, Smithies).
Each topic becomes a standalone `.html` file students can open in any browser.

---

## Key Difference from Accounting Skill

Business Management is NOT primarily a definitions subject.
The VCE exam tests students on:
- **Applying** concepts to unseen business case studies
- **Comparing** strategies, styles and approaches
- **Evaluating** effectiveness with justified recommendations
- **Discussing** advantages and disadvantages
- **Constructing** structured written responses using command terms

Therefore cheat sheets must include MORE than just term definitions. Every topic needs:
1. Key terms with plain English definitions (accordion — searchable)
2. Advantages / disadvantages panels for every strategy or approach
3. Comparison tables where concepts are commonly compared in exams
4. Model answer structures for common exam question types
5. Command term guidance (define vs explain vs discuss vs evaluate vs justify vs analyse vs distinguish vs recommend)

---

## Book Structure

**Unit 3 — Managing a Business**
| Topic | Title | Area of Study |
|-------|-------|---------------|
| Topic 1 | Business Foundations | AOS 1 |
| Topic 2 | Human Resource Management | AOS 2 |
| Topic 3 | Operations Management | AOS 3 |

**Unit 4 — Transforming a Business**
| Topic | Title | Area of Study |
|-------|-------|---------------|
| Topic 4 | Reviewing Performance — the Need for Change | AOS 1 |
| Topic 5 | Implementing Change | AOS 2 |

Each topic has numbered subtopics (e.g. 1.2, 1.3) rather than chapters.

---

## HTML Output Rules

### File format
- Single self-contained file: all CSS and JS inline, no external dependencies
- Open directly in any browser — no server required

### JavaScript rules (critical)
- Always use `var` — never `const` or `let`
- Never use template literals (backticks) — use string concatenation only
- Never use arrow functions — use `function` keyword or IIFE
- Use HTML entities for special characters:
  - `&#9660;` (▼), `&#9650;` (▲), `&#9658;` (▶)
  - `&#9733;` (★), `&#9888;` (⚠), `&#128161;` (💡), `&#10003;` (✓)
  - `&#43;` (+), `&#8722;` (−)
- **CRITICAL — data strings must use plain text, not HTML entities.** Write `'` not `&apos;`, `&` not `&amp;`, `—` not `&mdash;` inside JS data arrays. HTML entities inside JS strings break the search function because the regex matches the raw string before the browser decodes entities.

### CSS rules
- No CSS variables — hardcoded hex values only
- All font sizes must be in `em` units (not `px`) so the font-size toggle works correctly
- No `position: absolute` tooltips inside `overflow: hidden` containers
- Hot badge tooltips: `position: absolute; top: calc(100% + 6px)` — always drops DOWN

---

## Page Layout (apply to every file)

Every file must have these elements in this order:

```
1. <h1> title
2. <p class="subtitle"> subtitle
3. Font size toggle buttons
4. Search bar + result count + clear button
5. Section divider: "📚 Reference panels"
6. All collapsible box-wrap panels
7. Section divider: "🔍 Key terms"
8. No-results message div
9. <div id="list"> — accordion built by JS
10. Footer
```

### Font size toggle (include in every file)
Sits between the subtitle and search bar. Allows students to increase text size globally.

```html
<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
  <span style="font-size:0.79em;color:#5F5E5A;font-weight:600;">Text size:</span>
  <button onclick="setSize(14)" id="sz-s" style="padding:4px 11px;border-radius:6px;border:1.5px solid #D3D1C7;background:#fff;font-size:0.79em;cursor:pointer;font-weight:600;color:#1a1a18;">Default</button>
  <button onclick="setSize(17)" id="sz-m" style="padding:4px 11px;border-radius:6px;border:1.5px solid #D3D1C7;background:#fff;font-size:0.93em;cursor:pointer;font-weight:600;color:#1a1a18;">Large</button>
  <button onclick="setSize(20)" id="sz-l" style="padding:4px 11px;border-radius:6px;border:1.5px solid #D3D1C7;background:#fff;font-size:1.07em;cursor:pointer;font-weight:600;color:#1a1a18;">X-Large</button>
</div>
```

```javascript
function setSize(px) {
  document.body.style.fontSize = px + "px";
  var ids = ["sz-s","sz-m","sz-l"];
  var sizes = [14,17,20];
  for (var i = 0; i < ids.length; i++) {
    var btn = document.getElementById(ids[i]);
    if (sizes[i] === px) {
      btn.style.background = "#085041";
      btn.style.color = "#fff";
      btn.style.borderColor = "#085041";
    } else {
      btn.style.background = "#fff";
      btn.style.color = "#1a1a18";
      btn.style.borderColor = "#D3D1C7";
    }
  }
}
```

### Section dividers
Use these dark bars to clearly separate the two halves of the page.

```html
<!-- Before the reference panels -->
<div class="section-divider">&#128218; Reference panels <span>click any panel to expand</span></div>

<!-- Before the key terms accordion -->
<div class="section-divider">&#128269; Key terms <span>search above or click a section to expand</span></div>
```

```css
.section-divider {
  margin: 22px 0 14px;
  padding: 10px 14px;
  background: #1a1a18;
  color: #fff;
  border-radius: 8px;
  font-size: 0.93em;
  font-weight: 700;
  letter-spacing: 0.3px;
}
.section-divider span {
  font-weight: 400;
  opacity: 0.7;
  font-size: 0.9em;
  margin-left: 8px;
}
```

---

## Visual Design System

### Colour palette for accordion sections
| Class | Use for |
|-------|---------|
| purple | Intro/overview/foundations sections |
| teal | People management, positive strategies |
| coral | Risk, termination, negative concepts |
| amber | Operations, calculations, processes |
| blue | Change management, KPIs, performance |
| pink | Ethics, CSR, evaluation sections |
| gray | Definitions, principles, key terms |

### Collapsible panel style — CRITICAL UPDATE
**All panels must look identical when collapsed.** Do NOT use coloured backgrounds or borders on panel headers — this was too visually noisy. Use a plain white card with only a left-border accent to hint at category. Colour only appears inside the open panel body.

```css
.box-wrap {
  border-radius: 8px;
  margin-bottom: 8px;
  overflow: visible;
  border: 1px solid #D3D1C7;
  background: #fff;
  border-left: 4px solid #D3D1C7;  /* overridden per colour below */
}
.box-wrap.green  { border-left-color: #5DCAA5; }
.box-wrap.red    { border-left-color: #D85A30; }
.box-wrap.purple { border-left-color: #AFA9EC; }
.box-wrap.amber  { border-left-color: #BA7517; }
.box-wrap.blue   { border-left-color: #378ADD; }
.box-wrap.teal   { border-left-color: #5DCAA5; }
.box-wrap.pink   { border-left-color: #D4537E; }
.box-wrap.coral  { border-left-color: #D85A30; }
.box-wrap.gray   { border-left-color: #888780; }

/* ALL toggles are plain white — no coloured headers */
.box-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 11px 14px;
  cursor: pointer;
  user-select: none;
  font-size: 0.93em;
  font-weight: 700;
  color: #1a1a18;
  background: #fff;
  border-radius: 7px;
}
.box-toggle:hover { background: #F8F7F3; }

.box-body { display: none; border-top: 1px solid #EDECEA; }
.box-body.open { display: block; }
```

The left-border colour gives a subtle category signal without the noise of full tinted headers across every panel.

---

## Advantages / Disadvantages Panel — CRITICAL UPDATE

The old style used green and red background fills on the adv/dis cards, making text hard to read. Use white backgrounds with coloured borders and headings only:

```html
<div class="ad-grid">
  <div class="adv">
    <h3>&#43; Advantages</h3>
    <ul>
      <li>Advantage one — brief explanation of WHY</li>
      <li>Advantage two — brief explanation of WHY</li>
      <li>Advantage three — brief explanation of WHY</li>
    </ul>
  </div>
  <div class="dis">
    <h3>&#8722; Disadvantages</h3>
    <ul>
      <li>Disadvantage one — brief explanation of WHY</li>
      <li>Disadvantage two — brief explanation of WHY</li>
      <li>Disadvantage three — brief explanation of WHY</li>
    </ul>
  </div>
</div>
```

```css
.ad-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 12px; background: #fff; }
.ad-grid .adv { background: #fff; border: 1px solid #c8e8da; border-radius: 8px; padding: 12px; }
.ad-grid .dis { background: #fff; border: 1px solid #e8c4b8; border-radius: 8px; padding: 12px; }
.ad-grid h3 { font-size: 0.86em; font-weight: 700; margin-bottom: 7px; padding-bottom: 5px; border-bottom: 2px solid; }
.ad-grid .adv h3 { color: #085041; border-bottom-color: #5DCAA5; }
.ad-grid .dis h3 { color: #4A1B0C; border-bottom-color: #D85A30; }
.ad-grid ul { font-size: 0.79em; line-height: 1.8; padding-left: 15px; }
.ad-grid .adv ul, .ad-grid .dis ul { color: #1a1a18; }  /* dark text on white — readable */
@media(max-width:520px) { .ad-grid { grid-template-columns: 1fr; } }
```

**Key rule:** List text must be `color: #1a1a18` (near black) — never coloured text on white background. Heading colour is enough to signal positive/negative.

---

## Model Answer Panels — CRITICAL UPDATE

The old amber-filled model-step blocks were hard to read. Use white backgrounds with left-border accents only:

```css
.model-step {
  background: #fff;
  border: 1px solid #e8e0cc;
  border-left: 4px solid #BA7517;
  border-radius: 0 8px 8px 0;
  padding: 9px 12px;
  margin-bottom: 8px;
  font-size: 0.86em;
  line-height: 1.7;
  color: #1a1a18;
}
.model-step strong { color: #412402; }
.model-step.conclude {
  background: #fff;
  border: 1px solid #dddcf8;
  border-left: 4px solid #7F77DD;
}
.model-step.conclude strong { color: #26215C; }
```

Sample question banner inside model answer panel — also white:
```html
<div style="background:#fff;border:1px solid #BA7517;border-left:4px solid #BA7517;border-radius:0 8px 8px 0;padding:10px 12px;margin-bottom:12px">
  <p style="font-size:0.86em;font-weight:700;color:#412402">Sample question: ...</p>
</div>
```

---

## Maslow Hierarchy Bars — CRITICAL UPDATE

The original solid-colour bars (red, orange, amber, green) were too harsh. Use muted pastels with dark text:

```html
<div class="level-bar" style="background:#d9c4f0;color:#2e1a4a;width:100%">5. Self-actualisation — reaching full potential, creativity, meaningful work</div>
<div class="level-bar" style="background:#b8d4f0;color:#1a2e4a;width:90%">4. Esteem — recognition, status, achievement, respect from others</div>
<div class="level-bar" style="background:#a8dbc8;color:#0d3326;width:80%">3. Social — belonging, friendship, teamwork, acceptance</div>
<div class="level-bar" style="background:#f0d9a8;color:#3d2600;width:70%">2. Safety — job security, safe working conditions, stable income</div>
<div class="level-bar" style="background:#f0c4b0;color:#3d1200;width:60%">1. Physiological — basic pay, food, shelter, rest</div>
```

Use dark text (`color: #2e1a4a` etc.) not white — much more readable on pastel backgrounds.

---

## Search Function — CRITICAL (full implementation required)

The search must be fully implemented with highlight, result count, clear button, and auto-expand on match. Do NOT use a simplified version. The following pattern is required in every file:

### Data array rules
- All strings must be plain text — no HTML entities (`'` not `&apos;`, `&` not `&amp;`)
- Fields: `term`, `def`, `eg` (required), `note` (optional)
- Categories start **collapsed** by default; search auto-expands matching sections

### Search HTML
```html
<input id="search" type="text" placeholder="&#128269; Search terms..." oninput="filterTerms(this.value)">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;min-height:18px;">
  <span id="search-count" style="font-size:0.82em;color:#5F5E5A;"></span>
  <button id="search-clear" onclick="clearSearch()" style="display:none;padding:2px 10px;border-radius:5px;border:1px solid #D3D1C7;background:#fff;font-size:0.82em;cursor:pointer;color:#1a1a18;">&#10005; Clear</button>
</div>
```

### Full JS implementation (include verbatim)

```javascript
function highlight(text, q) {
  if (!q) return text;
  var escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return text.replace(new RegExp('(' + escaped + ')', 'gi'), '<mark style="background:#ffe066;border-radius:2px;padding:0 1px;">$1</mark>');
}

function build(source, q) {
  var list = document.getElementById("list");
  var noRes = document.getElementById("no-results");
  list.innerHTML = "";
  var totalFound = 0;
  var isSearching = q && q.length > 0;
  for (var i = 0; i < source.length; i++) {
    var cat = source[i];
    if (!cat.items.length) continue;
    totalFound += cat.items.length;
    var div = document.createElement("div");
    div.className = "cat " + cat.color;
    var badge = cat.hot ? '<span class="hot-badge">&#9733; HOT TOPIC<span class="tip">High-frequency exam topic</span></span>' : "";
    var head = document.createElement("div");
    head.className = "cat-head";
    var catLabel = isSearching ? highlight(cat.cat, q) : cat.cat;
    head.innerHTML = '<span class="cat-head-text">' + catLabel + '</span><div class="cat-head-right">' + badge + '<small>' + cat.items.length + ' terms</small><span class="cat-arrow">' + (isSearching ? '&#9660;' : '&#9658;') + '</span></div>';
    (function(d, h) {
      h.onclick = function() {
        var b = d.querySelector(".cat-body");
        var a = h.querySelector(".cat-arrow");
        var c = b.classList.toggle("collapsed");
        a.innerHTML = c ? "&#9658;" : "&#9660;";
      };
    })(div, head);
    div.appendChild(head);
    var body = document.createElement("div");
    body.className = isSearching ? "cat-body" : "cat-body collapsed";
    for (var j = 0; j < cat.items.length; j++) {
      var item = cat.items[j];
      var t = document.createElement("div");
      t.className = "term";
      var termText = isSearching ? highlight(item.term, q) : item.term;
      var defText  = isSearching ? highlight(item.def,  q) : item.def;
      var egText   = isSearching ? highlight(item.eg || "", q) : (item.eg || "");
      var note = item.note ? '<span class="term-note">&#9888; Exam tip: ' + (isSearching ? highlight(item.note, q) : item.note) + '</span>' : "";
      t.innerHTML = '<div class="term-title" onclick="toggle(this)"><span>' + termText + '</span><span class="arrow">&#9660;</span></div>'
        + '<div class="term-body' + (isSearching ? ' open' : '') + '"><p class="term-def">' + defText + '</p>'
        + '<span class="term-eg">Eg: ' + egText + '</span>' + note + '</div>';
      body.appendChild(t);
    }
    div.appendChild(body);
    list.appendChild(div);
  }
  if (noRes) noRes.style.display = (totalFound === 0 && isSearching) ? "block" : "none";
}

function filterTerms(q) {
  q = q.trim();
  var ql = q.toLowerCase();
  var countEl = document.getElementById("search-count");
  var clearBtn = document.getElementById("search-clear");
  clearBtn.style.display = q ? "inline-block" : "none";
  var filtered = [];
  for (var i = 0; i < data.length; i++) {
    var cat = data[i];
    var items = [];
    for (var j = 0; j < cat.items.length; j++) {
      var item = cat.items[j];
      if (!q || item.term.toLowerCase().indexOf(ql) > -1
              || item.def.toLowerCase().indexOf(ql) > -1
              || (item.eg && item.eg.toLowerCase().indexOf(ql) > -1)) {
        items.push(item);
      }
    }
    if (items.length) filtered.push({ cat: cat.cat, color: cat.color, hot: cat.hot, items: items });
  }
  build(filtered, q);
  if (q) {
    var total = 0;
    for (var k = 0; k < filtered.length; k++) total += filtered[k].items.length;
    countEl.textContent = total + " result" + (total !== 1 ? "s" : "");
  } else {
    countEl.textContent = "";
  }
}

function clearSearch() {
  document.getElementById("search").value = "";
  document.getElementById("search-count").textContent = "";
  document.getElementById("search-clear").style.display = "none";
  build(data, "");
}

function toggle(el) {
  var body = el.nextElementSibling;
  var arr = el.querySelector(".arrow");
  var open = body.classList.toggle("open");
  arr.innerHTML = open ? "&#9650;" : "&#9660;";
}

function toggleB(el) {
  var body = el.nextElementSibling;
  var arr = el.querySelector(".cat-arrow");
  var open = body.classList.toggle("open");
  arr.innerHTML = open ? "&#9650;" : "&#9660;";
}

build(data, "");
```

**Key behaviours:**
- Categories start **collapsed** on page load (`cat-body collapsed`)
- When searching: matching categories expand automatically, matching text is highlighted in yellow
- Category header text is also highlighted if the search term appears in it
- Clear button appears when search is active, resets everything
- Result count shown below search bar

---

## Command Terms — Full List (UPDATED)

The command terms panel must include all terms confirmed in the VCE study design. The original list was missing four important terms. Always use this complete list:

| Command term | What it means | Marks typically |
|---|---|---|
| Define | State the precise meaning of a term | 1–2 |
| Outline | Give a brief overview of the main points — less detail than describe | 1–2 |
| Describe | Give a detailed account of characteristics or features | 2–3 |
| Explain | Make clear how or why — give reasons | 2–4 |
| Analyse | Break a concept into its parts and examine how they relate or contribute to the whole — go beyond description to show cause and effect | 3–6 |
| Distinguish | Clearly identify the differences between two concepts — focus on contrast, not similarities | 2–4 |
| Compare | Show similarities AND differences between two things | 3–6 |
| Discuss | Give BOTH sides — advantages AND disadvantages | 4–6 |
| Evaluate | Discuss both sides AND make a judgement with justification | 6–10 |
| Justify | Give reasons that support a decision or recommendation | 3–6 |
| Propose | Put forward a strategy or solution with reasons | 3–5 |
| Recommend | Suggest the best course of action and explain why it is the most appropriate choice for the given situation | 3–5 |

**Updated box-note:** `Discuss = both sides. Evaluate = both sides + judgement. Analyse = causes/effects/relationships, not just description. Distinguish = differences only, not similarities.`

---

## Comparison Tables in Panels

Where a table sits inside a collapsible panel, wrap it in `<div style="overflow-x:auto;padding:12px">` to handle narrow screens. Table header background depends on category:

```css
table.ct th               { background: #3C3489; }   /* default purple */
table.ct.teal-head th     { background: #085041; }
table.ct.coral-head th    { background: #4A1B0C; }
table.ct.amber-head th    { background: #412402; }
```

All `td` cells must have `text-align: left` — never rely on browser defaults.

---

## Page Structure — Full CSS Reference

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #F5F4F0; color: #1a1a18; padding: 16px; font-size: 14px; }

/* All font sizes in em so font-size toggle works */
h1 { font-size: 1.57em; font-weight: 700; color: #085041; margin-bottom: 4px; }
.subtitle { font-size: 0.93em; color: #5F5E5A; margin-bottom: 14px; }
#search { width: 100%; padding: 9px 14px; border: 1.5px solid #D3D1C7; border-radius: 8px; font-size: 1em; outline: none; background: #fff; margin-bottom: 6px; }
#search:focus { border-color: #1D9E75; }

/* Accordion */
.cat { border-radius: 10px; margin-bottom: 10px; overflow: hidden; border: 1.5px solid; }
.cat.purple { border-color: #AFA9EC; background: rgba(206,203,246,0.18); }
.cat.teal   { border-color: #5DCAA5; background: rgba(159,225,203,0.15); }
.cat.coral  { border-color: #D85A30; background: rgba(240,153,123,0.12); }
.cat.amber  { border-color: #BA7517; background: rgba(239,159,39,0.12);  }
.cat.blue   { border-color: #378ADD; background: rgba(133,183,235,0.12); }
.cat.pink   { border-color: #D4537E; background: rgba(237,147,177,0.12); }
.cat.gray   { border-color: #888780; background: rgba(180,178,169,0.12); }

.cat-head { display: flex; justify-content: space-between; align-items: center; padding: 11px 14px; cursor: pointer; user-select: none; }
.cat.purple .cat-head { background: rgba(206,203,246,0.35); }
.cat.teal   .cat-head { background: rgba(159,225,203,0.30); }
.cat.coral  .cat-head { background: rgba(240,153,123,0.25); }
.cat.amber  .cat-head { background: rgba(239,159,39,0.22);  }
.cat.blue   .cat-head { background: rgba(133,183,235,0.25); }
.cat.pink   .cat-head { background: rgba(237,147,177,0.22); }
.cat.gray   .cat-head { background: rgba(180,178,169,0.22); }

.cat-head-text { font-size: 0.93em; font-weight: 700; color: #1a1a18; }
.cat-head-right { display: flex; align-items: center; gap: 8px; }
.cat-head-right small { font-size: 0.79em; color: #5F5E5A; }
.cat-arrow { font-size: 0.79em; color: #5F5E5A; }
.cat-body { padding: 0 10px 10px; }
.cat-body.collapsed { display: none; }

.term { border-radius: 7px; margin-top: 7px; background: #fff; border: 1px solid #E5E3DC; overflow: hidden; }
.term-title { display: flex; justify-content: space-between; align-items: center; padding: 9px 12px; cursor: pointer; font-size: 0.93em; font-weight: 600; color: #1a1a18; }
.term-title:hover { background: #F8F7F3; }
.arrow { font-size: 0.71em; color: #888780; }
.term-body { display: none; padding: 10px 12px; border-top: 1px solid #EDECEA; background: #FAFAF8; }
.term-body.open { display: block; }
.term-def { font-size: 0.86em; line-height: 1.65; color: #2C2C2A; margin-bottom: 6px; }
.term-eg { display: block; font-size: 0.79em; color: #085041; background: #E1F5EE; border-radius: 5px; padding: 5px 8px; margin-top: 4px; }
.term-note { display: block; font-size: 0.79em; color: #412402; background: #FAEEDA; border-left: 3px solid #BA7517; border-radius: 0 5px 5px 0; padding: 5px 8px; margin-top: 6px; font-style: italic; }

/* Hot badge — colour is RED for Bus Man (unlike PE which uses teal) */
.hot-badge { position: relative; display: inline-flex; align-items: center; background: #E24B4A; color: #fff; font-size: 0.71em; font-weight: 700; border-radius: 5px; padding: 2px 7px; cursor: help; white-space: nowrap; margin-right: 4px; }
.hot-badge .tip { display: none; position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%); background: #501313; color: #fff; font-size: 0.79em; border-radius: 6px; padding: 5px 9px; width: 210px; text-align: center; line-height: 1.4; z-index: 50; pointer-events: none; }
.hot-badge:hover .tip { display: block; }

/* Search highlight */
mark { background: #ffe066; border-radius: 2px; padding: 0 1px; }

/* Box wraps — see panel style section above */
.box-note { font-size: 0.79em; color: #412402; background: #FAEEDA; border-left: 3px solid #BA7517; border-radius: 0 5px 5px 0; padding: 6px 10px; margin: 10px 12px 12px; font-style: italic; }
.panel-section-title { font-size: 0.86em; font-weight: 700; color: #26215C; margin: 14px 12px 4px; border-bottom: 1px solid #D3D1C7; padding-bottom: 4px; }

/* Tables */
table.ct { width: 100%; border-collapse: collapse; font-size: 0.86em; }
table.ct th { background: #3C3489; color: #fff; padding: 7px 10px; text-align: left; font-size: 0.93em; font-weight: 700; }
table.ct td { padding: 7px 10px; border-bottom: 1px solid #EDECEA; vertical-align: top; line-height: 1.55; text-align: left; }
table.ct tr:nth-child(even) td { background: #F8F7F3; }
table.ct tr:last-child td { border-bottom: none; }
table.ct.teal-head th  { background: #085041; }
table.ct.coral-head th { background: #4A1B0C; }
table.ct.amber-head th { background: #412402; }

/* Tags */
.tag { display: inline-block; font-size: 0.71em; font-weight: 700; border-radius: 4px; padding: 1px 5px; margin-right: 3px; }
.tag-g { background: #E1F5EE; color: #085041; }
.tag-r { background: #FAECE7; color: #4A1B0C; }
.tag-p { background: #EEEDFE; color: #26215C; }
.tag-a { background: #FAEEDA; color: #412402; }

.footer { text-align: center; font-size: 0.79em; color: #888780; margin-top: 28px; padding-top: 12px; border-top: 1px solid #D3D1C7; }
```

---

## Content Guidelines

### Definitions
- Plain English — one or two sentences maximum
- Always state what the term IS, not just what it does
- No HTML entities in JS data strings (see JavaScript rules above)

### Examples
- Always use real or realistic Australian business scenarios
- Reference well-known Australian businesses:
  - Manufacturing: Toyota, Qantas, Bega Cheese
  - Service: Commonwealth Bank, Medibank, Linfox
  - Retail: Woolworths, JB Hi-Fi, Bunnings
  - Small business: local cafe, boutique retailer, trades business

### Advantages / Disadvantages
- Always 3 advantages and 3 disadvantages minimum
- Each point must be a full sentence including WHY it is an advantage/disadvantage
- Never single words (e.g. "Costly" → "High implementation costs reduce business profitability")
- List text must be `color: #1a1a18` — not coloured — for readability on white background

### Short-term vs long-term motivation effects
- When covering motivation strategies, always include whether the strategy produces short-term or long-term motivation effects
- General rule: financial strategies (bonuses, pay) = short-term; non-financial strategies (career advancement, job enrichment) = long-term
- Add a "Short or long-term?" column to motivation strategy tables

### Model answer structures
- Include for any concept commonly asked as discuss/evaluate
- Always: Define → Advantage → Disadvantage → Conclusion (evaluate/justify only)
- Use white background with amber left-border accent for steps (not amber fill)
- Conclusion step uses purple left-border accent (`.model-step.conclude`)

### Exam tips (note field)
- Focus on common exam mistakes:
  - "Always link your answer back to the business in the case study"
  - "Discuss requires BOTH advantages and disadvantages — not just one side"
  - "Evaluate requires a conclusion/judgement — not just discussion"
  - "Analyse means cause and effect, not just description"
  - "Distinguish means differences only — do not list similarities"

---

## Hot Topics by Topic (confirmed high-frequency exam areas)

| Topic | Hot subtopics |
|-------|--------------|
| Topic 1 | Management styles, Management skills, Corporate culture, Stakeholders |
| Topic 2 | Motivation theories (Maslow, Locke, Lawrence & Nohria), Training types, Performance management, Termination, Workplace participants, Dispute resolution |
| Topic 3 | Operations strategies, Quality management, Technology & automation, CSR in operations |
| Topic 4 | Key Performance Indicators (KPIs), Forces for change, SWOT analysis |
| Topic 5 | Leadership styles (Lewin), Strategies to overcome resistance, Kotter 8-step model, Learning organisation |

---

## Topic 2 Coverage Checklist (confirmed complete)

Before finalising any Topic 2 file, verify all key knowledge areas are covered:

- [ ] Relationship between HRM and business objectives
- [ ] Maslow's Hierarchy of Needs — five levels, management application
- [ ] Locke & Latham's Goal-Setting Theory — SCCEA principles
- [ ] Lawrence & Nohria's Four Drive Theory — all four drives, no hierarchy
- [ ] Comparison table: all three theories side by side
- [ ] Financial motivation strategies (remuneration, performance-related pay, profit sharing, share ownership) — adv/dis + short/long-term column
- [ ] Non-financial motivation strategies (recognition, job enrichment, career advancement, training, flexible work) — adv/dis + short/long-term column
- [ ] **Support strategies** (EAP, mentoring, wellness programs) — adv/dis
- [ ] **Sanction strategies** (verbal warning, written warning, demotion, dismissal as sanction) — adv/dis
- [ ] On-the-job training — adv/dis
- [ ] Off-the-job training — adv/dis
- [ ] Online/e-learning training — adv/dis
- [ ] Training comparison table (on/off/online)
- [ ] Performance management: MBO, appraisals, self-evaluation, employee observation — adv/dis
- [ ] Termination types: resignation, retirement, redundancy, dismissal (general), summary dismissal
- [ ] Unfair vs wrongful dismissal
- [ ] Entitlement obligations (Fair Work Act, NES)
- [ ] **Transition considerations** (outplacement, references, handover, exit interviews)
- [ ] **Workplace participants**: HR managers, employees, employer associations, unions, Fair Work Commission
- [ ] **Modern Awards** — what they set, who they cover
- [ ] **Enterprise Agreements** — BOOT, adv/dis
- [ ] **National Employment Standards (NES)** — 10 minimum conditions, cannot be excluded
- [ ] **Dispute resolution process**: direct negotiation → grievance → conciliation → arbitration
- [ ] **Mediation vs arbitration** distinction (voluntary agreement vs binding decision)

---

## Recommended Panel Structure per Topic

Always include these panels in this order:
1. **Font size toggle** — above search bar, every file
2. **Section divider** — "Reference panels"
3. **Command terms panel** (blue, all 12 terms) — every file
4. **Theory/concept panels** — comparison tables, adv/dis grids, worked examples
5. **Model answer panels** (amber) — for likely discuss/evaluate questions
6. **Section divider** — "Key terms"
7. **Key terms accordion** — all subtopic definitions, starts collapsed

---

## Known Issues & Fixes Applied

| Issue | Fix |
|-------|-----|
| Font size toggle had no effect | All CSS font sizes must be `em` not `px` — `em` scales from `body`, `px` ignores it |
| Search not finding terms with apostrophes (e.g. "Maslow's") | Data strings must use plain `'` not `&apos;` — HTML entities inside JS strings are not decoded before regex matching |
| Search appeared to do nothing | Categories were rendering without `collapsed` class — all looked open already. Fix: initial `build(data, "")` renders with `cat-body collapsed`; search renders with `cat-body` (no collapsed) and terms auto-open |
| Coloured panel headers too visually noisy | Replaced all coloured `box-toggle` backgrounds with plain white — colour only appears as left-border accent |
| Adv/dis cards hard to read | Replaced green/red background fills with white cards + coloured border + coloured heading underline only; list text is always `#1a1a18` |
| Maslow bars too harsh | Replaced solid saturated colours with muted pastels + dark text |
| Model answer steps hard to read | Replaced amber fill with white + left-border accent only |
| Command terms incomplete | Added: Outline, Analyse, Distinguish, Recommend |
| Topic 2 missing key knowledge areas | Added: support strategies, sanction strategies, transition considerations, workplace participants (employer associations, unions, FWC), modern awards, enterprise agreements (BOOT), NES, dispute resolution process, mediation vs arbitration |

---

## Prompt to Activate This Skill in a New Conversation

Paste the following at the start of a new chat, then attach this updated skill document:

> "I am creating interactive HTML cheat sheets for VCE Business Management Units 3 & 4 using the Jacaranda Key Concepts 7th edition textbook. Please use the attached skill document to generate each topic. Follow ALL rules and patterns in the skill exactly — particularly the CSS font-size em units, the plain-text data strings (no HTML entities), the full search implementation, the white panel headers (colour as left-border only), white adv/dis cards, white model-step backgrounds, and the two section dividers. I will give you the topic number and title. Identify hot topics, include all required panels, and produce a complete HTML file."
