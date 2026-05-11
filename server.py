from http.server import HTTPServer, BaseHTTPRequestHandler
import html as html_lib
import json
import os
import re

from datetime import date

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSESSMENTS_FILE = os.path.join(BASE_DIR, 'Assessments', 'assessments_data.json')
HOMEWORK_FILE = os.path.join(BASE_DIR, 'Homework', 'homework_data.json')
TODOS_FILE = os.path.join(BASE_DIR, 'TodoLists', 'todo_data.json')
STUDYNOTES_FILE = os.path.join(BASE_DIR, 'StudyNotes', 'studynotes.json')
IMPORTANT_DATES_FILE = os.path.join(BASE_DIR, 'ImportantDates', 'dates_data.json')


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def singular_date(date_str):
    """Convert date range like '23-27 Feb' to singular '23 Feb'."""
    if not date_str:
        return date_str
    if '\u2013' not in date_str and '-' not in date_str:
        return date_str
    m = re.match(r'(\d+)', date_str)
    months = re.findall(r'[A-Z][a-z]{2}', date_str)
    if m and months:
        return f"{m.group(1)} {months[0]}"
    return date_str


def reset_todos_if_new_day(data):
    """Reset all checked states when the date changes."""
    today = date.today().isoformat()
    if data.get('last_reset') != today:
        for student in ('eddie', 'dara'):
            for period in ('morning', 'afterschool', 'bedtime'):
                for item in data.get(student, {}).get(period, []):
                    item['checked'] = False
        data['last_reset'] = today
    return data


def normalize_assessments(data):
    """Convert legacy string assessments to {text, status, due} objects."""
    for student in ('eddie', 'dara'):
        for term in data.get(student, {}):
            for week_entry in data[student][term]:
                week_date = week_entry.get('date', '')
                new_assessments = []
                for a in week_entry.get('assessments', []):
                    if isinstance(a, str):
                        a = {'text': a, 'status': 'Not Started'}
                    if 'due' not in a:
                        a['due'] = singular_date(week_date)
                    if 'notes' not in a:
                        a['notes'] = ''
                    new_assessments.append(a)
                week_entry['assessments'] = new_assessments
    return data


# ── Markdown rendering (stdlib-only, print-friendly viewer) ────────────────

