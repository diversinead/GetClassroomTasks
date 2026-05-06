# Skill: VCE Physical Education — Study Notes & Quiz Generator

## Purpose
Generate two paired interactive HTML files per chapter section for VCE Physical Education Units 1 & 2 using the **Live it Up 5th edition** textbook.

- **File 1: Study Notes** — collapsible "Chapter contents" / "Reference panels" sections, SVG diagrams, reference tables, textbook image lightbox buttons, and a key terms accordion with search
- **File 2: Quiz & Exam Practice** — tabbed file with an interactive quiz (multiple choice, true/false, matching) and exam practice questions (short answer + extended response) with model answers

Each file is fully self-contained HTML — all CSS and JS inline, no external dependencies. Files are served by a Python http.server (`server.py`) which automatically injects a small "← Back to notes" toolbar at the top of every file.

---

## File Naming Convention

| File | Naming pattern | Example |
|------|---------------|---------|
| Study notes | `vce_pe_u[unit]_[aos]_ch[chapter]_part[X]_[topic].html` | `vce_pe_u1_aos1a_ch1_partA_skeletal.html` |
| Quiz | `vce_pe_u[unit]_[aos]_ch[chapter]_part[X]_quiz.html` | `vce_pe_u1_aos1a_ch1_partA_quiz.html` |

Each chapter is split into logical **Parts** of 2–4 textbook sections each. Never put more than ~4 sections in one file.

---

## Course Structure Reference

### Unit 1: The Human Body in Motion
- **AOS1a:** How does the musculoskeletal system work to produce movement
  - Ch1: The Musculoskeletal System
  - Ch2: Musculoskeletal Injuries, Illnesses and Safeguards
- **AOS1b:** Performance Enhancement methods of the MS System
- **AOS2:** How does the cardiorespiratory system function at rest and during physical activity
  - Ch3: The Cardiovascular System
  - Ch4: The Respiratory System
  - Ch5: Improving the Cardiorespiratory System

### Unit 2: Physical Activity, Sport & Society
- **AOS1:** What are the relationships between physical activity, sport, health & society
- **AOS2:** What are the contemporary issues associated with physical activity and sport

---

## JavaScript Rules (critical — do not deviate)

- Always use `var` — NEVER `const` or `let`
- Never use template literals (backticks) — use string concatenation only
- Never use arrow functions — use `function` keyword or IIFE
- Use HTML entities for special characters: `&#9660;` (▼), `&#9650;` (▲), `&#9658;` (▶), `&#9733;` (★), `&#9888;` (⚠), `&#128161;` (💡), `&#10003;` (✓), `&#128247;` (📷), `&#128218;` (📚), `&#128269;` (🔍)
- Avoid apostrophes inside JS strings — rephrase to avoid or use `&apos;`
- **Never use `scrollTo` as a function name** — conflicts with `window.scrollTo`. Use `jumpTo` instead
- **Never name anything that shadows a built-in** — check before naming functions

---

## CSS Rules

- No CSS variables — use hardcoded hex values only
- All table `td` cells must have `text-align: left` set explicitly in CSS — do NOT rely on browser defaults
- Body uses **Georgia serif** font for PE (subject-distinctive)
- Hot badge tooltips use `position: absolute; top: calc(100% + 6px)` (drops DOWN) — never upward
- `diagram-body` default is `display: none` — opened via `toggleB()`
- `box-body` default is `display: none` — opened via `toggleB()`
- `cat-body` default is `display: none` (collapsed); add `.open` class to expand
- All panel headers (`.box-toggle`, `.diagram-head`, `.cat-head`) use **plain white background** with `:hover { background: #F8F7F3 }` — colour appears only as 4px left-border accent on the wrapping div
- All SVG diagrams have a `style="max-width:Xpx;width:100%;display:inline-block;"` attribute to prevent over-stretching on wide screens; typical max-width is 720–880px

---

## Page Header & Title Hierarchy

The top of every study notes file follows this structure:

