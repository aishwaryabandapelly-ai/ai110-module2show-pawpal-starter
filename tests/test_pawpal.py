"""Basic Phase 2 tests for the PawPal+ system."""

from pawpal_system import Task, Pet


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
