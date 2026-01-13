# Task Board - FFI Version

[Run the app](index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-ffi)

The same task management application as the pyscript.web version, but
implemented using the FFI (foreign function interface) with direct
JavaScript API calls.

## What it demonstrates

- Finding elements using the native `document.getElementById()` and
  `document.querySelectorAll()` functions.
- Creating elements with `document.createElement()`.
- Modifying attributes by setting properties like `textContent`,
  `className`, `checked` on JSProxy objects.
- Working with classes via `classList.add()`,
  `classList.remove()` (i.e. native APIs).
- Collections by iterating over NodeLists from `querySelectorAll()`.
- Event handling with the `@when` decorator with CSS selectors.

## Features

This is the exact same application as the
[pyscript.web version](../task-board-web/), but implemented using
JavaScript APIs directly. Key differences:

## Files

- `index.html` - Page structure and styling (same as the `pyscript.web`
  version).
- `main.py` - Application logic using the FFI.

## How it works

Both versions of the app work just fine! The `pyscript.web` version is more
Pythonic and concise, whilst the FFI version gives you direct access to JavaScript
APIs. Choose based on your preference and familiarity with web development.

We've tried to compare and contrast the two approaches below:

### Finding elements

pyscript.web:

```python
web.page["tasks"]
```

FFI:

```python
document.getElementById("tasks")
```

### Creating elements

pyscript.web:

```python
task_div = web.div(
    checkbox,
    task_text,
    delete_btn,
    classes=["task", priority]
)
```

FFI:

```python
task_div = document.createElement("div")
task_div.className = f"task {priority}"
task_div.appendChild(checkbox)
task_div.appendChild(task_text)
task_div.appendChild(delete_btn)
```

### Working with classes

pyscript.web:

```python
element.classes.add("selected")
```

FFI:

```python
element.classList.add("selected")
```

### Setting content

pyscript.web:

```python
element.innerHTML = "text"
```

FFI:

```python
element.textContent = "text"
```

or

```python
element.innerHTML = "text"
```
