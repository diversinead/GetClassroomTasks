# Skill: VCE Physical Education — Study Notes & Quiz Generator

## Purpose
Generate two paired interactive HTML files per chapter section for VCE Physical Education Units 1 & 2 using the **Live it Up 5th edition** textbook.

- **File 1: Study Notes** — collapsible visual panels, SVG diagrams, reference tables, textbook image lightbox buttons, and a key terms accordion with search
- **File 2: Quiz & Exam Practice** — tabbed file with an interactive quiz (multiple choice, true/false, matching) and exam practice questions (short answer + extended response) with model answers

Each file is fully self-contained HTML — all CSS and JS inline, no external dependencies.

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

### Unit 2: Physical Activity, Sport & Society
- **AOS1:** What are the relationships between physical activity, sport, health & society
- **AOS2:** What are the contemporary issues associated with physical activity and sport

---

## JavaScript Rules (critical — do not deviate)

- Always use `var` — NEVER `const` or `let`
- Never use template literals (backticks) — use string concatenation only
- Never use arrow functions — use `function` keyword or IIFE
- Use HTML entities for special characters: `&#9660;` (▼), `&#9650;` (▲), `&#9658;` (▶), `&#9733;` (★), `&#9888;` (⚠), `&#128161;` (💡), `&#10003;` (✓), `&#128247;` (📷)
- Avoid apostrophes inside JS strings — rephrase to avoid or use `&apos;`
- **Never use `scrollTo` as a function name** — conflicts with `window.scrollTo`. Use `jumpTo` instead
- **Never name anything that shadows a built-in** — check before naming functions

---

## CSS Rules

- No CSS variables — use hardcoded hex values only
- All table `td` cells must have `text-align: left` set explicitly in CSS — do NOT rely on browser defaults
- Hot badge tooltips use `position: absolute; top: calc(100% + 6px)` (drops DOWN) — never upward
- `diagram-body` default is `display: none` — opened via `toggleB()`
- `box-body` default is `display: none` — opened via `toggleB()`
- `cat-body` default is `collapsed` class (display:none) — sections start collapsed

---

## Colour Palette

### Accordion section colours
| Class | Border | Head bg | Use for |
|-------|--------|---------|---------|
| purple | #AFA9EC | rgba(206,203,246,0.35) | Overview, intro, joint structure |
| teal | #5DCAA5 | rgba(159,225,203,0.28) | Muscular system, positive/active concepts |
| coral | #D85A30 | rgba(240,153,123,0.22) | Injury, risk, liabilities |
| amber | #BA7517 | rgba(239,159,39,0.20) | Formulas, calculations, energy systems |
| blue | #378ADD | rgba(133,183,235,0.25) | Skeletal system, bones, general |
| pink | #D4537E | rgba(237,147,177,0.22) | Fibre types, ethics, evaluation |
| gray | #888780 | rgba(180,178,169,0.20) | Definitions, principles, terminology |

### Box/panel wrap colours
| Class | Use for |
|-------|---------|
| .box-wrap.blue | Skeletal functions, general reference |
| .box-wrap.purple | Joint types, comparison tables |
| .box-wrap.teal | Muscle roles, positive concepts |
| .box-wrap.amber | Formulas, vertebral column |
| .box-wrap.green | Positive movement concepts |
| .box-wrap.coral | Risk, injury content |
| .box-wrap.pink | Fibre types, evaluation |

### Diagram wrap colours
| Class | Use for |
|-------|---------|
| .diagram-wrap (default) | Teal border — anatomical diagrams |
| .diagram-wrap.blue | Concept/overview diagrams |
| .diagram-wrap.purple | Joint type diagrams |
| .diagram-wrap.amber | Formula/calculation visuals |

---

## Page Structure — Study Notes File

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VCE PE — Ch[X] Part [Y]: [Topic]</title>
  <style>/* all CSS inline */</style>
