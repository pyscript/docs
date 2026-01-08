# Task Board - pyscript.web Version

A task management application demonstrating the Pythonic `pyscript.web`
interface for DOM manipulation.

## What it demonstrates

- **Finding elements**: Using `web.page["id"]` and `web.page.find()`.
- **Creating elements**: Using `web.div()`, `web.button()`, etc.
- **Modifying attributes**: Setting `innerHTML`, `value`, `dataset`.
- **Working with classes**: Using `classes.add()`, `classes.remove()`.
- **Collections**: Iterating over elements with `.find()`.
- **Event handling**: Using `@when` decorator with web elements.

## Features

- Add tasks with text descriptions.
- Set priority levels (high, medium, low) with visual indicators.
- Mark tasks as complete with checkboxes.
- Filter tasks by status (all, active, completed).
- Delete tasks.
- Visual feedback with colours and styles.

## Files

- `index.html` - Page structure and styling.
- `main.py` - Application logic using pyscript.web.

## How it works

1. User enters task text and selects a priority level.
2. Clicking "Add Task" creates a new task object and re-renders.
3. Tasks are displayed with priority-based colour coding.
4. Checkboxes toggle completion status.
5. Filter buttons show different subsets of tasks.
6. Delete buttons remove tasks from the list.

All DOM manipulation uses `pyscript.web`'s Pythonic interface:
- Elements accessed via `web.page["id"]` (dictionary-style).
- Classes managed with set operations (`add`, `remove`).
- Elements created with function calls (`web.div()`).
- Events handled with `@when` decorator.

## Compare with FFI version

See the [FFI version](../task-board-ffi/) of this same application to
compare the Pythonic approach with direct JavaScript API calls.

## Running locally

Serve these files from a web server:

```bash
python3 -m http.server
```

Then open http://localhost:8000 in your browser.