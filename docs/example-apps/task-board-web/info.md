# Task Board - pyscript.web Version

[Run the app](index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-web) 

A task management application demonstrating the Pythonic `pyscript.web`
interface for DOM manipulation.

## What it demonstrates

- Finding elements with `web.page["id"]` and `web.page.find()`.
- Creating elements using `web.div()`, `web.button()`, etc.
- Modifying attributes by setting `innerHTML`, `value`, `dataset`.
- Working with classes with `classes.add()`, `classes.remove()`.
- Collections via iterating over elements with `.find()`.
- Event handling using the `@when` decorator with web elements.

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

All DOM manipulation uses `pyscript.web`'s Pythonic interface:

- Elements accessed via `web.page["id"]` (dictionary-style).
- Classes managed with set operations (`add`, `remove`).
- Elements created with function calls (`web.div()`).
- Events handled with `@when` decorator.

## Compare with FFI version

See the [FFI version](../task-board-ffi/info.md) of this same application to
compare the Pythonic approach with direct JavaScript API calls.