</head>
<body>
  <h1>VCE Physical Education — Unit [X] AOS[Y]</h1>
  <p class="subtitle">Chapter [N] Part [X] · Section [A]–[B]: [Title] · Live it Up 5th ed.</p>

  <!-- NAV PILLS (jump to each section) -->
  <div class="nav-pills">...</div>

  <!-- SEARCH BAR -->
  <div class="search-wrap">
    <input id="search" type="text" placeholder="🔍 Search terms..." oninput="doSearch(this.value)">
    <button id="search-clear" onclick="clearSearch()">✕ Clear</button>
    <span id="search-count"></span>
  </div>

  <!-- SECTION LABEL -->
  <p class="section-label" id="sec[XY]">emoji Section X.Y Title</p>

  <!-- DIAGRAMS (collapsible, default closed) -->
  <!-- VISUAL PANELS / REFERENCE TABLES (collapsible, default closed) -->
  <!-- KEY TERMS ACCORDION -->
  <div id="list"></div>
  <div id="no-results">No terms match your search.</div>

  <p class="footer">VCE Physical Education — Unit X AOS Y · Ch[N] Part [X] · Live it Up 5th ed. · ★</p>

  <!-- LIGHTBOX OVERLAY -->
  <div class="lightbox-overlay" id="lightbox" onclick="closeLightbox(event)">...</div>

  <script>/* all JS inline */</script>
</body>
</html>
```

---

## Component Patterns — Study Notes

### 1. Nav pills
```html
<div class="nav-pills">
  <span class="nav-pill" onclick="jumpTo('sec11')">1.1 Overview</span>
  <span class="nav-pill" onclick="jumpTo('sec12')">1.2 Topic</span>
</div>
```
**Critical:** Use `jumpTo()` not `scrollTo()` — scrollTo is a reserved browser function.

```javascript
function jumpTo(id) {
  var el = document.getElementById(id);
  if (el) { el.scrollIntoView({ behavior: "smooth", block: "start" }); }
}
```

### 2. Search with highlight and result count
```javascript
function doSearch(q) {
  q = q.trim();
  var clearBtn = document.getElementById("search-clear");
  var countEl = document.getElementById("search-count");
  clearBtn.className = q ? "visible" : "";
  if (!q) { build(data, ""); countEl.textContent = ""; return; }
  var ql = q.toLowerCase();
  var filtered = [];
  for (var i = 0; i < data.length; i++) {
    var cat = data[i];
    var items = [];
    for (var j = 0; j < cat.items.length; j++) {
      var item = cat.items[j];
      if (item.term.toLowerCase().indexOf(ql) > -1 ||
          item.def.toLowerCase().indexOf(ql) > -1 ||
          (item.eg && item.eg.toLowerCase().indexOf(ql) > -1) ||
          (item.note && item.note.toLowerCase().indexOf(ql) > -1)) {
        items.push(item);
      }
    }
    if (items.length) filtered.push({ cat: cat.cat, color: cat.color, hot: cat.hot, items: items });
  }
  var count = build(filtered, q);
  countEl.textContent = count + " result" + (count !== 1 ? "s" : "");
}

function highlight(text, q) {
  if (!q) return text;
  var re = new RegExp("(" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
  return text.replace(re, '<span class="hl">$1</span>');
}
```
- Search expands matching sections and auto-opens matching terms
- Matching text is highlighted yellow using `.hl` class
- Shows result count next to clear button

### 3. Textbook image lightbox button
```html
<button class="fig-btn" onclick="openLightbox('filename.png', 'Descriptive caption')">
  &#128247; Descriptive label (NOT "View Figure X.Y")
</button>
```

**Button label rules:**
- Label must be DESCRIPTIVE of the content, not just the figure number
- ✅ "Major bones of the skeletal system"
- ✅ "Six types of synovial joint"
- ✅ "Basic structure of a synovial joint"
- ❌ "View Textbook Figure 1.5" — too generic
- ❌ "View Figure 1.14" — tells user nothing

**Button placement rules:**
- Place buttons in the CORRECT section (e.g. joint classification button in the joints section, not the bones section)
- Multiple buttons can appear in one panel when multiple images relate to that concept
- Knee anatomy image belongs in the SYNOVIAL STRUCTURE section, not joint types

**Lightbox JS (include verbatim):**
```javascript
function openLightbox(filename, caption) {
  var overlay = document.getElementById("lightbox");
  var img = document.getElementById("lightbox-img");
  var cap = document.getElementById("lightbox-caption");
  var fn = document.getElementById("lightbox-filename");
  var err = document.getElementById("lightbox-error");
  img.src = filename;
  cap.textContent = caption;
  fn.textContent = "File: " + filename;
  err.className = "lightbox-error";
  img.onerror = function() { err.className = "lightbox-error show"; };
  img.onload = function() { err.className = "lightbox-error"; };
  overlay.className = "lightbox-overlay open";
  document.body.style.overflow = "hidden";
}
function closeLightboxBtn() {
  document.getElementById("lightbox").className = "lightbox-overlay";
  document.body.style.overflow = "";
}
function closeLightbox(e) {
  if (e.target === document.getElementById("lightbox")) { closeLightboxBtn(); }
}
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") { closeLightboxBtn(); }
});
```

**Image files** must be in the SAME FOLDER as the HTML file. If the image is not found, a helpful error message is shown automatically.

### 4. Diagram panel (collapsible, default closed)
```html
<div class="diagram-wrap [color-modifier]">
  <div class="diagram-head [color-modifier]" onclick="toggleB(this)">
    <span>emoji Figure X.Y — Title</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="diagram-body">
    <!-- SVG or table content here -->
    <p class="diagram-caption">Caption / exam tip text here.</p>
    <button class="fig-btn" onclick="openLightbox('filename.png','Caption')">&#128247; Descriptive label</button>
  </div>
