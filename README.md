# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```text
========================================
Today's Schedule
========================================
[ ] 07:30  Feed cat           (medium)
[ ] 08:00  Morning walk       (high)
[ ] 14:00  Vet appointment    (high)
[ ] 18:00  Dinner             (high)

========================================
Tasks by Priority
========================================
- Morning walk       (high)
- Dinner             (high)
- Vet appointment    (high)
- Feed cat           (medium)

========================================
Pending Tasks
========================================
- 18:00  Dinner
- 07:30  Feed cat
- 14:00  Vet appointment

```text


======================================= test session starts =======================================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/aish/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 2 items

tests/test_pawpal.py ..                                                                     [100%]

======================================== 2 passed in 0.02s ========================================
```


```

## 📐 Smarter Scheduling

PawPal+ adds lightweight algorithms so the daily plan is organized, conflict-aware,
and self-maintaining.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting (by time) | `Scheduler.sort_by_time()` | Sorts `Task` objects by their `"HH:MM"` time using `sorted()` with a `key` lambda that converts the time string to minutes (`_time_to_minutes`). |
| Task sorting (by priority) | `Scheduler.sort_by_priority()` | Sorts high → medium → low via a `PRIORITY_ORDER` lookup. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Return tasks for a single pet, or only completed / pending tasks. |
| Conflict detection | `Scheduler.detect_conflicts()`, `Scheduler.conflict_warnings()` | `detect_conflicts()` flags same-day tasks whose times overlap (start + duration); `conflict_warnings()` turns each conflict into a printable warning string instead of crashing. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily/weekly task auto-creates the next instance. `next_occurrence()` uses `datetime.timedelta` to advance the `due_date` by 1 day (daily) or 7 days (weekly). |

### How it works

- **Sorting** — Times are strings like `"08:00"`, so they are converted to minutes
  since midnight before comparing. `sort_by_time(tasks)` returns a new sorted list.
- **Filtering** — `filter_by_pet("Rex")` walks the owner's pets; `filter_by_status(False)`
  returns every pending task across all pets.
- **Conflict detection** — For each pair of tasks on the same `due_date`, a conflict is
  reported when the later task starts before the earlier one ends. Warnings are returned
  as friendly strings, so the CLI and Streamlit UI can simply display them.
- **Recurring tasks** — When `mark_task_complete()` is called on a daily or weekly task,
  the scheduler builds its `next_occurrence()` (today + 1 day, or + 7 days) and adds that
  fresh, uncompleted task back to the same pet.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