```html
<h1>VCE PHYSICAL EDUCATION &middot; UNIT 1 AOS1a</h1>           <!-- small grey uppercase -->
<p class="chapter-title">Chapter 1 (1.1 &amp; 1.2) &mdash; Overview &amp; The Skeletal System</p>   <!-- big green -->
<p class="subtitle">Live it Up 5th ed.</p>                       <!-- small italic -->

<div class="size-row">...</div>                                  <!-- text-size toggle, left-aligned -->
<div class="search-wrap">...</div>                               <!-- search input, full width -->

<div class="section-divider">&#128218; Chapter contents</div>    <!-- black bar -->
<!-- ... section panels ... -->

<div class="section-divider" id="secTerms">&#128269; Key terms <span style="font-weight:400;opacity:0.7;font-size:0.9em;margin-left:8px;">search above or click a section to expand</span></div>
<div id="list"></div>
<div id="no-results">No matching terms found.</div>
```

```css
h1 { text-align: center; font-size: 0.79em; font-weight: 600; color: #5F5E5A; margin-bottom: 2px; letter-spacing: 0.4px; text-transform: uppercase; }
.chapter-title { text-align: center; font-size: 1.43em; font-weight: 700; color: #085041; margin-bottom: 4px; letter-spacing: -0.3px; }
.subtitle { text-align: center; color: #5F5E5A; font-size: 0.86em; margin-bottom: 14px; font-style: italic; }
```

**Do NOT use** the old gradient-banner h1 (`linear-gradient(135deg, #2c5f6e, #1a3d48)`) or the dark teal subtitle banner. These have been removed everywhere. New files start with the muted green palette below.

---

## Section Dividers

Two types of horizontal divider exist:

1. **`.section-divider`** — solid black bar, used to separate **major page regions**:
   - `📚 Chapter contents` (or `📚 Reference panels` for sections without textbook section numbers)
   - `🔍 Key terms` (always at the boundary between section panels and the searchable accordion)

   ```css
   .section-divider { font-size: 0.93em; font-weight: 700; color: #fff; background: #1a1a18;
     border-radius: 8px; padding: 10px 14px; margin: 22px 0 14px; letter-spacing: 0.3px; }
   ```

2. **`.section-label`** — subtle centred uppercase grey, used **only for in-panel sub-headings** (rare). Do NOT use this as a section header above a panel — sections are themselves panels and put the section title in the panel header.

   ```css
   .section-label { text-align: center; font-size: 0.75em; font-weight: 700;
     letter-spacing: 2px; text-transform: uppercase; color: #aaa; padding: 14px 0 4px; }
   ```

### When to use Chapter contents vs Reference panels

- **Chapter contents** — when the panels below correspond to numbered textbook sections (e.g. `1.1`, `1.2.1`, `2.4.1`). Section numbers appear in each panel header.
- **Reference panels** — when the panels below cover the chapter's content but do NOT have textbook section numbers (e.g. ch2 Part B `Fitness Requirements / Warm-up / Cool-down / Rehabilitation`, ch2 Part C `Equipment / Taping / Concussion`). Each panel just shows its topic title.

A single file uses only one of the two — never both.

---

## Section Panels (the new structure)

Every textbook section becomes a single expandable panel. The section title (with emoji + section number where applicable) is the **panel header text** — NOT a separate `<p class="section-label">` above the panel.

### Single-panel section (the common case)

```html
<div class="diagram-wrap blue" id="sec11">
  <div class="diagram-head blue" onclick="toggleB(this)">
    <span>&#128200; 1.1 Overview of the Musculoskeletal System</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="diagram-body">
    <!-- SVG, table, text content -->
  </div>
</div>
```

Use `.diagram-wrap` when the panel's main content is a diagram/SVG; use `.box-wrap` for tabular/text content. Both panel types are visually identical (white card, coloured left-border accent) — the class names are just semantic.

### Section with multiple inner panels (e.g. 1.2.5 with both a comparison table AND a diagram)

Wrap both inner panels in an outer panel whose header is the section title:

```html
<div class="box-wrap teal" id="sec125">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128279; 1.2.5 Types of Joints</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div class="box-wrap teal">
      <div class="box-toggle" onclick="toggleB(this)">
        <span>&#128202; Three Categories of Joint &mdash; Overview</span>
        <span class="cat-arrow">&#9660;</span>
      </div>
      <div class="box-body">[table]</div>
    </div>
    <div class="diagram-wrap purple">
      <div class="diagram-head purple" onclick="toggleB(this)">
        <span>&#128202; Six Types of Synovial Joint</span>
        <span class="cat-arrow">&#9660;</span>
      </div>
      <div class="diagram-body">[SVG]</div>
    </div>
  </div>
</div>
```