</div>
```

**SVG diagram rules:**
- Use inline SVG — no external images
- Set explicit `viewBox` and `style="max-width:Xpx;width:100%;display:inline-block;"`
- Use `svg text { font-family: Georgia, serif; }` in CSS
- For labelled anatomy diagrams: use a wide viewBox (e.g. 860px) with skeleton centred and labels in left/right zones with adequate vertical spacing (min 26px between labels)
- Left labels: right-aligned text (`text-anchor="end"`) at a fixed x column with leader lines to bones
- Right labels: left-aligned text at a fixed x column with leader lines
- Leader lines: `<line>` elements in `stroke="#888" stroke-width="1"`

**When to use SVG vs textbook image button:**
- Use SVG for concept diagrams (planes of movement, lever systems, fibre type comparisons, step-by-step processes)
- Use textbook image button for anatomical figures that are better shown from the actual textbook (skeleton, vertebral column, synovial structure, joint types)
- You can combine both: SVG diagram for concept + textbook button for the real figure alongside it

### 5. Reference table (in a box-wrap panel)
```html
<div class="box-wrap [color]">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>emoji Table Title</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="[ct|mt|pt]">
        <thead><tr><th>Col 1</th><th>Col 2</th></tr></thead>
        <tbody>
          <tr><td><strong>Term</strong></td><td>Description</td></tr>
        </tbody>
      </table>
    </div>
    <p class="box-note">&#128161; Tip text here.</p>
    <button class="fig-btn" onclick="openLightbox(...)">&#128247; Label</button>
  </div>
</div>
```

**Table classes:**
| Class | Header colour | Use for |
|-------|--------------|---------|
| `.ct` | Dark charcoal `#2C2C2A` | Comparison tables, general |
| `.mt` | Dark teal `#085041` | Muscle/movement tables |
| `.pt` | Dark purple `#3C3489` | Joint/skeletal tables |

**All tables must have `text-align: left` on both `th` and `td` in CSS.** This must be set explicitly — do not rely on browser defaults.

### 6. Key terms accordion data structure
```javascript
var data = [
  { cat: "1.2 Section Title", color: "blue", hot: false, items: [
    { term: "Term name", def: "Plain English definition.", eg: "Concrete real-world example." },
    { term: "Another term", def: "Definition.", eg: "Example.", note: "Exam tip — one sentence only." }
  ]},
  { cat: "1.3 Another Section", color: "teal", hot: true, items: [...] }
];
```
- `hot: true` adds red ★ HOT TOPIC badge
- `note` field adds ⚠ Exam tip block inside the expanded term
- Term sections start **collapsed** by default
- When searching, sections auto-expand and terms auto-open to show matches

### 7. toggleB function (verbatim)
```javascript
function toggleB(el) {
  var body = el.nextElementSibling;
  var arr = el.querySelector(".cat-arrow");
  var open = body.classList.toggle("open");
  arr.innerHTML = open ? "&#9650;" : "&#9660;";
}
```

