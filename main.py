"""PawPal+ demo : builds some pets and tasks, then shows the smarter scheduler."""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_header(title):
    """Print a simple boxed section header."""
    print()
    print("=" * 40)
    print(title)
    print("=" * 40)


def main():
    """Set up sample data and show what the Scheduler can do."""

    # 1. Create the owner and two pets.
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    bella = Pet("Bella", "cat", 5)
    owner.add_pet(rex)
    owner.add_pet(bella)

    # 2. Add tasks deliberately OUT OF ORDER so sorting has work to do.
    rex.add_task(Task("Dinner", "18:00", 15, "high", "daily"))
    rex.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
    bella.add_task(Task("Vet appointment", "14:00", 60, "high", "once"))
    bella.add_task(Task("Feed cat", "07:30", 10, "medium", "daily"))
    # A second walk that overlaps with the 08:00 walk -> conflict.
    rex.add_task(Task("Backyard play", "08:15", 20, "low", "daily"))

    scheduler = Scheduler(owner)

    # 3. Sorting by time (Scheduler.sort_by_time).
    print_header("Today's Schedule (sorted by time)")
    for task in scheduler.generate_daily_plan():
        status = "[x]" if task.completed else "[ ]"
        print(f"{status} {task.time}  {task.description:<18} ({task.priority})")

    # 4. Sorting by priority (Scheduler.sort_by_priority).
    print_header("Tasks by Priority")
    for task in scheduler.sort_by_priority(owner.get_all_tasks()):
        print(f"- {task.description:<18} ({task.priority})")

    # 5. Filtering by pet (Scheduler.filter_by_pet).
    print_header("Rex's Tasks (filtered by pet)")
    for task in scheduler.filter_by_pet("Rex"):
        print(f"- {task.time}  {task.description}")

    # 6. Conflict detection (Scheduler.conflict_warnings).
    print_header("Conflict Check")
    warnings = scheduler.conflict_warnings()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No conflicts found.")

    # 7. Recurring tasks: completing a daily task schedules the next one.
    print_header("Recurring Task Demo")
    morning_walk = scheduler.filter_by_pet("Rex")[1]  # the 08:00 daily walk
    print(f"Completing '{morning_walk.description}' (due {morning_walk.due_date})...")
    follow_up = scheduler.mark_task_complete(morning_walk)
    if follow_up:
        print(f"-> Auto-scheduled next '{follow_up.description}' for {follow_up.due_date}")

    # 8. Filtering by status (Scheduler.filter_by_status) shows what's left.
    print_header("Pending Tasks (filtered by status)")
    for task in scheduler.sort_by_time(scheduler.filter_by_status(False)):
        print(f"- {task.due_date} {task.time}  {task.description}")


if __name__ == "__main__":
    main()
