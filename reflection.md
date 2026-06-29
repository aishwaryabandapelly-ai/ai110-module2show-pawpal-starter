# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design shows PawPal+ as a simple object-oriented pet care scheduling system. The design connects four main classes: Owner, Pet, Task, and Scheduler. An Owner can have multiple Pets, each Pet can have multiple Tasks, and the Scheduler works with the Owner’s pet/task data to organize daily care activities. I kept the UML simple so the system would be easy to understand before adding more advanced scheduling logic.

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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