### 8. build() and toggle() functions (verbatim)
```javascript
function build(source, q) {
  var list = document.getElementById("list");
  var noRes = document.getElementById("no-results");
  list.innerHTML = "";
  var total = 0;
  for (var i = 0; i < source.length; i++) {
    var cat = source[i];
    if (!cat.items || !cat.items.length) continue;
    total += cat.items.length;
    var div = document.createElement("div");
    div.className = "cat " + cat.color;
    var badge = cat.hot ? '<span class="hot-badge">&#9733; HOT TOPIC<span class="tip">High-frequency exam topic</span></span>' : "";
    var head = document.createElement("div");
    head.className = "cat-head";
    head.innerHTML = '<span class="cat-head-text">' + cat.cat + '</span><div class="cat-head-right">' + badge + '<small>' + cat.items.length + ' terms</small><span class="cat-arrow">&#9660;</span></div>';
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
    body.className = "cat-body";
    if (q) body.classList.remove("collapsed");
    else body.classList.add("collapsed");
    for (var j = 0; j < cat.items.length; j++) {
      var item = cat.items[j];
      var t = document.createElement("div");
      t.className = "term";
      var note = item.note ? '<span class="term-note">&#9888; Exam tip: ' + highlight(item.note, q) + '</span>' : "";
      t.innerHTML = '<div class="term-title" onclick="toggle(this)"><span>' + highlight(item.term, q) + '</span><span class="arrow">&#9660;</span></div><div class="term-body"><p class="term-def">' + highlight(item.def, q) + '</p><span class="term-eg">Eg: ' + highlight(item.eg, q) + '</span>' + note + '</div>';
      if (q) t.querySelector(".term-body").classList.add("open");
      body.appendChild(t);
    }
    div.appendChild(body);
    list.appendChild(div);
  }
  noRes.style.display = (total === 0) ? "block" : "none";
  return total;
}

function toggle(el) {
  var body = el.nextElementSibling;
  var arr = el.querySelector(".arrow");
  var open = body.classList.toggle("open");
  arr.innerHTML = open ? "&#9650;" : "&#9660;";
}

build(data, "");
```

---

## Content Guidelines — Study Notes

### Term definitions
- Plain English — no jargon unless the jargon IS the term
- Maximum 2 sentences
- No apostrophes in JS strings — rephrase ("does not" not "doesn't")
- Always include: term, definition, real-world example, and exam tip if a common mistake exists

### Examples
- Always sport/exercise-specific and concrete (name the sport, the muscle, the movement)
- Use Australian context where possible (AFL, netball, cricket, swimming, athletics)
- Be specific: "The quadriceps contract concentrically during knee extension in a drop punt kick" not "muscles work during kicking"

### Exam tips (note field)
- Only include when there is a GENUINE common exam mistake
- One sentence only
- Examples of good exam tips:
  - "LIGAMENT = bone to bone. TENDON = muscle to bone. Confusing these is the #1 exam mistake."
  - "Dorsiflexion and plantarflexion are ankle-specific — do not just write flexion/extension."
  - "Circumduction is only possible at ball and socket joints — not at hinge joints."
  - "Menisci exist at the KNEE ONLY — do not apply this term to other joints."

### HOT TOPIC identification
Apply `hot: true` to sections covering high-frequency VCE PE exam topics:

| Unit/Chapter | Hot sections |
|-------------|-------------|
| U1 Ch1 | Joints (types + structure), Movement terminology, Muscle roles, Sliding filament theory, Muscle fibre types |
| U1 Ch2 | RICER/HARM, Acute vs chronic injury, Soft tissue injury types |
| U1 AOS2 | Cardiac output, Heart rate response, VO2 max |

---

## Page Structure — Quiz File

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>VCE PE — Ch[X] Part [Y]: Quiz & Exam Practice</title>
  <style>/* all CSS inline */</style>
</head>
<body>
  <h1>VCE Physical Education — Unit [X] AOS[Y]</h1>
  <p class="subtitle">Chapter [N] Part [X] · Quiz & Exam Practice · Sections [A]–[B]</p>

  <!-- TAB BAR -->
  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('quiz')">🎯 Quiz</button>
    <button class="tab-btn" onclick="switchTab('exam')">📝 Exam Practice</button>
  </div>

  <!-- TAB 1: QUIZ -->
  <div id="tab-quiz" class="tab-pane active">
    <!-- Score bar -->
    <!-- Multiple choice questions -->
    <!-- True/False questions -->
    <!-- Matching questions -->
  </div>

  <!-- TAB 2: EXAM PRACTICE -->
  <div id="tab-exam" class="tab-pane">
    <!-- Short answer questions (2–4 marks) -->
    <!-- Extended response questions (6–8 marks) -->
  </div>

  <script>/* all JS inline */</script>