### Critical: do NOT add `<p class="section-label" id="secXXX">…</p>` above panels

This was the old pattern and produced an ugly subtle grey label sitting above every panel. The current pattern moves that label INTO the panel header, and the `id` attribute moves onto the wrapping div. Anchor links / nav still work because the wrap div carries the id.

### No more nav-pills

The old top-of-file `<div class="nav-pills">…</div>` quick-jump row is removed. Section panels are clearly labelled and listed under "Chapter contents" so the pills became redundant.

---

## Colour Palette

### Body / page chrome

```css
body { background: #F5F4F0; color: #1a1a18; font-family: Georgia, serif; font-size: 14px;
       line-height: 1.55; padding: 16px; }
```

### Section panel border-left accents

| Class modifier | Border-left colour | Use for |
|----------------|-------------------|---------|
| `.blue`   | `#378ADD` | Overview, skeletal system, general reference |
| `.purple` | `#AFA9EC` | Joint types, comparison tables, intro panels |
| `.teal`   | `#5DCAA5` | Muscular system, joints by category, positive concepts |
| `.amber`  | `#BA7517` | Vertebral column, formulas, calculations |
| `.coral`  | `#D85A30` | Movement terminology, injury content |
| `.pink`   | `#D4537E` | Fibre types, evaluation, ethics |
| `.green`  | `#5DCAA5` | Positive movement concepts (alias for teal) |
| `.gray`   | `#888780` | Definitions, principles, terminology |

The same colour set applies to `.box-wrap.X`, `.diagram-wrap.X`, and `.cat-wrap.X`.

```css
.box-wrap, .diagram-wrap, .cat-wrap {
  border-radius: 8px; margin-bottom: 8px;
  border: 1px solid #D3D1C7; background: #fff;
  border-left: 4px solid #D3D1C7; overflow: visible;
}
.box-wrap.blue, .diagram-wrap.blue, .cat-wrap.blue { border-left-color: #378ADD; }
.box-wrap.teal, .diagram-wrap.teal, .cat-wrap.teal { border-left-color: #5DCAA5; }
/* ... etc for all colours ... */
```

### Panel headers (always white)

```css
.box-toggle, .diagram-head, .cat-head, .box-head {
  background: #fff; color: #1a1a18; padding: 11px 14px; cursor: pointer;
  font-weight: 700; font-size: 0.93em; border-radius: 7px;
  display: flex; justify-content: space-between; align-items: center;
}
.box-toggle:hover, .diagram-head:hover, .cat-head:hover, .box-head:hover { background: #F8F7F3; }
```

NEVER apply colour to panel header backgrounds. The colour appears only as the left-border accent on the wrapping div.

### Hot Topic badge — red, right-aligned

```css
.hot-badge {
  display: inline-block; background: #E24B4A; color: #fff;
  font-size: 0.7em; font-weight: 700; border-radius: 10px; padding: 2px 8px;
  margin-left: auto;            /* pushes badge to right edge of flex header */
  position: relative; cursor: default;
  letter-spacing: 0.4px; white-space: nowrap;
}
.hot-badge .tooltip { display: none; position: absolute; top: calc(100% + 6px); left: 50%;
  transform: translateX(-50%); background: #501313; color: #fff; font-size: 0.79em;
  border-radius: 6px; padding: 5px 9px; width: 200px; text-align: center; line-height: 1.4;
  z-index: 50; pointer-events: none; }
.hot-badge:hover .tooltip { display: block; }
```

Render order in the panel header is `<span>title</span> <hot-badge> <span>arrow</span>`. The `margin-left: auto` on `.hot-badge` makes it sit hard against the arrow on the right.

### Permitted / Prohibited pills (ch2 Part D only) — coloured, anchored next to title

```css
.pill-permitted  { display: inline-block; background: #eafaf1; color: #1a7a58;
  border: 1px solid #9adcc5; border-radius: 12px; padding: 2px 10px;
  font-size: 0.78em; font-weight: 700;
  margin-left: 8px; margin-right: auto;       /* sticks next to title in flex header */
  white-space: nowrap; }
.pill-prohibited { display: inline-block; background: #fdf5f8; color: #8b2050;
  border: 1px solid #e096b4; border-radius: 12px; padding: 2px 10px;
  font-size: 0.78em; font-weight: 700;
  margin-left: 8px; margin-right: auto;
  white-space: nowrap; }
```

