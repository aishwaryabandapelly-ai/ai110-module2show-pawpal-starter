import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan and organize your pets' daily care tasks.")

# Keep one Owner in session_state so data survives Streamlit's reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.divider()

# --- Add a pet -------------------------------------------------------------
st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=2)
    add_pet = st.form_submit_button("Add pet")

    if add_pet:
        owner.add_pet(Pet(pet_name, species, int(age)))
        st.success(f"Added {pet_name} to your pets!")

st.divider()

# --- Schedule a task -------------------------------------------------------
st.subheader("Schedule a Task")

if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task_form"):
        # Let the user pick which pet this task belongs to.
        pet_names = [pet.name for pet in owner.pets]
        chosen_pet_name = st.selectbox("For which pet?", pet_names)

        description = st.text_input("Task description", value="Morning walk")
        task_time = st.time_input("Time")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task = st.form_submit_button("Add task")

        if add_task:
            # Find the Pet object that matches the chosen name.
            selected_pet = None
            for pet in owner.pets:
                if pet.name == chosen_pet_name:
                    selected_pet = pet

            task = Task(
                description,
                task_time.strftime("%H:%M"),
                int(duration),
                priority,
                frequency,
            )
            selected_pet.add_task(task)
            st.success(f"Scheduled '{description}' for {chosen_pet_name}!")

st.divider()

# --- Today's schedule ------------------------------------------------------
st.subheader("Today's Schedule")

scheduler = Scheduler(owner)
daily_plan = scheduler.generate_daily_plan()  # tasks sorted by time

if not daily_plan:
    st.info("No tasks yet. Add a pet and schedule a task to see the plan.")
else:
    # Look up which pet each task belongs to, for a clearer table.
    task_owner = {}
    for pet in owner.pets:
        for task in pet.tasks:
            task_owner[id(task)] = pet.name

    # Build one clean table row per task (already sorted by time).
    rows = []
    for task in daily_plan:
        rows.append(
            {
                "Status": "✅" if task.completed else "⬜",
                "Time": task.time,
                "Task": task.description,
                "Pet": task_owner.get(id(task), "—"),
                "Priority": task.priority,
                "Frequency": task.frequency,
            }
        )
    st.table(rows)

    # Surface any scheduling conflicts as warnings rather than crashing.
    warnings = scheduler.conflict_warnings()
    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts — your day is clear! 🐾")