</body>
</html>
```

---

## Component Patterns — Quiz File

### Multiple choice question
```javascript
var mcAnswers = {
  mc1: { correct: "B", explanation: "Explanation of why B is correct and why others are wrong." }
};
```
```html
<div class="q-card" id="mc1">
  <div class="q-num">Question 1 — Multiple Choice</div>
  <div class="q-text">Question text here?</div>
  <div class="mc-options">
    <div class="mc-opt" onclick="checkMC(this,'mc1','A')"><span class="opt-letter">A</span> Option A text</div>
    <div class="mc-opt" onclick="checkMC(this,'mc1','B')"><span class="opt-letter">B</span> Option B text</div>
    <div class="mc-opt" onclick="checkMC(this,'mc1','C')"><span class="opt-letter">C</span> Option C text</div>
    <div class="mc-opt" onclick="checkMC(this,'mc1','D')"><span class="opt-letter">D</span> Option D text</div>
  </div>
  <div class="q-feedback" id="fb-mc1"></div>
</div>
```
- On answer: correct option turns green, incorrect turns red, correct option always revealed
- Explanation shown in feedback block
- Card locked after first answer — cannot change

### True/False question
```javascript
var tfAnswers = {
  tf1: { correct: true, explanation: "Explanation of the correct answer." }
};
```
```html
<div class="q-card" id="tf1">
  <div class="q-num">Question N — True or False</div>
  <div class="q-text">Statement to evaluate.</div>
  <div class="tf-options">
    <button class="tf-btn" onclick="checkTF(this,'tf1',true)">True</button>
    <button class="tf-btn" onclick="checkTF(this,'tf1',false)">False</button>
  </div>
  <div class="q-feedback" id="fb-tf1"></div>
</div>
```
**Critical:** The second argument to `checkTF` must match what clicking that button represents:
- True button: `onclick="checkTF(this,'tfN',true)"`
- False button: `onclick="checkTF(this,'tfN',false)"`

### Matching question
```html
<div class="q-card" id="match1">
  <div class="q-num">Question N — Matching</div>
  <div class="q-text">Match each [X] to its correct [Y].</div>
  <div class="match-wrap">
    <div>
      <div class="match-col-head">Column A</div>
      <div class="match-term">Item 1</div>
      <div class="match-term">Item 2</div>
    </div>
    <div>
      <div class="match-col-head">Column B</div>
      <select class="match-select" id="m1-1"><option value="">-- select --</option>...</select>
      <select class="match-select" id="m1-2"><option value="">-- select --</option>...</select>
    </div>
  </div>
  <button class="match-check-btn" onclick="checkMatch1()">Check Answers</button>
  <div class="q-feedback" id="fb-match1"></div>
</div>
```
```javascript
function checkMatch1() {
  checkMatch("match1", {
    "m1-1": "Correct answer for item 1",
    "m1-2": "Correct answer for item 2"
  }, "fb-match1");
}
```

### Score tracking
```javascript
var totalQ = [total number of quiz questions];
var answered = 0;
var correctCount = 0;

function updateScore(gotIt) {
  answered++;
  if (gotIt) correctCount++;
  document.getElementById("score-correct").textContent = correctCount;
  document.getElementById("score-total").textContent = answered;
  var pct = Math.round((answered / totalQ) * 100);
  document.getElementById("progress-bar").style.width = pct + "%";
}
```
- Call `updateScore(true)` or `updateScore(false)` at the end of every `checkMC`, `checkTF`, and `checkMatch` function

### Exam question with model answer
```html
<div class="eq-card">
  <div class="eq-head">
    <div class="eq-meta">
      <span class="eq-type">Short Answer</span>  <!-- or "Extended Response" -->
      <span class="eq-marks">2 marks</span>
    </div>
  </div>
  <!-- Optional stimulus: -->
  <div class="eq-stimulus">Context or case study text here.</div>
  <div class="eq-q">Question text here.</div>
  <div class="eq-body">
    <textarea class="eq-answer-area" placeholder="Write your answer here..."></textarea>
    <button class="eq-reveal-btn" onclick="toggleModel(this)">&#128065; Show Model Answer</button>
    <div class="eq-model">
      <div class="eq-model-head">&#9989; Model Answer</div>
      <div class="eq-model-body">
        <div class="mark-row"><span class="mark-tick">&#10003;</span><span>Mark point 1 (1 mark)</span></div>
        <div class="mark-row"><span class="mark-tick">&#10003;</span><span>Mark point 2 (1 mark)</span></div>
      </div>
      <div class="examiner-tip"><strong>&#9888; Examiner tip:</strong> What students commonly get wrong and how to score full marks.</div>
    </div>
  </div>
