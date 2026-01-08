"""
Task Board application demonstrating the FFI.

Shows how to use JavaScript APIs directly from Python: querySelector,
createElement, classList, dataset, and addEventListener. Compare this
with the pyscript.web version to see the differences.
"""
from pyscript import document, when


# Track tasks with their DOM elements.
tasks = []
current_filter = "all"
selected_priority = "medium"


def update_visibility():
    """
    Update visibility of task elements based on current filter.
    """
    for task in tasks:
        if task["deleted"]:
            task["element"].style.display = "none"
            continue
        
        should_show = False
        if current_filter == "all":
            should_show = True
        elif current_filter == "active":
            should_show = not task["completed"]
        elif current_filter == "completed":
            should_show = task["completed"]
        
        task["element"].style.display = "flex" if should_show else "none"
    
    # Show empty state if no visible tasks.
    visible_count = sum(
        1 for t in tasks
        if not t["deleted"] and (
            current_filter == "all" or
            (current_filter == "active" and not t["completed"]) or
            (current_filter == "completed" and t["completed"])
        )
    )
    
    empty_state = document.getElementById("empty-state")
    if visible_count == 0:
        if not empty_state:
            empty = document.createElement("div")
            empty.id = "empty-state"
            empty.className = "empty-state"
            empty.textContent = "No tasks yet. Add one above!"
            document.getElementById("tasks").appendChild(empty)
    else:
        if empty_state:
            empty_state.remove()


def toggle_complete(event):
    """
    Toggle task completion status.
    """
    index = int(event.target.dataset.index)
    tasks[index]["completed"] = event.target.checked
    
    # Update visual state.
    task_element = tasks[index]["element"]
    if event.target.checked:
        task_element.classList.add("completed")
    else:
        task_element.classList.remove("completed")
    
    # Update visibility based on current filter.
    update_visibility()


def delete_task(event):
    """
    Mark a task as deleted.
    """
    index = int(event.target.dataset.index)
    tasks[index]["deleted"] = True
    
    # Update visibility.
    update_visibility()


@when("click", "#add-task-btn")
def add_task(event):
    """
    Add a new task when the button is clicked.
    """
    task_input = document.getElementById("task-input")
    text = task_input.value.strip()
    
    if not text:
        return
    
    # Create task object.
    task_index = len(tasks)
    
    # Create checkbox.
    checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.className = "checkbox"
    checkbox.checked = False
    checkbox.dataset.index = str(task_index)
    checkbox.addEventListener("change", toggle_complete)
    
    # Create task text.
    task_text = document.createElement("div")
    task_text.className = "task-text"
    task_text.textContent = text
    
    # Create delete button.
    delete_btn = document.createElement("button")
    delete_btn.className = "delete-btn"
    delete_btn.textContent = "Delete"
    delete_btn.dataset.index = str(task_index)
    delete_btn.addEventListener("click", delete_task)
    
    # Create task container.
    task_div = document.createElement("div")
    task_div.className = f"task {selected_priority}"
    task_div.appendChild(checkbox)
    task_div.appendChild(task_text)
    task_div.appendChild(delete_btn)
    
    # Add to DOM.
    document.getElementById("tasks").appendChild(task_div)
    
    # Add task to list.
    tasks.append({
        "text": text,
        "priority": selected_priority,
        "completed": False,
        "deleted": False,
        "element": task_div,
        "checkbox": checkbox
    })
    
    # Clear input.
    task_input.value = ""
    
    # Update visibility.
    update_visibility()


@when("keypress", "#task-input")
def handle_keypress(event):
    """
    Add task when Enter is pressed.
    """
    if event.key == "Enter":
        add_task(event)


@when("click", ".priority-btn")
def select_priority(event):
    """
    Select a priority level.
    """
    global selected_priority
    
    # Get all priority buttons.
    priority_btns = document.querySelectorAll(".priority-btn")
    
    # Remove selected class from all.
    for btn in priority_btns:
        btn.classList.remove("selected")
    
    # Add selected class to clicked button.
    event.target.classList.add("selected")
    
    # Update selected priority.
    selected_priority = event.target.dataset.priority


@when("click", ".filter-btn")
def filter_tasks(event):
    """
    Filter tasks by completion status.
    """
    global current_filter
    
    # Get all filter buttons.
    filter_btns = document.querySelectorAll(".filter-btn")
    
    # Remove active class from all.
    for btn in filter_btns:
        btn.classList.remove("active")
    
    # Add active class to clicked button.
    event.target.classList.add("active")
    
    # Update filter.
    current_filter = event.target.dataset.filter
    
    # Update visibility.
    update_visibility()


# Initial setup.
update_visibility()