`margin-right: auto` on the pill absorbs flex space to its right so the pill stays close to the section title. If there's also a hot-badge in the header, the hot-badge's `margin-left: auto` pulls it to the far right, leaving the empty space between pill and hot-badge.

### Highlight on search match

```css
.hl, mark { background: #ffe066; border-radius: 2px; padding: 0 1px; }
```

---

## Search — both Key Terms AND Chapter Section Panels

The search bar searches both:
1. The Key Terms accordion (term, definition, example, exam tip)
2. The visible text inside every Chapter section panel — auto-expanding panels with matches and highlighting matched text yellow

### Required JS (verbatim)

```javascript
// ===== Key Terms search =====
function highlight(text, q) {
  if (!q) return text;
  var re = new RegExp("(" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
  return text.replace(re, '<span class="hl">$1</span>');
}

function build(source, q) {
  /* renders the Key Terms accordion. When q is non-empty, .cat-body has 'open' class
     (auto-expanded) and arrow is ▲; when q is empty, body is collapsed and arrow ▼.
     See full implementation in vce_pe_ch1_partA_skeletal.html. */
}

// ===== Chapter-section search =====
var sectionIndex = null;
var autoExpandedSections = [];

function buildSectionIndex() {
  if (sectionIndex !== null) return sectionIndex;
  sectionIndex = [];
  var els = document.querySelectorAll('[id^="sec"]');
  for (var i = 0; i < els.length; i++) {
    var el = els[i];
    if (!/^sec\d/.test(el.id)) continue;
    var body = el.querySelector('.box-body, .diagram-body');
    if (!body) continue;
    sectionIndex.push({
      id: el.id, el: el, body: body,
      arrow: el.querySelector('.cat-arrow'),
      text: (body.textContent || '').toLowerCase()
    });
  }
  return sectionIndex;
}

function highlightSectionText(root, re) {
  /* DOM walker: wraps matching text nodes in <span class="hl">.
     SKIPS text inside <svg> (different namespace) and inside existing .hl spans. */
}

function clearSectionHighlights(root) {
  /* unwrap span.hl nodes back to plain text, then root.normalize() */
}

function applySectionSearch(q) {
  // Close previously auto-expanded sections; clear their highlights
  for (var i = 0; i < autoExpandedSections.length; i++) {
    var s = autoExpandedSections[i];
    s.body.classList.remove('open');
    if (s.arrow) s.arrow.innerHTML = '&#9660;';
    clearSectionHighlights(s.body);
  }
  autoExpandedSections = [];
  if (!q) return 0;
  var sections = buildSectionIndex();
  var ql = q.toLowerCase();
  var re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  var count = 0;
  for (var i = 0; i < sections.length; i++) {
    var sec = sections[i];
    if (sec.text.indexOf(ql) > -1) {
      sec.body.classList.add('open');
      if (sec.arrow) sec.arrow.innerHTML = '&#9650;';
      highlightSectionText(sec.body, re);
      autoExpandedSections.push(sec);
      count++;
    }
  }
  return count;
}

function doSearch(q) {
  q = q.trim();
  document.getElementById("search-clear").className = q ? "visible" : "";
  var countEl = document.getElementById("search-count");
  if (!q) { build(data, ""); applySectionSearch(""); countEl.textContent = ""; return; }
  /* ... filter Key Terms data array ... */
  var termCount = build(filtered, q);
  var sectionCount = applySectionSearch(q);
  var parts = [];
  if (termCount > 0) parts.push(termCount + ' term' + (termCount !== 1 ? 's' : ''));
  if (sectionCount > 0) parts.push(sectionCount + ' chapter section' + (sectionCount !== 1 ? 's' : ''));
  countEl.textContent = parts.length ? parts.join(' &middot; ') : 'no results';
}
```

The full working implementation is in `vce_pe_ch1_partA_skeletal.html`. Copy it verbatim — do not rewrite from memory.

### Behaviour