</div>
```

### Model answer toggle (verbatim)
```javascript
function toggleModel(btn) {
  var model = btn.nextElementSibling;
  var open = model.classList.toggle("open");
  btn.innerHTML = open ? "&#128065; Hide Model Answer" : "&#128065; Show Model Answer";
}
```

---

## Quiz Content Guidelines

### Multiple choice questions
- 6–10 questions per quiz
- Always include one "trap" question testing the most common misconception (e.g. ligament vs tendon)
- Distractors (wrong options) should be plausible — not obviously wrong
- Each question should test a DIFFERENT concept

### True/False questions
- 5–8 questions per quiz
- At least half should be FALSE — students tend to assume true
- Target common misconceptions: wrong definitions, reversed terms, incorrect numbers

### Matching questions
- 3 matching sets per quiz
- 5 pairs per set — enough to challenge without being overwhelming
- Sets should test: terminology definitions, structure-to-function, concept-to-example
- Each option in a set should appear exactly ONCE — no repeated answers

### Exam questions
- 3–4 short answer questions (2–4 marks each)
- 2–3 extended response questions (6–8 marks each)
- At least one question should use a stimulus (case study, scenario, or athlete context)
- Model answers should be mark-by-mark with ✓ tick for each mark point
- Every question must include an examiner tip highlighting the most common errors

---

## Workflow for New Chapter Sections

1. **Receive** chapter number, section numbers, and title from the user
2. **Confirm** which sections to group into Part A, Part B etc. if the chapter is long
3. **Ask** if the user has textbook images to link — get the filenames before building
4. **Build Study Notes file:**
   - Nav pills for each section
   - SVG diagrams for concept visuals (planes, lever systems, comparisons)
   - Textbook image buttons for anatomical figures (use descriptive labels)
   - Reference tables in collapsible panels
   - Key terms accordion (collapsed by default, HOT TOPIC badges where appropriate)
   - Working search with highlight
   - Lightbox system for all textbook images
5. **Build Quiz file:**
   - Tab 1: 15–20 quiz questions across MC, T/F and matching
   - Tab 2: 5–7 exam practice questions across short answer and extended response
   - Score tracker and reset button
   - Model answers with mark-by-mark breakdown and examiner tips
6. **Remind user** to save both HTML files and all image files in the **same folder**

---

## Known Issues & Fixes Applied

| Issue | Fix |
|-------|-----|
| Nav pills did nothing when clicked | `scrollTo` conflicts with `window.scrollTo` — renamed to `jumpTo` |
| Table text centre-aligned | Added `text-align: left` explicitly to all `td` CSS rules |
| Right-side skeleton labels bunched | Increased viewBox width to 860px, fixed label columns with right-aligned left labels and left-aligned right labels, 26px+ vertical spacing |
| SVG skeleton replaced with drawing | Cannot embed copyrighted textbook images — use SVG for layout diagram + lightbox button for textbook photo |
| Classification of joints button in wrong section | Always check: image goes in the section it BELONGS TO conceptually, not wherever convenient |
| Knee anatomy button in joint types instead of synovial structure | Knee anatomy shows internal joint STRUCTURE — belongs in 1.2.6, not 1.2.5 |
| Tendons missing from synovial joint structure table | Tendons are critical — always include in any joint structure section |

---

## Prompt to Activate This Skill in a New Conversation

Paste the following at the start of a new chat, then attach this skill document:

> "I am creating interactive HTML study notes and quiz files for VCE Physical Education Units 1 & 2 using the Live it Up 5th edition textbook. Please use the attached skill document to generate each chapter section as two files: a study notes file and a paired quiz/exam practice file. I will provide the chapter number, section headings, and any textbook image filenames. Follow all rules, patterns and known fixes in the skill document exactly."
