"""
A simple task board application demonstrating the FFI.

Shows how to use JavaScript APIs directly from Python: querySelector,
createElement, classList, dataset, and addEventListener. Compare this
with the pyscript.web version to see the differences.
"""
from pyscript import document, when


# Store all tasks in a list.
_TASKS = []
# Track which filter is active: "all", "active", or "completed".
_CURRENT_FILTER = "all"
# Track which priority level is selected for new tasks.
_SELECTED_PRIORITY = "medium"


def count_visible_tasks():
    """
    Count how many tasks should be shown with the current filter.
    
    Returns the number of tasks that match the current filter and
    haven't been deleted.
    """
    count = 0
    for task in _TASKS:
        # Skip deleted tasks.
        if task["deleted"]:
            continue
        # Check if task matches current filter.
        if _CURRENT_FILTER == "all":
            count += 1
        elif _CURRENT_FILTER == "active" and not task["completed"]:
            count += 1
        elif _CURRENT_FILTER == "completed" and task["completed"]:
            count += 1
    return count


def show_or_hide_empty_message():
    """
    Show "No tasks yet" message if there are no visible tasks.
    
    Removes the message if there are visible tasks. Uses direct
    JavaScript DOM APIs via the FFI.
    """
    visible = count_visible_tasks()
    # Try to find the empty state element (if it exists).
    empty_state = document.getElementById("empty-state")
    # Get the container for visible tasks.
    tasks_container = document.getElementById("tasks")
    if visible == 0:
        # Show empty message if not already shown.
        if not empty_state:
            # Create a new div element using JavaScript's createElement.
            empty = document.createElement("div")
            empty.id = "empty-state"
            empty.className = "empty-state"
            empty.textContent = "No tasks yet. Add one above!"
            # Add it to the tasks container.
            tasks_container.appendChild(empty)
    else:
        # Remove empty message if it exists.
        if empty_state:
            empty_state.remove()


def update_task_visibility():
    """
    Show or hide each task based on the current filter.
    
    Uses JavaScript's style.display property directly via the FFI to
    control visibility.
    """
    for task in _TASKS:
        # Always hide deleted tasks.
        if task["deleted"]:
            task["element"].style.display = "none"
            continue
        # A flag to indicate if this task should be visible.
        should_show = False
        if _CURRENT_FILTER == "all":
            should_show = True
        elif _CURRENT_FILTER == "active" and not task["completed"]:
            should_show = True
        elif _CURRENT_FILTER == "completed" and task["completed"]:
            should_show = True
        # Update the task element's visibility using JavaScript style API.
        if should_show:
            task["element"].style.display = "flex"
        else:
            task["element"].style.display = "none"
    # Update the empty state message.
    show_or_hide_empty_message()


def toggle_complete(event):
    """
    Handle checkbox clicks to mark tasks complete or incomplete.
    
    Uses JavaScript's classList API via the FFI to add/remove the
    "completed" class for visual styling.
    """
    # Get which task this checkbox belongs to.
    task_index = int(event.target.dataset.index)
    task = _TASKS[task_index]
    # Update completion status based on checkbox state.
    task["completed"] = event.target.checked
    # Update visual styling using JavaScript's classList API.
    if task["completed"]:
        task["element"].classList.add("completed")
    else:
        task["element"].classList.remove("completed")
    # Update which tasks are visible based on current filter.
    update_task_visibility()


def delete_task(event):
    """
    Handle delete button clicks to remove tasks.
    
    Marks the task as deleted (rather than removing it from the list)
    to preserve task indices, then updates visibility.
    """
    # Get which task this delete button belongs to.
    task_index = int(event.target.dataset.index)
    # Mark as deleted (but keep in list to preserve indices).
    _TASKS[task_index]["deleted"] = True
    # Update which tasks are visible.
    update_task_visibility()


