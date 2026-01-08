"""
Task Board application demonstrating pyscript.web.

Shows how to find elements, create elements, manipulate attributes,
work with classes and styles, and handle events using the Pythonic
pyscript.web interface.
"""
from pyscript import when, web


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
            task["element"].style["display"] = "none"
            continue
        
        should_show = False
        if current_filter == "all":
            should_show = True
        elif current_filter == "active":
            should_show = not task["completed"]
        elif current_filter == "completed":
            should_show = task["completed"]
        
        task["element"].style["display"] = "flex" if should_show else "none"
    
    # Show empty state if no visible tasks.
    visible_count = sum(
        1 for t in tasks
        if not t["deleted"] and (
            current_filter == "all" or
            (current_filter == "active" and not t["completed"]) or
            (current_filter == "completed" and t["completed"])
        )
    )
    
    empty_state = web.page["empty-state"]
    tasks_container = web.page["tasks"]
    
    if visible_count == 0:
        if not empty_state:
            empty = web.div(
                "No tasks yet. Add one above!",
                id="empty-state",
                classes=["empty-state"]
            )
            tasks_container.append(empty)
    else:
        if empty_state:
            empty_state._dom_element.remove()


def toggle_complete(event):
    """
    Toggle task completion status.
    """
    index = int(event.target.dataset.index)
    tasks[index]["completed"] = event.target.checked
    
    # Update visual state.
    task_element = tasks[index]["element"]
    if event.target.checked:
        task_element.classes.add("completed")
    else:
        task_element.classes.remove("completed")
    
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
    task_input = web.page["task-input"]
    text = task_input.value.strip()
    
    if not text:
        return
    
    # Create task object.
    task_index = len(tasks)
    
    # Create checkbox.
    checkbox = web.input(
        type="checkbox",
        classes=["checkbox"]
    )
    checkbox.dataset.index = str(task_index)
    checkbox._dom_element.addEventListener("change", toggle_complete)
    
    # Create task text.
    task_text = web.div(
        text,
        classes=["task-text"]
    )
    
    # Create delete button.
    delete_btn = web.button(
        "Delete",
        classes=["delete-btn"]
    )
    delete_btn.dataset.index = str(task_index)
    delete_btn._dom_element.addEventListener("click", delete_task)
    
    # Create task container.
    task_div = web.div(
        checkbox,
        task_text,
        delete_btn,
        classes=["task", selected_priority]
    )
    
    # Add to DOM.
    web.page["tasks"].append(task_div)
    
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
    priority_btns = web.page.find(".priority-btn")
    
    # Remove selected class from all.
    for btn in priority_btns:
        btn.classes.remove("selected")
    
    # Add selected class to clicked button.
    event.target.classes.add("selected")
    
    # Update selected priority.
    selected_priority = event.target.dataset.priority


@when("click", ".filter-btn")
def filter_tasks(event):
    """
    Filter tasks by completion status.
    """
    global current_filter
    
    # Get all filter buttons.
    filter_btns = web.page.find(".filter-btn")
    
    # Remove active class from all.
    for btn in filter_btns:
        btn.classes.remove("active")
    
    # Add active class to clicked button.
    event.target.classes.add("active")
    
    # Update filter.
    current_filter = event.target.dataset.filter
    
    # Update visibility.
    update_visibility()


# Initial setup.
update_visibility()