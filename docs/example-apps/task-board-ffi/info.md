# Task Board - FFI Version

The same task management application as the pyscript.web version, but
implemented using the FFI (foreign function interface) with direct
JavaScript API calls.

## What it demonstrates

- **Finding elements**: Using `document.getElementById()` and
  `document.querySelectorAll()`.
- **Creating elements**: Using `document.createElement()`.
- **Modifying attributes**: Setting properties like `textContent`,
  `className`, `checked`.
- **Working with classes**: Using `classList.add()`,
  `classList.remove()`.
- **Collections**: Iterating over NodeLists from `querySelectorAll()`.
- **Event handling**: Using `@when` decorator with CSS selectors.

## Comparing with pyscript.web

This is the exact same application as the
[pyscript.web version](../task-board-web/), but implemented using
JavaScript APIs directly. Key differences:

### Finding elements

**pyscript.web**: `web.page["tasks"]`

**FFI**: `document.getElementById("tasks")`

### Creating elements

**pyscript.web**:
```python
task_div = web.div(
    checkbox,
    task_text,
    delete_btn,
    classes=["task", priority]
)
```

**FFI**:
```python
task_div = document.createElement("div")
task_div.className = f"task {priority}"
task_div.appendChild(checkbox)
task_div.appendChild(task_text)
task_div.appendChild(delete_btn)
```

### Working with classes

**pyscript.web**: `element.classes.add("selected")`

**FFI**: `element.classList.add("selected")`

### Setting content

**pyscript.web**: `element.innerHTML = "text"`

**FFI**: `element.textContent = "text"` or `element.innerHTML = "text"`

## Which approach to use?

Both work perfectly! The pyscript.web version is more Pythonic and
concise, whilst the FFI version gives you direct access to JavaScript
APIs. Choose based on your preference and familiarity with web
development.

## Files

- `index.html` - Page structure and styling (same as web version).
- `main.py` - Application logic using FFI.

## Running locally

Serve these files from a web server:

```bash
python3 -m http.server
```

Then open http://localhost:8000 in your browser.