- Categories in the Key Terms accordion **start collapsed**. Searching auto-expands matching categories with their term definitions visible.
- Chapter section panels start collapsed. Searching auto-expands sections that contain the search text and yellow-highlights the matched text inside them.
- Result count reads e.g. `4 terms · 2 chapter sections`.
- Clearing the search collapses everything that was auto-expanded by the search; sections the user manually opened stay open.

---

## Component Patterns — Study Notes

### 1. Size toggle and search bar (above all sections)

```html
<div class="size-row">
  <span>Text size:</span>
  <button class="sz-btn active" id="sz-s" onclick="setSize(14)">Default</button>
  <button class="sz-btn" id="sz-m" onclick="setSize(17)">Large</button>
  <button class="sz-btn" id="sz-l" onclick="setSize(20)">X-Large</button>
</div>

<div class="search-wrap">
  <input id="search" type="text" placeholder="&#128269; Search terms, definitions..." oninput="doSearch(this.value)">
  <button id="search-clear" onclick="clearSearch()">&#10005; Clear</button>
  <span id="search-count"></span>
</div>
```

Both rows are LEFT-aligned (no `justify-content: center`). The search input uses `flex: 1` so it spans the full available width.

### 2. Textbook image lightbox button

```html
<button class="fig-btn" onclick="openLightbox('filename.png', 'Descriptive caption')">
  &#128247; Descriptive label
</button>
```

Same lightbox JS and rules as before — labels must describe the content (NOT just "Figure X.Y"), buttons go in the section whose content the image illustrates, image files live in the same folder as the HTML.

### 3. Reference table (in a box-wrap panel inside a section)

```html
<div class="box-wrap teal" id="sec121">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#129454; 1.2.1 Functions of the Skeletal System</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="pt">
        <thead><tr><th>Function</th><th>Description</th><th>Example</th></tr></thead>
        <tbody>...</tbody>
      </table>
    </div>
    <p class="box-note">&#128161; Memorise all six functions.</p>
  </div>
</div>
```

Table classes (`.ct`, `.mt`, `.pt`) unchanged — see Chapter 1 reference. All `td` and `th` must have `text-align: left` explicit in CSS.

### 4. Key terms accordion data structure

```javascript
var data = [
  { cat: "1.2 Section Title", color: "blue", hot: false, items: [
    { term: "Term name", def: "Plain English definition.", eg: "Concrete real-world example." },
    { term: "Another term", def: "Definition.", eg: "Example.", note: "Exam tip — one sentence only." }
  ]}
];
```

Category names (`cat`) should NOT include redundant chapter references. The user is already inside the chapter — `"1.2 Section Title"` is fine, but `"Chapter 1 — 1.2 Section Title"` is noise.

### 5. SVG diagram rules

- Every SVG MUST have `style="max-width:Xpx;width:100%;display:inline-block;"` (typical max-width 720–880px) so it doesn't stretch to fill ultra-wide screens.
- Every child box must have a unique non-overlapping x-coordinate. Calculate `next_x = prev_x + width + gap` (min gap 8px). Always verify `last_box_x + last_box_width <= viewBox_width - margin`.
- Use `text-anchor="middle"` with `x = box_x + (box_width / 2)` for centred text.
- For 3+ child columns, prefer wider viewBoxes (860–1100px) and design boxes to fit, not the reverse.

The most common bug: child boxes calculated as `parent_centre - half_width` and pasted with the parent's centre coordinates, producing identical x-values that overlap. Always verify each box's x is unique.

---

## Subject-Level Listing (PE uses table layout)

PE entries appear in a sortable filterable table in the parent app (`studynotes.json` has `"layout": "table"` for PE). The flatten function pulls out:
- Each chapter file as a row, classified Type=`Study Notes`
- Each quiz file as a row, classified Type=`Quiz`
- Anatomical Terminology lives as a top-level chapter on Unit 1 (no subsection) so its AOS column shows "All"
- Index file (`vce_pe_index.html`) referenced via `subject.index[].keywordSource: true` — used silently to enrich the table search via the `data-keywords` attributes on each card

### Index file role

`vce_pe_index.html` is no longer rendered as an iframe in the parent app; it serves only as the **keyword source** for the table search. Each chapter card in the index has:

