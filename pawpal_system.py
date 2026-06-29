"""PawPal+ : a simple pet care management system."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List

# Lower number = more important. Used when sorting tasks by priority.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# How many days forward a recurring task jumps for each frequency.
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


def _time_to_minutes(time_str):
    """Convert a 'HH:MM' time string into minutes since midnight."""
    hours, minutes = time_str.split(":")
    return int(hours) * 60 + int(minutes)


@dataclass
class Task:
    """A single pet care task. Time should be written in 'HH:MM' 24-hour format."""

    description: str
    time: str
    duration: int
    priority: str
    frequency: str
    completed: bool = False
    # Defaults to today (ISO 'YYYY-MM-DD') so existing positional calls still work.
    due_date: str = field(default_factory=lambda: date.today().isoformat())

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self):
        """Return True if this task repeats (e.g. daily or weekly)."""
        return self.frequency.lower() not in ("once", "one-time", "")

    def next_occurrence(self):
        """Build the next instance of a recurring task.

        Uses ``timedelta`` to advance ``due_date`` by one day for a daily task
        or seven days for a weekly task. Returns a fresh, uncompleted ``Task``
        for that next date, or ``None`` if the task does not recur.
        """
        step = RECURRENCE_DAYS.get(self.frequency.lower())
        if step is None:
            return None
        next_date = date.fromisoformat(self.due_date) + timedelta(days=step)
        return Task(
            description=self.description,
            time=self.time,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
            due_date=next_date.isoformat(),
        )

    def display_task(self):
        """Print a friendly summary of this task."""
        status = "done" if self.completed else "pending"
        print(f"{self.time} - {self.description} ({self.priority}, {status})")


@dataclass
class Pet:
    """A pet that has its own list of care tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def remove_task(self, task_description):
        """Remove a task from this pet by its description."""
        self.tasks = [t for t in self.tasks if t.description != task_description]


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_name):
        """Remove a pet from this owner by its name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self):
        """Return all tasks across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Organizes and plans an owner's pet care tasks."""

    def __init__(self, owner):
        """Create a scheduler for a given owner."""
        self.owner = owner

    def sort_by_time(self, tasks):
        """Return tasks sorted by their scheduled time."""
        return sorted(tasks, key=lambda t: _time_to_minutes(t.time))

    def sort_by_priority(self, tasks):
        """Return tasks sorted by their priority (high first)."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority.lower(), 99))

    def filter_by_pet(self, pet_name):
        """Return tasks that belong to a specific pet."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.tasks
        return []

    def filter_by_status(self, completed):
        """Return tasks that match the given completed status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self):
        """Return pairs of tasks on the same day whose times overlap.

        Two tasks conflict when they fall on the same ``due_date`` and the
        later one starts before the earlier one ends (start time + duration).
        Tasks on different dates never conflict.
        """
        tasks = self.sort_by_time(self.owner.get_all_tasks())
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].due_date != tasks[j].due_date:
                    continue
                start_i = _time_to_minutes(tasks[i].time)
                end_i = start_i + tasks[i].duration
                start_j = _time_to_minutes(tasks[j].time)
                if start_j < end_i:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def conflict_warnings(self):
        """Return a friendly warning string for each detected conflict.

        This is the "lightweight" view of :meth:`detect_conflicts`: instead of
        raising or returning raw task pairs, it hands back human-readable
        warnings the UI (or CLI) can simply print.
        """
        warnings = []
        for first, second in self.detect_conflicts():
            warnings.append(
                f"⚠️  Conflict on {first.due_date}: "
                f"'{first.description}' ({first.time}) overlaps with "
                f"'{second.description}' ({second.time})."
            )
        return warnings

    def generate_daily_plan(self):
        """Return all of the owner's tasks ordered by time."""
        return self.sort_by_time(self.owner.get_all_tasks())

    def _find_pet_for_task(self, task):
        """Return the Pet that owns this exact task object, or None."""
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                return pet
        return None

    def mark_task_complete(self, task):
        """Mark a task complete and auto-schedule its next occurrence.

        When the task recurs (daily or weekly), a fresh instance is created for
        the next due date and added to the same pet's task list. Returns the
        newly created follow-up ``Task``, or ``None`` for one-time tasks.
        """
        task.mark_complete()
        if not task.is_recurring():
            return None
        follow_up = task.next_occurrence()
        if follow_up is None:
            return None
        owning_pet = self._find_pet_for_task(task)
        if owning_pet is not None:
            owning_pet.add_task(follow_up)
        return follow_up
