"""PawPal+ demo : builds some pets and tasks, then prints a daily plan."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Set up sample data and show what the Scheduler can do."""

    # 1. Create the owner.
    owner = Owner("Sam")

    # 2. Create two pets.
    rex = Pet("Rex", "dog", 3)
    bella = Pet("Bella", "cat", 5)

    # 3. Add the pets to the owner.
    owner.add_pet(rex)
    owner.add_pet(bella)

    # 4. Give each pet some tasks at different times.
    rex.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
    rex.add_task(Task("Dinner", "18:00", 15, "high", "daily"))
    bella.add_task(Task("Feed cat", "07:30", 10, "medium", "daily"))
    bella.add_task(Task("Vet appointment", "14:00", 60, "high", "once"))

    # 5. Build a scheduler for this owner.
    scheduler = Scheduler(owner)

    # 6. Print today's schedule, ordered by time.
    print("=" * 40)
    print("Today's Schedule")
    print("=" * 40)
    for task in scheduler.generate_daily_plan():
        status = "[x]" if task.completed else "[ ]"
        print(f"{status} {task.time}  {task.description:<18} ({task.priority})")

    # 7a. Show the same tasks sorted by priority (high first).
    print()
    print("=" * 40)
    print("Tasks by Priority")
    print("=" * 40)
    all_tasks = owner.get_all_tasks()
    for task in scheduler.sort_by_priority(all_tasks):
        print(f"- {task.description:<18} ({task.priority})")

    # 7b. Mark one task done, then list the tasks still pending.
    rex.tasks[0].mark_complete()  # Rex finished his morning walk
    print()
    print("=" * 40)
    print("Pending Tasks")
    print("=" * 40)
    for task in scheduler.filter_by_status(False):
        print(f"- {task.time}  {task.description}")


if __name__ == "__main__":
    main()