@when("click", "#add-task-btn")
def add_task(event):
    """
    Add a new task when the Add Task button is clicked.
    
    Uses JavaScript's createElement, appendChild, and property setting
    APIs directly via the FFI to build the task element.
    """
    # Get the input element using JavaScript's getElementById.
    task_input = document.getElementById("task-input")
    text = task_input.value.strip()
    # Don't add empty tasks.
    if not text:
        return
    # This task's index in the tasks list.
    task_index = len(_TASKS)
    # Create checkbox using JavaScript's createElement.
    checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.className = "checkbox"
    checkbox.checked = False
    # Store the task index so we know which task this checkbox controls.
    checkbox.dataset.index = str(task_index)
    # Connect the checkbox to the toggle_complete function via JavaScript's
    # addEventListener.
    checkbox.addEventListener("change", toggle_complete)
    # Create the task text display.
    task_text = document.createElement("div")
    task_text.className = "task-text"
    task_text.textContent = text
    # Create the delete button.
    delete_btn = document.createElement("button")
    delete_btn.className = "delete-btn"
    delete_btn.textContent = "Delete"
    # Store the task index so we know which task to delete.
    delete_btn.dataset.index = str(task_index)
    # Connect the button to the delete_task function via JavaScript's
    # addEventListener.
    delete_btn.addEventListener("click", delete_task)
    # Create the task container and add all elements to it.
    task_div = document.createElement("div")
    task_div.className = f"task {_SELECTED_PRIORITY}"
    # Use JavaScript's appendChild to build the element hierarchy.
    task_div.appendChild(checkbox)
    task_div.appendChild(task_text)
    task_div.appendChild(delete_btn)
    # Add the task to the page using appendChild.
    tasks_container = document.getElementById("tasks")
    tasks_container.appendChild(task_div)
    # Store the task data in our tasks list.
    _TASKS.append({
        "text": text,
        "priority": _SELECTED_PRIORITY,
        "completed": False,
        "deleted": False,
        "element": task_div,
        "checkbox": checkbox
    })
    # Clear the input field for the next task.
    task_input.value = ""
    # Update which tasks are visible.
    update_task_visibility()


@when("keypress", "#task-input")
def handle_keypress(event):
    """
    Add a task when Enter key is pressed in the input field.
    
    This lets users quickly add tasks by typing and pressing Enter
    instead of clicking the Add Task button.
    """
    if event.key == "Enter":
        add_task(event)


@when("click", ".priority-btn")
def select_priority(event):
    """
    Handle priority button clicks to set priority for new tasks.
    
    Uses JavaScript's querySelectorAll and classList APIs via the FFI
    to manage button styling.
    """
    global _SELECTED_PRIORITY 
    # Find all priority buttons using JavaScript's querySelectorAll.
    priority_btns = document.querySelectorAll(".priority-btn")
    # Remove "selected" styling from all buttons using classList.
    for btn in priority_btns:
        btn.classList.remove("selected")
    # Add "selected" styling to the clicked button.
    event.target.classList.add("selected")
    # Update which priority will be used for new tasks.
    _SELECTED_PRIORITY = event.target.dataset.priority


@when("click", ".filter-btn")
def filter_tasks(event):
    """
    Handle filter button clicks to show all, active, or completed tasks.
    
    Uses JavaScript's querySelectorAll and classList APIs via the FFI
    to manage button styling and update which tasks are visible.
    """
    global _CURRENT_FILTER
    # Find all filter buttons using JavaScript's querySelectorAll.
    filter_btns = document.querySelectorAll(".filter-btn")
    # Remove "active" styling from all buttons using classList.
    for btn in filter_btns:
        btn.classList.remove("active")
    # Add "active" styling to the clicked button.
    event.target.classList.add("active")
    # Update the current filter setting.
    _CURRENT_FILTER = event.target.dataset.filter
    # Update which tasks are visible.
    update_task_visibility()


# Initial setup - check if we should show the empty state message.
update_task_visibility()