```html
<div class="card" data-keywords="skeletal bones axial appendicular joints synovial ...">
  <div class="card-head">
    <div class="card-title">Part A — Skeletal System &amp; Joints</div>
    <span class="card-tag tag-notes">Study Notes</span>
  </div>
  <ul class="card-topics">...</ul>
  <div class="card-links">
    <a class="card-link" href="vce_pe_ch1_partA_skeletal.html">&#128218; Study Notes</a>
    <a class="card-link ql" href="vce_pe_ch1_partA_quiz.html">&#127919; Quiz</a>
  </div>
</div>
```

Keep `data-keywords` accurate and densely populated for every chapter card — it powers the parent-app table search.

---

## Page Structure — Quiz File

(Unchanged from previous version. Tabbed file with quiz on tab 1, exam practice on tab 2. See Component Patterns — Quiz File for details.)

```html
<body>
  <h1>VCE PHYSICAL EDUCATION &middot; UNIT 1 AOS1a</h1>
  <p class="chapter-title">Chapter [N] Part [X] &mdash; Quiz &amp; Exam Practice</p>
  <p class="subtitle">Sections [A]–[B] &middot; Live it Up 5th ed.</p>

  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('quiz')">&#127919; Quiz</button>
    <button class="tab-btn" onclick="switchTab('exam')">&#128221; Exam Practice</button>
  </div>

  <div id="tab-quiz" class="tab-pane active">...</div>
  <div id="tab-exam" class="tab-pane">...</div>
</body>
```

Quiz files use the same h1/chapter-title/subtitle structure as study notes.

---

## Component Patterns — Quiz File

### Multiple choice / True-False / Matching / Score tracking

(Unchanged. See section in original skill file for full code patterns. Critical points retained):

- MC: card locks after first answer; correct option always revealed
- T/F: second `checkTF` argument must match the button's truth value
- Matching: 5 pairs per set; each option appears exactly once
- Score: call `updateScore(true|false)` at end of every check function
- Wrong-answer styling uses **teal not red** (`.q-card.wrong { border-color: #9adcc5; background: #f0f7f9; }`)

### Exam question with model answer

```html
<div class="eq-card">
  <div class="eq-head">
    <div class="eq-meta">
      <span class="eq-type">Short Answer</span>
      <span class="eq-marks">2 marks</span>
    </div>
  </div>
  <div class="eq-q">Question text.</div>
  <div class="eq-body">
    <textarea class="eq-answer-area" placeholder="Write your answer..."></textarea>
    <button class="eq-reveal-btn" onclick="toggleModel(this)">&#128065; Show Model Answer</button>
    <div class="eq-model">
      <div class="eq-model-head">&#9989; Model Answer</div>
      <div class="eq-model-body">
        <div class="mark-row"><span class="mark-tick">&#10003;</span><span>Mark point 1 (1 mark)</span></div>
      </div>
      <div class="examiner-tip"><strong>&#9888; Examiner tip:</strong> Common mistake.</div>
    </div>
  </div>
</div>
```

```javascript
function toggleModel(btn) {
  var model = btn.nextElementSibling;
  var open = model.classList.toggle("open");
  btn.innerHTML = open ? "&#128065; Hide Model Answer" : "&#128065; Show Model Answer";
}
```

---

## Quiz Content Guidelines

(Unchanged from previous version):

- 6–10 MC questions, at least one trap targeting common misconception
- 5–8 T/F questions, at least half FALSE
- 3 matching sets of 5 pairs each, no repeated answers
- 3–4 short answer (2–4 marks each), 2–3 extended response (6–8 marks each)
- Always include at least one stimulus-based question
- Model answers mark-by-mark with ✓ tick; every question has an examiner tip

---

## Image Management Rules

(Unchanged — these rules are critical):

1. Always confirm filenames with the user before building
2. Never assign the same filename to two different images
3. Place each image button in the section whose content it illustrates
4. Keep SVG concept diagrams even when textbook image button exists
5. If no image is available, do not add a placeholder button
6. When user uploads images, look at them — don't trust the filename
7. Filename convention: `fig[chapter]_[section]_[descriptor].png`, lowercase, underscores

---

## Workflow for New Chapter Sections

