"""
A simple task board application demonstrating the `pyscript.web` API.

Shows how to find elements, create elements, manipulate attributes,
work with CSS classes and styles, and handle events using the Pythonic
`pyscript.web` interface.
"""
from pyscript import when, web


# Store all tasks in this list.
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
    
    Removes the message if there are visible tasks.
    """
    # Get the number of visible tasks.
    visible = count_visible_tasks()
    # Try to find the empty state element (if it exists).
    empty_state = web.page["empty-state"]
    # Get the container for visibletasks.
    tasks_container = web.page["tasks"]
    if visible == 0:
        # Show empty message if not already shown.
        if not empty_state:
            empty = web.div(
                "No tasks yet. Add one above!",
                id="empty-state",
                classes=["empty-state"]
            )
            tasks_container.append(empty)
    else:
        # Remove empty message if it exists.
        if empty_state:
            empty_state._dom_element.remove()


def update_task_visibility():
    """
    Show or hide each task based on the current filter.
    
    Loops through all tasks and sets their display style based on
    whether they match the current filter ("all", "active", or
    "completed") and whether they've been deleted.
    """
    for task in _TASKS:
        # Always hide deleted tasks.
        if task["deleted"]:
            task["element"].style["display"] = "none"
            continue
        # A flag to indicate if this task should be visible.
        should_show = False
        if _CURRENT_FILTER == "all":
            should_show = True
        elif _CURRENT_FILTER == "active" and not task["completed"]:
            should_show = True
        elif _CURRENT_FILTER == "completed" and task["completed"]:
            should_show = True
        # Update the task element's visibility.
        if should_show:
            task["element"].style["display"] = "flex"
        else:
            task["element"].style["display"] = "none"
    # Update the empty state message.
    show_or_hide_empty_message()


def toggle_complete(event):
    """
    Handle checkbox clicks to mark tasks complete or incomplete.
    
    Reads the task index from the checkbox's data attribute, updates
    the task's completion status, and updates its visual styling.
    """
    # Get which task this checkbox belongs to.
    task_index = int(event.target.dataset.index)
    task = _TASKS[task_index]
    # Update completion status based on checkbox state.
    task["completed"] = event.target.checked
    # Update visual styling.
    if task["completed"]:
        task["element"].classes.add("completed")
    else:
        task["element"].classes.remove("completed")
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
    
    Creates a new task with a checkbox, text, and delete button, then
    adds it to both the tasks list and the page. Also ensures the checkbox
    and delete button are connected to their respective event handlers.
    """
    # Get the input element and its value.
    task_input = web.page["task-input"]
    text = task_input.value.strip()
    # Don't add empty tasks.
    if not text:
        return
    # This task's index in the tasks list.
    task_index = len(_TASKS)
    # Create the checkbox for marking complete.
    checkbox = web.input_(
        type="checkbox",
        classes=["checkbox"]
    )
    # Store the task index so we know which task this checkbox controls.
    checkbox.dataset.index = str(task_index)
    # Connect the checkbox to the toggle_complete function.
    when("change", checkbox)(toggle_complete)
    # Create the task text display.
    task_text = web.div(
        text,
        classes=["task-text"]
    )
    # Create the delete button.
    delete_btn = web.button(
        "Delete",
        classes=["delete-btn"]
    )
    # Store the task index so we know which task to delete.
    delete_btn.dataset.index = str(task_index)
    # Connect the button to the delete_task function.
    when("click", delete_btn)(delete_task)
    # Create the task container with all elements inside.
    task_div = web.div(
        checkbox,
        task_text,
        delete_btn,
        classes=["task", _SELECTED_PRIORITY]
    )
    # Add the task to the page.
    web.page["tasks"].append(task_div)
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
    
    Updates the visual state of priority buttons and sets which
    priority level will be used for the next task added.
    """
    global _SELECTED_PRIORITY
    # Find all priority buttons.
    priority_btns = web.page.find(".priority-btn")
    # Remove "selected" styling from all buttons.
    for btn in priority_btns:
        btn.classes.discard("selected")
    # Add "selected" styling to the clicked button.
    event.target.classList.add("selected")
    # Update which priority will be used for new tasks.
    _SELECTED_PRIORITY = event.target.dataset.priority


@when("click", ".filter-btn")
def filter_tasks(event):
    """
    Handle filter button clicks to show all, active, or completed tasks.
    
    Updates the visual state of filter buttons and updates which tasks
    are visible based on the selected filter.
    """
    global _CURRENT_FILTER
    # Find all filter buttons.
    filter_btns = web.page.find(".filter-btn")
    # Remove "active" styling from all buttons.
    for btn in filter_btns:
        btn.classes.discard("active")
    # Add "active" styling to the clicked button.
    event.target.classList.add("active")
    # Update the current filter setting.
    _CURRENT_FILTER = event.target.dataset.filter
    # Update which tasks are visible.
    update_task_visibility()


# Initial setup - check if we should show the empty state message.
update_task_visibility()