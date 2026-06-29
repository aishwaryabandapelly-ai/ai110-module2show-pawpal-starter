# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design shows PawPal+ as a simple object-oriented pet care scheduling system. The design connects four main classes: Owner, Pet, Task, and Scheduler. An Owner can have multiple Pet objects, each Pet can have multiple Task objects, and the Scheduler works with the owner’s pet and task data to organize daily care activities. I kept the UML simple so the system would be easy to understand before adding more advanced scheduling logic.

- What classes did you include, and what responsibilities did you assign to each?

I included four main classes in my design. The Owner class stores owner information and manages the list of pets. The Pet class stores details about each pet, such as name, species, and age, and keeps track of that pet’s care tasks. The Task class represents one pet care activity, such as feeding, walking, medication, grooming, or an appointment, with details like time, duration, priority, frequency, and completion status. The Scheduler class is responsible for organizing tasks, sorting them, filtering them, detecting conflicts, and helping generate a daily care plan.

**b. Design changes**

- Did your design change during implementation?

Yes, my design changed slightly during implementation. My original UML design had the right overall structure with Owner, Pet, Task, and Scheduler, so I did not change the main class relationships. However, as I moved from design to code, I realized the Scheduler needed more practical logic to support the project requirements, such as sorting tasks, prioritizing tasks, filtering by status, detecting conflicts, and generating a daily plan.

- If yes, describe at least one change and why you made it.

One change I made was giving the Scheduler class more responsibility. Instead of only storing an Owner object, it now includes methods such as sort_by_time(), sort_by_priority(), filter_by_pet(), filter_by_status(), detect_conflicts(), and generate_daily_plan(). I made this change because PawPal+ needs to produce a daily plan based on task time, duration, priority, and owner constraints. I also added helper logic like _time_to_minutes() and PRIORITY_ORDER so tasks can be sorted correctly instead of staying in the order they were added.After reviewing Claude’s feedback, I did not make major structural changes because the class separation was already clean. I only noted that task times should use the "HH:MM" format, since _time_to_minutes() depends on that format.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers three main constraints: the time of day a task is scheduled
("HH:MM"), the task's duration in minutes, and its priority (high, medium, or low). Time
and duration are used together to build the daily plan in order and to detect conflicts
when two tasks on the same day overlap. Priority is used to let the owner re-sort their
tasks so the most important care activities (like medication or feeding) stand out. I
also track each task's frequency (once, daily, weekly) so recurring tasks can be handled.

- How did you decide which constraints mattered most?

I decided time mattered most because a pet owner's day is organized around when things
need to happen, so sorting and conflict detection both depend on it. Priority came next,
because when the day gets busy the owner needs to know what to do first. I treated
duration as a supporting constraint that mostly matters for conflict detection. I kept
"preferences" out for now to avoid over-engineering, since the core scheduling problem
was really about ordering tasks and avoiding overlaps.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My conflict detector only flags tasks that fall on the **same calendar day** and
compares them using each task's start time plus its duration. It does **not** account
for buffer/travel time between tasks, and it assumes no task crosses midnight. In other
words, a 30-minute walk at 08:00 and another task at 08:15 are correctly flagged as
overlapping, but a task ending at 08:00 and one starting at 08:00 are treated as fine
even though a real owner might need a few minutes in between. I chose the simpler
"start + duration overlap, same day" rule over a full interval-tree or gap-aware model.

- Why is that tradeoff reasonable for this scenario?

For a single pet owner planning a handful of daily tasks, the lightweight O(n²) overlap
check is fast, easy to read, and easy to verify by hand. The edge cases it skips
(buffer time, midnight-spanning tasks) are rare for everyday pet care and would add
real complexity for little practical benefit, so a clear warning message is more useful
here than a perfectly precise scheduling engine.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used Claude as a collaborator across every phase. Early on it helped me brainstorm the
class design (Owner, Pet, Task, Scheduler) and think through responsibilities for each
class. During the logic phase it helped me plan small algorithms like sorting "HH:MM"
times, filtering tasks, detecting conflicts, and handling recurring tasks with
`timedelta`. It also helped me connect the logic to the Streamlit UI in `app.py` and
write the automated tests. To stay organized, I used separate chats for design,
algorithms, testing, and documentation so each conversation stayed focused.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were specific and scoped, like "how do I sort tasks in HH:MM
format using a lambda key" or "give me a lightweight conflict detection strategy that
returns a warning instead of crashing." Asking for a short list of options, and asking
"how could this be simpler or more readable," gave me choices I could evaluate instead of
one big block of code I had to accept blindly.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

There were a few times I limited or rejected suggestions that felt over-engineered. For
example, for conflict detection I chose the simple "start + duration overlap on the same
day" approach instead of a more complex interval/gap-aware model, because the simpler
version was easier to read and good enough for one owner's daily tasks. I made similar
calls to keep the code beginner-friendly rather than adding features the project didn't
need yet.

- How did you evaluate or verify what the AI suggested?

I verified suggestions by running them myself rather than trusting them on sight. I ran
`main.py` to watch the CLI output (sorted schedule, conflict warning, and a recurring
task being re-created for the next day) and I ran `python -m pytest` to confirm the
automated tests passed. When something looked too clever, I asked for a simpler version
and compared readability before deciding which to keep.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested five core behaviors: (1) marking a task complete updates its completion status,
(2) adding a task to a pet increases that pet's task list, (3) tasks are sorted into
chronological order, (4) completing a daily recurring task creates the next occurrence
for the following day, and (5) conflict detection flags overlapping tasks.

- Why were these tests important?

These tests cover the main promises of the app. If sorting, recurrence, or conflict
detection silently broke, the daily plan would be wrong or misleading, which defeats the
purpose of a scheduling assistant. Testing them with automated tests means I can change
the code later and quickly confirm I didn't break the core behavior.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am fairly confident (about ⭐⭐⭐⭐☆). The main task-management and scheduling behaviors
are covered by passing automated tests, and I also verified the same logic by hand
through the CLI demo and the Streamlit UI.

- What edge cases would you test next if you had more time?

I would add tests for invalid time formats, empty pet schedules, that a non-recurring
("once") task does not respawn when completed, and tasks that cross midnight. These are
the cases most likely to expose gaps in my current simple approach.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the smarter scheduling logic came together and stayed
readable. Sorting, filtering, conflict warnings, and recurring tasks all live in the
`Scheduler` and `Task` classes with clear method names, and they're visible in both the
CLI and the Streamlit table. It feels like a small system that actually does something
useful instead of just storing data.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would make conflict detection smarter by accounting for buffer/travel time between
tasks and tasks that cross midnight, and I'd let the recurrence logic generate a longer
horizon of upcoming tasks rather than just the next one. I'd also add a "mark complete"
button in the Streamlit UI so users can trigger recurrence directly from the app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

My biggest takeaway is that AI can suggest a lot of code, but I still had to act as the
lead architect and decide what actually belonged in the project. Keeping separate chats
for design, algorithms, testing, and documentation kept the work organized, and
verifying every suggestion by running it myself was what turned AI's ideas into a system
I understood and could stand behind.