1. **Receive** chapter number, section numbers, and title from the user
2. **Confirm** which sections to group into Part A, Part B etc. if the chapter is long
3. **Ask** if the user has textbook images to link — get exact filenames before building
4. **Build Study Notes file:**
   - h1 (small grey caps), `.chapter-title` (big green), `.subtitle` (italic)
   - Size toggle + full-width search (left-aligned)
   - `📚 Chapter contents` divider (or `📚 Reference panels` if sections lack textbook numbers)
   - One panel per section — section title is the panel header
   - SVG diagrams with `max-width` set; verify no overlapping child boxes
   - Textbook image buttons with descriptive labels
   - `🔍 Key terms` divider then the searchable accordion
   - Key Terms category names without redundant chapter prefix
   - Working search with section-content highlight + key terms filtering
   - Lightbox system for textbook images
5. **Build Quiz file:**
   - Same h1/chapter-title/subtitle structure
   - 15–20 quiz questions (MC/TF/matching), 5–7 exam questions
   - Score tracker, model answers, examiner tips
6. **Update `vce_pe_index.html`** — add a new chapter card with `data-keywords` for table search
7. **Add chapter rows to `studynotes.json`** under the appropriate Unit/AOS subsection so the entries appear in the parent-app table

---

## Hot Topic Sections (running list)

| Unit/Chapter | Hot sections |
|-------------|-------------|
| U1 Ch1 Part A (skeletal) | 1.2.5 Joints (types + structure), 1.2.8 Movement terminology |
| U1 Ch1 Part B (muscular) | 1.3.4 Muscle roles (agonist/antagonist), 1.4.1 Muscle fibre types, 1.4.2 Sliding filament theory |
| U1 Ch1 Part C (neural) | 1.5.3 Neuromuscular junction, 1.5.4 Motor unit recruitment, 1.6.1 Contraction types |
| U1 Ch2 Part A injuries | Sprain vs strain, fracture types, soft vs hard tissue |
| U1 Ch2 Part A illnesses | OA vs RA distinction, osteoporosis & Wolff's Law |
| U1 Ch2 Part B (prevention/rehab) | RICER + HARM, TOTAPS, dynamic vs static stretching |
| U1 Ch2 Part C (keeping safe) | Concussion (no same-day return, GRTP, second impact) |
| U1 Ch2 Part D (permitted/prohibited) | WADA criteria (2 of 3), creatine = PERMITTED, AAS mechanism |
| U1 Ch3 Part A (cardiovascular) | Cardiac output, heart rate response, vascular shunt |

---

## Known Issues & Fixes Applied

| Issue | Fix |
|-------|-----|
| Nav pills did nothing when clicked | `scrollTo` conflicts with `window.scrollTo` — use `jumpTo` |
| Table text centre-aligned | Add `text-align: left` explicitly to all `td` CSS rules |
| Old gradient banner h1 unreadable on green | Replaced with small grey caps h1 + new big green `.chapter-title` element |
| `<p class="section-label">` above every panel was redundant | Section title moved INTO the panel header; `id` moved onto the wrap div |
| Hot Topic badges in middle of header | `margin-left: auto` pushes them right to sit next to the arrow |
| Permitted/Prohibited pills floating in middle | `margin-right: auto` anchors them next to title regardless of sibling badges |
| Key Terms divider showed "— Chapter 3A" suffix | Standardised to plain `🔍 Key terms` everywhere |
| Key Terms accordion opened expanded by default | Hard-coded `cat-body open` replaced with `isSearching ? 'cat-body open' : 'cat-body'` |
| SVG diagrams stretched on wide screens | Add `style="max-width:720-880px;"` to every diagram SVG |
| SVG child boxes geometrically overlapped | Compute each box's `x` explicitly; never rely on parent-centre arithmetic |
| Search only matched Key Terms | Extended search to also walk text inside chapter section panels and auto-expand matches |

---

## Prompt to Activate This Skill in a New Conversation

> "I am creating interactive HTML study notes and quiz files for VCE Physical Education Units 1 & 2 using the Live it Up 5th edition textbook. Please use the attached skill document to generate each chapter section as two files: a study notes file (with the new section-as-panel structure, muted green palette, Chapter contents divider, working two-stage search) and a paired quiz/exam practice file. I will provide the chapter number, section headings, and any textbook image filenames. Follow all rules, patterns and known fixes in the skill document exactly. We have completed Chapter 1, Chapter 2 and Chapter 3 Part A — building the next chapter section now."