MD_VIEWER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>
  @page { size: A4; margin: 18mm 16mm; }
  * { box-sizing: border-box; }
  body { font-family: Georgia, "Times New Roman", serif; color: #1a1a18; background: #f4f4f4;
         margin: 0; padding: 0; line-height: 1.55; }
  .page { max-width: 820px; margin: 0 auto; background: #fff; padding: 30px 38px 50px;
          box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
  .toolbar { position: sticky; top: 0; z-index: 10; background: #2a7a7a; color: #fff;
             padding: 9px 16px; display: flex; gap: 10px; align-items: center; justify-content: space-between;
             box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-family: -apple-system, "Segoe UI", sans-serif; }
  .toolbar a, .toolbar button { color: #fff; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
             padding: 5px 12px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;
             text-decoration: none; font-family: inherit; }
  .toolbar a:hover, .toolbar button:hover { background: rgba(255,255,255,0.25); }
  .toolbar .title { font-size: 13px; font-weight: 600; opacity: 0.9; }

  h1 { font-size: 24px; font-weight: 700; color: #2a7a7a; margin: 26px 0 10px;
       border-bottom: 2px solid #2a7a7a; padding-bottom: 6px; }
  h1:first-of-type { margin-top: 4px; }
  h2 { font-size: 18px; font-weight: 700; color: #1f5c5c; margin: 22px 0 8px; }
  h3 { font-size: 15px; font-weight: 700; color: #333; margin: 16px 0 6px; }
  h4 { font-size: 14px; font-weight: 700; color: #555; margin: 14px 0 6px; }
  p  { margin: 0 0 10px; font-size: 14px; }
  ul, ol { margin: 0 0 12px 28px; font-size: 14px; }
  li { margin-bottom: 4px; }
  ul.checklist { list-style: none; margin-left: 0; padding-left: 0; }
  ul.checklist li { padding-left: 26px; position: relative; }
  ul.checklist li::before { content: "\\2610"; position: absolute; left: 0; font-size: 16px; color: #888; }
  ul.checklist li.checked::before { content: "\\2611"; color: #2a7a7a; }
  blockquote { border-left: 4px solid #2a7a7a; background: #f0f7f7; margin: 12px 0;
               padding: 10px 14px; color: #1f5c5c; font-style: italic; font-size: 13.5px; border-radius: 0 6px 6px 0; }
  blockquote p { margin: 0; }
  hr { border: none; border-top: 1px solid #d0d0d0; margin: 22px 0; }
  code { background: #f4f4f4; border: 1px solid #e0e0e0; border-radius: 3px;
         padding: 1px 5px; font-family: "Consolas", "Menlo", monospace; font-size: 13px; }
  pre { background: #f4f4f4; border: 1px solid #e0e0e0; border-radius: 6px;
        padding: 10px 12px; overflow-x: auto; font-size: 13px; margin: 0 0 12px; }
  pre code { background: none; border: none; padding: 0; }
  a { color: #1a5fb4; }
  strong { color: #1a1a18; }
  em { color: #333; }

  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
  table th { background: #2a7a7a; color: #fff; padding: 7px 10px; text-align: left; font-weight: 700; }
  table td { padding: 7px 10px; border-bottom: 1px solid #e8e8e8; vertical-align: top; line-height: 1.5; }
  table tr:nth-child(even) td { background: #f8f9fa; }
  table tr:last-child td { border-bottom: none; }

  @media print {
    body { background: #fff; }
    .toolbar, .no-print { display: none !important; }
    .page { max-width: none; margin: 0; padding: 0; box-shadow: none; }
    h1 { color: #000; border-bottom-color: #000; page-break-before: always; }
    h1:first-of-type { page-break-before: auto; }
    h2, h3 { page-break-after: avoid; }
    h2 + p, h2 + ul, h2 + ol, h2 + table, h3 + p, h3 + ul, h3 + ol, h3 + table { page-break-before: avoid; }
    table, tr, blockquote { page-break-inside: avoid; }
    hr { page-break-after: always; border: none; margin: 0; }
    a { color: #000; text-decoration: none; }
    body { font-size: 11pt; }
    p, ul, ol { font-size: 11pt; }
    table { font-size: 10pt; }
    blockquote { background: #f4f4f4; }
  }
</style>
</head>
<body>
<div class="toolbar no-print">
  <a href="javascript:history.length>1?history.back():window.close()">&#x2190; Back</a>
  <span class="title">__TITLE__</span>
  <button onclick="window.print()">&#x1F5A8; Print</button>
</div>
<div class="page">
__BODY__
</div>
</body>
</html>"""


def render_markdown(text):
    """Convert markdown to HTML. Pure Python, stdlib only.

    Supports: headings (#-####), bold, italic, inline code, fenced code blocks,
    bullet/numbered/checkbox lists, tables, blockquotes, hr, links, paragraphs.
    Walks the document as a state machine: each line is dispatched by kind, and
    consecutive lines of the same kind are collected before being rendered.
    """
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line — skip
        if stripped == '':
            i += 1
            continue

        # Fenced code block
        if stripped.startswith('```'):
            j = i + 1
            while j < n and not lines[j].lstrip().startswith('```'):
                j += 1
            body = '\n'.join(lines[i + 1:j])
            out.append('<pre><code>' + html_lib.escape(body) + '</code></pre>')
            i = j + 1
            continue

        # Heading
        m = re.match(r'^(#{1,4})\s+(.*)$', stripped)
        if m:
            level = len(m.group(1))
            out.append('<h{0}>{1}</h{0}>'.format(level, _render_inline(m.group(2)))
                       )
            i += 1
            continue

        # Horizontal rule (a line of 3+ dashes/asterisks/underscores by itself)
        if re.match(r'^(?:---+|\*\*\*+|___+)$', stripped):
            out.append('<hr>')
            i += 1
            continue

        # Table: current line has |, next line is a |-separator with dashes
        if (
            '|' in line
            and i + 1 < n
            and '|' in lines[i + 1]
            and re.match(r'^\s*\|?[\s|:\-]+\|?\s*$', lines[i + 1])
            and '-' in lines[i + 1]
        ):
            j = i + 2
            while j < n and lines[j].strip() != '' and '|' in lines[j]:
                j += 1
            out.append(_render_table(lines[i:j]))
            i = j
            continue

        # Blockquote (consecutive lines starting with >)
        if stripped.startswith('>'):
            j = i
            while j < n and lines[j].lstrip().startswith('>'):
                j += 1
            inner = ' '.join(re.sub(r'^\s*>\s?', '', ln) for ln in lines[i:j])
            out.append('<blockquote><p>' + _render_inline(inner) + '</p></blockquote>')
            i = j
            continue

        # Checkbox list (- [ ] / - [x])
        if re.match(r'^\s*-\s+\[[ xX]\]\s+', line):
            j = i
            while j < n and re.match(r'^\s*-\s+\[[ xX]\]\s+', lines[j]):
                j += 1
            out.append(_render_checklist(lines[i:j]))
            i = j
            continue

        # Bullet list
        if re.match(r'^\s*[-*]\s+', line):
            j = i
            # Stop at checkbox-list lines so they get rendered as their own block
            while j < n and re.match(r'^\s*[-*]\s+', lines[j]) and not re.match(r'^\s*-\s+\[[ xX]\]\s+', lines[j]):
                j += 1
            out.append(_render_ul(lines[i:j]))
            i = j
            continue

        # Numbered list
        if re.match(r'^\s*\d+\.\s+', line):
            j = i
            while j < n and re.match(r'^\s*\d+\.\s+', lines[j]):
                j += 1
            out.append(_render_ol(lines[i:j]))
            i = j
            continue

        # Paragraph: collect until blank line or until a different kind of block starts
        j = i
        while j < n:
            stp = lines[j].strip()
            if stp == '':
                break
            if re.match(r'^#{1,4}\s+', stp):
                break
            if re.match(r'^(?:---+|\*\*\*+|___+)$', stp):
                break
            if re.match(r'^[-*]\s+', stp):
                break
            if re.match(r'^\d+\.\s+', stp):
                break
            if stp.startswith('>'):
                break
            if stp.startswith('```'):
                break
            j += 1
        para = ' '.join(ln.strip() for ln in lines[i:j])
        out.append('<p>' + _render_inline(para) + '</p>')
        i = j

    return '\n'.join(out)


def _split_table_row(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in line.split('|')]


def _render_table(lines):
    header = _split_table_row(lines[0])
    body_rows = [_split_table_row(ln) for ln in lines[2:]]  # skip header + separator
    out = ['<table>', '<thead><tr>']
    for cell in header:
        out.append('<th>' + _render_inline(cell) + '</th>')
    out.append('</tr></thead><tbody>')
    for row in body_rows:
        out.append('<tr>')
        for cell in row:
            out.append('<td>' + _render_inline(cell) + '</td>')
        out.append('</tr>')
    out.append('</tbody></table>')
    return ''.join(out)


def _render_checklist(lines):
    out = ['<ul class="checklist">']
    for ln in lines:
        m = re.match(r'^\s*-\s+\[([ xX])\]\s+(.*)$', ln)
        if not m:
            continue
        checked = m.group(1).lower() == 'x'
        cls = ' class="checked"' if checked else ''
        out.append('<li' + cls + '>' + _render_inline(m.group(2)) + '</li>')
    out.append('</ul>')
    return ''.join(out)


def _render_ul(lines):
    out = ['<ul>']
    for ln in lines:
        m = re.match(r'^\s*[-*]\s+(.*)$', ln)
        if m:
            out.append('<li>' + _render_inline(m.group(1)) + '</li>')
    out.append('</ul>')
    return ''.join(out)


def _render_ol(lines):
    out = ['<ol>']
    for ln in lines:
        m = re.match(r'^\s*\d+\.\s+(.*)$', ln)
        if m:
            out.append('<li>' + _render_inline(m.group(1)) + '</li>')
    out.append('</ol>')
    return ''.join(out)


def _render_inline(text):
    """Apply inline markdown: code spans, bold, italic, links. HTML-escapes plain text."""
    # Stash code spans first so their contents aren't transformed
    code_spans = []

    def stash(m):
        code_spans.append(m.group(1))
        return '\x00CODE{0}\x00'.format(len(code_spans) - 1)

    text = re.sub(r'`([^`]+)`', stash, text)

    # Stash links similarly so the URL isn't HTML-escaped wrong
    links = []

    def stash_link(m):
        links.append((m.group(1), m.group(2)))
        return '\x00LINK{0}\x00'.format(len(links) - 1)

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', stash_link, text)

    # Now escape any HTML special chars in the remaining plain text
    text = html_lib.escape(text, quote=False)

    # Bold (**text**)
    text = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (*text*) — avoid matching inside ** or empty
    text = re.sub(r'(?<!\*)\*([^*\s][^*]*?)\*(?!\*)', r'<em>\1</em>', text)

    # Restore links (escape inside text portion only)
    for i, (label, url) in enumerate(links):
        safe_label = html_lib.escape(label, quote=False)
        safe_url = html_lib.escape(url, quote=True)
        text = text.replace('\x00LINK{0}\x00'.format(i),
                            '<a href="{0}">{1}</a>'.format(safe_url, safe_label))

    # Restore code spans (escape their contents)
    for i, code in enumerate(code_spans):
        text = text.replace('\x00CODE{0}\x00'.format(i),
                            '<code>' + html_lib.escape(code, quote=False) + '</code>')

    return text


def render_markdown_page(md_text, title):
    body = render_markdown(md_text)
    title_safe = html_lib.escape(title, quote=False)
    return MD_VIEWER_TEMPLATE.replace('__TITLE__', title_safe).replace('__BODY__', body)


# Back-button toolbar injected into every HTML file served from /studynotes/.
# Hidden inside iframes (so the PE Index iframe doesn't get a duplicate button)
# and hidden in print. Detects student from the URL path.
BACK_BUTTON_SNIPPET = """
<style>
  #__back-toolbar { position: sticky; top: 0; z-index: 9999;
    padding: 7px 14px; background: #2a7a7a;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: -16px -16px 12px -16px; }
  #__back-toolbar a { color: #fff; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3); padding: 4px 11px;
    border-radius: 6px; font-size: 13px; font-weight: 600;
    text-decoration: none; display: inline-block; }
  #__back-toolbar a:hover { background: rgba(255,255,255,0.25); }
  @media print { #__back-toolbar { display: none !important; } }
</style>
<div id="__back-toolbar" style="display:none">
  <a id="__back-link" href="/eddie/notes">&#x2190; Back to notes</a>
</div>
<script>
  (function(){
    if (window.self !== window.top) return;
    var bar = document.getElementById('__back-toolbar');
    var link = document.getElementById('__back-link');
    if (!bar || !link) return;
    var m = window.location.pathname.match(/\\/studynotes\\/(eddie|dara)\\//);
    if (m) link.href = '/' + m[1] + '/notes';
    bar.style.display = 'block';
  })();
</script>
"""


def inject_back_button(html):
    """Insert the back-button toolbar just after <body> so it appears at the top of the page."""
    pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
    if pattern.search(html):
        return pattern.sub(lambda m: m.group(1) + BACK_BUTTON_SNIPPET, html, count=1)
    # Fallback: prepend to the document if no <body> tag found
    return BACK_BUTTON_SNIPPET + html


# ───────────────────────────────────────────────────────────────────────────


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.serve_file('launcher.html', 'text/html')
        elif self.path in ('/eddie', '/dara'):
            self.serve_file('student.html', 'text/html')
        elif self.path in ('/eddie/notes', '/dara/notes'):
            self.serve_file('studynotes.html', 'text/html')
        elif self.path.startswith('/studynotes/'):
            rel = self.path[len('/studynotes/'):]
            if '..' in rel or rel.startswith('/'):
                self.send_response(403)
                self.end_headers()
                return
            ext = os.path.splitext(rel)[1].lower()
            if ext == '.md':
                # Render markdown through the print-friendly viewer template
                md_path = os.path.join(BASE_DIR, 'StudyNotes', rel)
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        md_text = f.read()
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
                    return
                title = os.path.splitext(os.path.basename(rel))[0].replace('_', ' ').replace('-', ' ').title()
                page_html = render_markdown_page(md_text, title)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page_html.encode('utf-8'))
                return
            ct = {
                '.js': 'application/javascript',
                '.css': 'text/css',
                '.json': 'application/json',
                '.svg': 'image/svg+xml',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
            }.get(ext, 'text/html')
            if ct == 'text/html':
                # Read the HTML, inject the back-button toolbar, then serve
                path = os.path.join(BASE_DIR, 'StudyNotes', rel)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
                    return
                content = inject_back_button(content)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return
            self.serve_file(os.path.join('StudyNotes', rel), ct)
        elif self.path == '/api/studynotes/data':
            data = read_json(STUDYNOTES_FILE)
            self.send_json(json.dumps(data, ensure_ascii=False))
        elif self.path == '/api/studynotes/files':
            studynotes_dir = os.path.join(BASE_DIR, 'StudyNotes')
            files = []
            for root, dirs, filenames in os.walk(studynotes_dir):
                for fn in sorted(filenames):
                    if fn.endswith('.html') or fn.endswith('.md'):
                        rel = os.path.relpath(os.path.join(root, fn), studynotes_dir).replace('\\', '/')
                        files.append(rel)
            self.send_json(json.dumps(files, ensure_ascii=False))
        elif self.path == '/favicon.svg':
            self.serve_file('favicon.svg', 'image/svg+xml')
        elif self.path in ('/apple-touch-icon.png', '/apple-touch-icon-precomposed.png'):
            self.serve_file('apple-touch-icon.png', 'image/png')
        elif self.path == '/api/assessments/data':
            data = read_json(ASSESSMENTS_FILE)
            self.send_json(json.dumps(normalize_assessments(data), ensure_ascii=False))
        elif self.path == '/api/homework/data':
            data = read_json(HOMEWORK_FILE)
            self.send_json(json.dumps(data, ensure_ascii=False))
        elif self.path == '/api/importantdates/data':
            data = read_json(IMPORTANT_DATES_FILE)
            self.send_json(json.dumps(data, ensure_ascii=False))
        elif self.path == '/api/todos/data':
            data = read_json(TODOS_FILE)
            if data.get('last_reset') != date.today().isoformat():
                reset_todos_if_new_day(data)
                write_json(TODOS_FILE, data)
            self.send_json(json.dumps(data, ensure_ascii=False))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        # ── Assessment routes ──────────────────────────────────────────────
        if self.path == '/api/assessments/add':
            data = read_json(ASSESSMENTS_FILE)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            date = body['date'].strip()
            text = body['assessment'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty assessment"}')
                return

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            item = {'text': text, 'status': body.get('status', 'Not Started'), 'due': body.get('date', '').strip(), 'notes': '', 'grade': body.get('grade', '')}
            if entry:
                entry['assessments'].append(item)
            else:
                weeks.append({'week': week_n, 'date': date, 'assessments': [item]})
                weeks.sort(key=lambda w: w['week'])

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/edit':
            data = read_json(ASSESSMENTS_FILE)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            text = body['assessment'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty assessment"}')
                return

            normalize_assessments(data)
            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['text'] = text
                if 'due' in body:
                    entry['assessments'][idx]['due'] = body['due'].strip()
                if 'grade' in body:
                    entry['assessments'][idx]['grade'] = body['grade']

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/update_grade':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            grade = body.get('grade', '')

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['grade'] = grade

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/update_status':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            status = body['status']

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['status'] = status

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/delete':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'].pop(idx)
                if not entry['assessments']:
                    data[student][term] = [w for w in weeks if w['week'] != week_n]

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/update_notes':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            notes = body.get('notes', '')

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['notes'] = notes

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        # ── Homework routes ────────────────────────────────────────────────
        elif self.path == '/api/homework/add':
            data = read_json(HOMEWORK_FILE)

            student = body['student']
            new_id = data['next_id']
            entry = {
                'id': new_id,
                'subject': body['subject'].strip(),
                'title': body['title'].strip(),
                'due': body['due'].strip(),
                'term': int(body['term']),
                'week': int(body['week']),
                'status': body.get('status', 'Not Started'),
                'notes': ''
            }
            if not entry['title']:
                self.send_json('{"ok": false, "error": "Empty title"}')
                return

            data[student].append(entry)
            data['next_id'] += 1

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/edit':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            for student in ('eddie', 'dara'):
                for entry in data[student]:
                    if entry['id'] == homework_id:
                        if 'subject' in body: entry['subject'] = body['subject'].strip()
                        if 'title' in body:   entry['title'] = body['title'].strip()
                        if 'due' in body:     entry['due'] = body['due'].strip()
                        if 'term' in body:    entry['term'] = int(body['term'])
                        if 'week' in body:    entry['week'] = int(body['week'])
                        if 'status' in body:  entry['status'] = body['status']
                        break

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/update_status':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            new_status = body['status']
            for student in ('eddie', 'dara'):
                for entry in data[student]:
                    if entry['id'] == homework_id:
                        entry['status'] = new_status
                        break

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/update_notes':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            notes = body.get('notes', '')
            for s in ('eddie', 'dara'):
                for entry in data[s]:
                    if entry['id'] == homework_id:
                        entry['notes'] = notes
                        break

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/delete':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            student = body['student']
            data[student] = [e for e in data[student] if e['id'] != homework_id]

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        # ── Todo routes ──────────────────────────────────────────────────
        elif self.path == '/api/todos/toggle':
            data = read_json(TODOS_FILE)
            reset_todos_if_new_day(data)

            student = body['student']
            period = body['period']
            idx = int(body['index'])

            items = data.get(student, {}).get(period, [])
            if 0 <= idx < len(items):
                items[idx]['checked'] = not items[idx]['checked']

            write_json(TODOS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/todos/add':
            data = read_json(TODOS_FILE)
            reset_todos_if_new_day(data)

            student = body['student']
            period = body['period']
            text = body['text'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty item"}')
                return

            data[student][period].append({'text': text, 'checked': False})

            write_json(TODOS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/todos/delete':
            data = read_json(TODOS_FILE)

            student = body['student']
            period = body['period']
            idx = int(body['index'])

            items = data.get(student, {}).get(period, [])
            if 0 <= idx < len(items):
                items.pop(idx)

            write_json(TODOS_FILE, data)
            self.send_json('{"ok": true}')

        # ── Study Notes routes ─────────────────────────────────────
        elif self.path == '/api/studynotes/add_link':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            title = body['title'].strip()
            url = body['url'].strip()
            if not title or not url:
                self.send_json('{"ok": false, "error": "Title and URL required"}')
                return
            for subj in data[student]['subjects']:
                if subj['name'] == subject_name:
                    if 'links' not in subj:
                        subj['links'] = []
                    subj['links'].append({'title': title, 'url': url})
                    break
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/delete_link':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            idx = int(body['index'])
            for subj in data[student]['subjects']:
                if subj['name'] == subject_name:
                    links = subj.get('links', [])
                    if 0 <= idx < len(links):
                        links.pop(idx)
                    break
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/add_aos':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body['name'].strip()
            if not aos_name:
                self.send_json('{"ok": false, "error": "Empty AOS name"}')
                return
            for subj in data[student]['subjects']:
                if subj['name'] == subject_name and 'aos' in subj:
                    subj['aos'].append({'name': aos_name, 'chapters': []})
                    break
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/add_chapter':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            title = body['title'].strip()
            file_path = body.get('file', '').strip()
            aos_name = body.get('aos', '')
            sub_name = body.get('subsection', '')
            if not title:
                self.send_json('{"ok": false, "error": "Empty title"}')
                return
            target = self._find_target(data, student, subject_name, aos_name, sub_name)
            if target is not None:
                if 'chapters' not in target:
                    target['chapters'] = []
                target['chapters'].append({'title': title, 'file': file_path})
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/delete_chapter':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body.get('aos', '')
            sub_name = body.get('subsection', '')
            idx = int(body['index'])
            target = self._find_target(data, student, subject_name, aos_name, sub_name)
            if target is not None:
                chapters = target.get('chapters', [])
                if 0 <= idx < len(chapters):
                    chapters.pop(idx)
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/add_quiz':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body['aos']
            sub_name = body.get('subsection', '')
            title = body['title'].strip()
            file_path = body.get('file', '').strip()
            if not title:
                self.send_json('{"ok": false, "error": "Empty title"}')
                return
            target = self._find_target(data, student, subject_name, aos_name, sub_name)
            if target is not None:
                if 'quizzes' not in target:
                    target['quizzes'] = []
                target['quizzes'].append({'title': title, 'file': file_path})
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/delete_quiz':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body['aos']
            sub_name = body.get('subsection', '')
            idx = int(body['index'])
            target = self._find_target(data, student, subject_name, aos_name, sub_name)
            if target is not None:
                quizzes = target.get('quizzes', [])
                if 0 <= idx < len(quizzes):
                    quizzes.pop(idx)
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/add_notes':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body['aos']
            sub_name = body.get('subsection', '')
            title = body['title'].strip()
            file_path = body.get('file', '').strip()
            if not title:
                self.send_json('{"ok": false, "error": "Empty title"}')
                return
            target = self._find_target(data, student, subject_name, aos_name, sub_name)
            if target is not None:
                if 'notes' not in target:
                    target['notes'] = []
                target['notes'].append({'title': title, 'file': file_path})
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/delete_notes':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body['aos']
            sub_name = body.get('subsection', '')
            idx = int(body['index'])
            target = self._find_target(data, student, subject_name, aos_name, sub_name)
            if target is not None:
                notes_list = target.get('notes', [])
                if 0 <= idx < len(notes_list):
                    notes_list.pop(idx)
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/studynotes/add_subsection':
            data = read_json(STUDYNOTES_FILE)
            student = body['student']
            subject_name = body['subject']
            aos_name = body['aos']
            name = body['name'].strip()
            if not name:
                self.send_json('{"ok": false, "error": "Empty name"}')
                return
            for subj in data[student]['subjects']:
                if subj['name'] == subject_name and 'aos' in subj:
                    for aos in subj['aos']:
                        if aos['name'] == aos_name:
                            if 'subsections' not in aos:
                                aos['subsections'] = []
                            aos['subsections'].append({'name': name, 'chapters': [], 'quizzes': []})
                            break
                    break
            write_json(STUDYNOTES_FILE, data)
            self.send_json('{"ok": true}')

        else:
            self.send_response(404)
            self.end_headers()

    def _find_target(self, data, student, subject_name, aos_name, sub_name):
        """Find the target dict (aos or subsection) to add/remove chapters/quizzes."""
        for subj in data[student]['subjects']:
            if subj['name'] == subject_name:
                if 'aos' in subj and aos_name:
                    for aos in subj['aos']:
                        if aos['name'] == aos_name:
                            if sub_name and 'subsections' in aos:
                                for sub in aos['subsections']:
                                    if sub['name'] == sub_name:
                                        return sub
                                return None
                            return aos
                return subj
        return None

    def serve_file(self, filename, content_type):
        path = os.path.join(BASE_DIR, filename)
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            ct = content_type if content_type.startswith('image/') else content_type + '; charset=utf-8'
            self.send_header('Content-Type', ct)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # Suppress request logs


if __name__ == '__main__':
    # One-time migration: normalize assessments data and persist
    data = read_json(ASSESSMENTS_FILE)
    normalize_assessments(data)
    write_json(ASSESSMENTS_FILE, data)

    print(f"Server running at http://0.0.0.0:{PORT}/")
    print(f"Local: http://localhost:{PORT}/")
    HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
