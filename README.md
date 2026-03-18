# School Hub - Albert Park College 2026

A local web app for tracking **assessments** and **homework** for Eddie (Year 11) and Dara (Year 7) at Albert Park College.

---

## Quick Start

```bash
python start.py
```

This starts the server on **port 8080** and opens the launcher in your browser. From the launcher, click Eddie or Dara to open their task page in a new tab.

---

## Project Structure

```
GetClassroomTasks/
├── server.py                      # Unified server (port 8080)
├── start.py                       # Starts server and opens launcher
├── launcher.html                  # Home page - select Eddie or Dara
├── student.html                   # Per-student task page (assessments + homework)
├── Assessments/
│   └── assessments_data.json      # Assessment data
├── Homework/
│   └── homework_data.json         # Homework data
└── ClassroomScraper/              # Legacy Google Classroom scraper (kept for reference)
```

---

## How It Works

### Launcher (`/`)
The launcher page presents two cards - one for Eddie, one for Dara. Clicking either opens their task page in a new tab.

### Student Page (`/eddie` or `/dara`)

Each student has a single page that combines both **assessments** and **homework** in one unified table.

#### Timetable
A collapsible timetable section at the top of the page shows the student's weekly class schedule (Day / P1-P5). Click the header to expand or collapse.

#### Filters
- **Type toggle**: All / Assessments / Homework
- **Dropdowns**: Term, Week, Subject, Status

#### Table
Columns: **Type** | **Term** | **Week** | **Date Range** | **Due** | **Subject** | **Detail** | **Status** | **Actions**

- **Type** -badge indicating Assessment (green) or Homework (blue)
- **Date Range** -auto-computed from the term/week (e.g. "16-20 Mar")
- **Due** -the specific due date for the item
- **Status** -inline dropdown (Not Started / In Progress / Completed), saves immediately on change
- **Actions** -edit and delete buttons per row

#### Inline Editing
Click the pencil icon on any row to edit it in place. All fields become editable dropdowns/inputs:
- **Term/Week** -cascading dropdowns (changing term updates week options)
- **Due** -dropdown of weekday dates within the selected week
- **Subject** -dropdown of the student's subjects
- **Detail** -text input
- **Status** -dropdown

Press **Enter** to save, **Escape** to cancel, or use the tick/cross buttons.

If an assessment's term or week is changed, it is automatically moved to the new location.

#### Adding Items
Click the green **+ Add** button to reveal the add form. Select Assessment or Homework type, then fill in:
- **Term** (dropdown 1-4)
- **Week** (dropdown with date ranges)
- **Due** (dropdown of individual dates in the week)
- **Subject** (dropdown)
- **Detail/Title** (text input)
- **Status** (dropdown)

The form stays open after adding for quick entry of multiple items.

---

## Data Files

### Assessments (`Assessments/assessments_data.json`)

Organised by student, then term, then week:

```json
{
  "eddie": {
    "1": [
      {
        "week": 5,
        "date": "23 Feb",
        "assessments": [
          { "text": "Maths: GA 1", "status": "Not Started", "due": "23 Feb" }
        ]
      }
    ],
    "2": [], "3": [], "4": []
  },
  "dara": { "1": [], "2": [], "3": [], "4": [] }
}
```

### Homework (`Homework/homework_data.json`)

Flat list per student with auto-incrementing IDs:

```json
{
  "next_id": 3,
  "eddie": [
    { "id": 1, "subject": "English", "title": "Essay draft", "due": "27 Mar", "term": 1, "week": 9, "status": "In Progress" }
  ],
  "dara": []
}
```

---

## API Endpoints

All served by `server.py` on port 8080.

### Assessment Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/assessments/data` | Get all assessment data (auto-normalised) |
| POST | `/api/assessments/add` | Add assessment `{student, term, week, date, assessment, status}` |
| POST | `/api/assessments/edit` | Edit assessment text/due `{student, term, week, index, assessment, due}` |
| POST | `/api/assessments/update_status` | Update status `{student, term, week, index, status}` |
| POST | `/api/assessments/delete` | Delete assessment `{student, term, week, index}` |

### Homework Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/homework/data` | Get all homework data |
| POST | `/api/homework/add` | Add homework `{student, subject, title, due, term, week, status}` |
| POST | `/api/homework/edit` | Edit homework `{id, subject, title, due, term, week, status}` |
| POST | `/api/homework/update_status` | Update status `{id, status}` |
| POST | `/api/homework/delete` | Delete homework `{id, student}` |

---

## Known Subjects

| Eddie (Year 11) | Dara (Year 7) |
|-----------------|---------------|
| Accounting, Business Mgt, English, Maths, Physical Education, Pos Ed, Sociology | Digital Art, English, Food, French, Humanities, Leadership, Maths, Philosophy, Pos Ed, Science, Volleyball |

---

## Term Calendar 2026

| Term | Weeks | Dates |
|------|-------|-------|
| Term 1 | 10 weeks | 27 Jan - 2 Apr |
| Term 2 | 10 weeks | 20 Apr - 26 Jun |
| Term 3 | 10 weeks | 13 Jul - 18 Sep |
| Term 4 | 2+ weeks | 5 Oct - onwards |

---

## ClassroomScraper (Legacy)

The original system that scraped assignments directly from Google Classroom via Selenium. Kept in `ClassroomScraper/` for reference.

```bash
python ClassroomScraper/classroom_scraper.py eddie
python ClassroomScraper/classroom_scraper.py dara
python ClassroomScraper/server.py eddie
```

| File | Description |
|------|-------------|
| `classroom_scraper.py` | Scrapes assignments from Google Classroom via Selenium |
| `create_html.py` | Generates HTML views with timetable, Gantt chart, filters |
| `server.py` | Serves generated HTML with status persistence |
| `data/` | Scraped data, manual tasks, and status files |
| `config/config.properties` | Login credentials (not committed) |
