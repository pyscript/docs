# Foreign Function Interface

The Foreign Function Interface (FFI) enables Python and JavaScript to
work together seamlessly. Python code can call JavaScript functions,
access browser APIs, and manipulate the DOM directly. JavaScript code
can call Python functions and access Python objects. This
interoperability is what makes PyScript possible.

PyScript provides a unified FFI through `pyscript.ffi` that works
consistently across both Pyodide and MicroPython interpreters. This
guide explains how to use the FFI to bridge between Python and
JavaScript when necessary.

!!! info

    PyScript also enables JavaScript to call into Python!

    Please see the [PyScript in JavaScript](./from_javascript.md) section
    of this user-guide for more information.

## When to use the FFI

The FFI is a low-level interface for situations where higher-level
abstractions don't suffice. Most of the time, you should prefer
`pyscript.web` for DOM manipulation, `pyscript.media` for device
access, and other purpose-built APIs. These modules use the FFI
internally whilst providing cleaner, more Pythonic interfaces.

Use the FFI directly when you need to work with JavaScript libraries
that don't have PyScript wrappers, access browser APIs not yet covered
by PyScript modules, or pass Python functions as callbacks to JavaScript
code.

For DOM manipulation specifically, always prefer `pyscript.web` over
direct FFI usage. The FFI examples in this guide focus on situations
where `pyscript.web` doesn't apply.

## Converting Python to JavaScript

The `to_js()` function converts Python objects into their JavaScript
equivalents:

```python
from pyscript.ffi import to_js


# Python dict becomes JavaScript object.
options = {"title": "Hello", "icon": "icon.png"}
js_options = to_js(options)

# Python list becomes JavaScript array.
numbers = [1, 2, 3, 4, 5]
js_array = to_js(numbers)
```

This conversion is essential when calling JavaScript APIs that expect
JavaScript objects rather than Python objects. The function handles the
translation automatically, converting dictionaries to JavaScript objects
(not Maps), lists to arrays, and other common types appropriately.

!!! info

    PyScript's `to_js()` differs from Pyodide's version by defaulting
    to converting Python dictionaries into JavaScript objects rather
    than Maps. This matches what most JavaScript APIs expect and aligns
    with MicroPython's behaviour, providing consistency across
    interpreters.

## Creating function proxies

When passing Python functions to JavaScript, you must create a proxy to
prevent garbage collection:

```python
from pyscript.ffi import create_proxy
from pyscript import document


def handle_click(event):
    """
    Handle button clicks.
    """
    print("Button clicked!")


# Create a proxy for the JavaScript event listener.
button = document.getElementById("my-button")
button.addEventListener("click", create_proxy(handle_click))
```

Without `create_proxy()`, the Python function would be garbage collected
immediately, causing the event listener to fail. The proxy maintains a
reference, keeping the function alive for JavaScript to call.

!!! warning

    When using `pyscript.web` with the `@when` decorator, proxies are
    created automatically. You only need `create_proxy()` when working
    directly with JavaScript APIs.

## Checking for null values

JavaScript has both `null` and `undefined`. Python has `None`. The
`is_none()` function checks for both:

```python
from pyscript.ffi import is_none
from pyscript import js


value = js.document.getElementById("nonexistent")
if is_none(value):
    print("Element not found")
```

This handles the mismatch between Python's single null-like value and
JavaScript's multiple null-like values, providing consistent behaviour
across interpreters.

## Merging JavaScript objects

The `assign()` function merges JavaScript objects, similar to
`Object.assign()` in JavaScript:

```python
from pyscript.ffi import assign, to_js
from pyscript import js


# Create a base object.
options = js.Object.new()

# Merge in properties.
assign(options, {"width": 800}, {"height": 600})
```

This is useful when building configuration objects for JavaScript
libraries that expect objects built through mutation rather than created
whole.

## Accessing JavaScript globals

The `js` module provides access to JavaScript's global namespace:

```python
from pyscript import js


# Call JavaScript functions.
js.console.log("Hello from Python!")

# Access browser APIs.
js.alert("This is an alert")

# Create JavaScript objects.
date = js.Date.new()
print(date.toISOString())
```

Through `js`, you can access anything available in JavaScript's global
scope, including browser APIs, third-party libraries loaded via script
tags, and built-in JavaScript objects.

## Example: Task board with direct DOM manipulation

The task board example demonstrates FFI usage for direct DOM
manipulation, contrasting with the more Pythonic `pyscript.web`
approach:

<iframe src="../../example-apps/task-board-ffi/" style="border: 1px solid black; width:100%; min-height: 600px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-ffi).

This example intentionally uses the FFI directly rather than
`pyscript.web`, showing how to work with the DOM at a lower level when
necessary. Compare this to
[the `pyscript.web` version](../example-apps/task-board-web/info.md) to see why the
higher-level API is Pythonically preferable.

The FFI code creates elements, sets properties, and appends children
manually:

```python
from pyscript import document
from pyscript.ffi import create_proxy


# Create element.
task_div = document.createElement("div")
task_div.className = "task"
task_div.textContent = task_text

# Create button with event handler.
delete_btn = document.createElement("button")
delete_btn.textContent = "Delete"
delete_btn.addEventListener("click", create_proxy(delete_handler))

# Assemble the DOM.
task_div.appendChild(delete_btn)
container.appendChild(task_div)
```

This works, but `pyscript.web` would express the same logic more clearly,
Pythonically and with less boilerplate.

## Understanding interpreter differences

Pyodide and MicroPython implement JavaScript interop differently.
PyScript's FFI abstracts these differences, but understanding them helps
when debugging issues.

Pyodide provides comprehensive FFI features including detailed type
conversion control, whilst MicroPython offers a simpler, more
straightforward implementation. PyScript's unified FFI provides a
consistent interface that works reliably on both, defaulting to
sensible behaviours that match common use cases.

For interpreter-specific FFI features, access them through
`pyodide.ffi` or `micropython.ffi` directly. However, this breaks
cross-interpreter compatibility and should only be done when absolutely
necessary.

## Worker context utilities

When working with workers, the FFI provides additional utilities for
cross-thread communication. The `direct`, `gather`, and `query`
functions help manage objects and data across thread boundaries. These
are advanced features covered in detail in the
[workers API docs](../api/workers.md) and are primarily relevant when building
complex multi-threaded applications.

## In summary

Prefer higher-level APIs when they exist. Use `pyscript.web` for DOM
work, `pyscript.media` for devices, and other purpose-built modules
rather than reaching for the FFI directly.

Create proxies for Python callbacks passed to JavaScript. Without
proxies, functions get garbage collected and event handlers fail.

Convert Python objects to JavaScript when calling browser APIs. Most
JavaScript functions expect JavaScript objects, not Python objects, so
use `to_js()` when passing dictionaries or complex data structures.

Handle null values correctly. JavaScript's `null` and `undefined` both
exist alongside Python's `None`, so use `is_none()` for reliable null
checking.

## What's next

Now that you understand the FFI, explore these related topics:

**[Architecture guide](architecture.md)** - provides technical details about
how PyScript implements workers using PolyScript and Coincident if you're
interested in the underlying mechanisms.

**[Workers](workers.md)** - Display content from background threads
(requires explicit `target` parameter).

**[Filesystem](filesystem.md)** - Learn more about the virtual
filesystem and how the `files` option works.

**[FFI](ffi.md)** - Understand how JavaScript modules integrate with
Python through the foreign function interface.

**[Offline](offline.md)** - Use PyScript while not connected to the internet.