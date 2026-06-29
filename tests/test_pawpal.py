"""Basic Phase 2 + Phase 5 tests for the PawPal+ system."""

from datetime import date, timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_sets_completed_to_true():
    """Calling mark_complete() should flip completed from False to True."""
    task = Task("Morning walk", "08:00", 30, "high", "daily")

    assert task.completed is False  # starts off as not done

    task.mark_complete()

    assert task.completed is True  # now marked as done


def test_adding_task_increases_pet_task_count():
    """Adding a task to a pet should make its task list grow by one."""
    pet = Pet("Rex", "dog", 3)

    assert len(pet.tasks) == 0  # a new pet has no tasks yet

    pet.add_task(Task("Feed", "07:30", 10, "medium", "daily"))

    assert len(pet.tasks) == 1  # the task was added


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should order tasks earliest-first, not by insertion order."""
    owner = Owner("Sam")
    scheduler = Scheduler(owner)

    # Tasks created out of order on purpose.
    tasks = [
        Task("Dinner", "18:00", 15, "high", "daily"),
        Task("Morning walk", "08:00", 30, "high", "daily"),
        Task("Lunch feed", "12:00", 10, "medium", "daily"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)
    times = [task.time for task in sorted_tasks]

    assert times == ["08:00", "12:00", "18:00"]  # chronological order


def test_completing_daily_task_schedules_next_day():
    """Completing a daily task should add a new task due the next day."""
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.add_pet(pet)

    today = date.today().isoformat()
    walk = Task("Morning walk", "08:00", 30, "high", "daily", due_date=today)
    pet.add_task(walk)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(walk)

    # The original task is now marked complete.
    assert walk.completed is True

    # A second (recurring) task was added for the next day.
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    expected_date = (date.today() + timedelta(days=1)).isoformat()
    assert next_task.due_date == expected_date
    assert next_task.completed is False


def test_detect_conflicts_flags_overlapping_tasks():
    """Two tasks at the same time should produce at least one conflict."""
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.add_pet(pet)

    # Both tasks start at 08:00, so they clearly overlap.
    pet.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
    pet.add_task(Task("Backyard play", "08:00", 20, "low", "daily"))

    scheduler = Scheduler(owner)

    assert len(scheduler.detect_conflicts()) >= 1
    assert len(scheduler.conflict_warnings()) >= 1
