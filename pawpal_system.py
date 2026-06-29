"""PawPal+ : a simple pet care management system."""

from dataclasses import dataclass, field
from typing import List

# Lower number = more important. Used when sorting tasks by priority.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self):
        """Return True if this task repeats (e.g. daily or weekly)."""
        return self.frequency.lower() not in ("once", "one-time", "")

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
        """Return pairs of tasks whose scheduled times overlap."""
        tasks = self.sort_by_time(self.owner.get_all_tasks())
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                start_i = _time_to_minutes(tasks[i].time)
                end_i = start_i + tasks[i].duration
                start_j = _time_to_minutes(tasks[j].time)
                if start_j < end_i:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def generate_daily_plan(self):
        """Return all of the owner's tasks ordered by time."""
        return self.sort_by_time(self.owner.get_all_tasks())

    def mark_task_complete(self, task):
        """Mark a given task as completed."""
        task.mark_complete()
