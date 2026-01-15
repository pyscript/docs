# PyScript Example Applications

This directory contains complete, working example applications
demonstrating PyScript features and capabilities. Each example
accompanies and is embedded within a specific section of the PyScript
documentation.

These applications show idiomatic PyScript patterns and best practices.
Use them as starting points for your own projects or learning resources
for understanding how PyScript works.

## Running the examples

Each example is self-contained with its own `index.html` file. To run
an application locally with Python (we'll use the "Pirate Translator" as
an example):

```sh
# Navigate to the example directory.
cd example_apps/pirate-translator

# Serve with any web server.
python -m http.server 8000

# Visit http://localhost:8000 in your browser.
```

**Sometimes an example uses web-workers, and these need the server to
respond with special headers.** The 
[`mini-coi` command](https://github.com/WebReflection/mini-coi) (which
uses [node.js](https://nodejs.org/en) under the hood) does the right
thing for you:

```sh
# Navigate to the worker-related project.
cd example_apps/prime-worker

# Serve the app with the correct headers.
npx mini-coi .

# Visit http://localhost:8080/ in your browser.
```

All examples use the latest PyScript release referenced in this
version of the docs. Check each example's `index.html` for the reference
to the specific version of PyScript in use.

## Available examples

### Beginning PyScript

**[Pirate Translator (Polyglot)](pirate-translator/info.md)** - A simple text transformation application that
demonstrates basic PyScript concepts: writing Python in HTML, handling
user input, and manipulating the DOM. This is the first example new
users encounter.

[Run the app](./pirate-translator/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/pirate-translator) |
[Beginning PyScript](../beginning-pyscript.md)

### DOM manipulation

**[Task Board (`pyscript.web`)](task-board-web/info.md)** - A task
management application using `pyscript.web`, PyScript's idiomatic API
for DOM manipulation. Shows how to create, modify, and remove elements
using Pythonic patterns along with element access, creating
elements with Python functions, event handlers, dynamic content updates.

[Run the app](./task-board-web/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-web) |
[The DOM](../user-guide/dom.md)

**[Task Board (FFI)](task-board-ffi/info.md)** - The same task management
application using the Foreign Function Interface (FFI) instead of
`pyscript.web`. Demonstrates direct JavaScript interoperability for cases
where `pyscript.web` isn't sufficient along with direct JavaScript object
access, `ffi.create_proxy` for event handlers, working with JavaScript
APIs, when to use FFI vs `pyscript.web`.

[Run the app](./task-board-ffi/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-ffi) |
[The DOM](../user-guide/dom.md) |
[The FFI](../user-guide/ffi.md)

### Events

**[Colour Picker](colour-picker/info.md)** - An interactive colour picker
demonstrating event handling patterns. Shows how to respond to user
interactions and update the interface based on input. Specific use of
event handlers via `pyscript.web`, handling multiple input types (sliders,
text), real-time updates, colour manipulation.

[Run the app](./colour-picker/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/colour-picker) |
[Events](../user-guide/events.md)

### Display

**[Display Demo](display-demo/info.md)** - A comprehensive demonstration of
PyScript's `display()` capabilities including basic types and HTML, custom
`_repr_html_()` methods for objects, displaying Pandas DataFrames as
formatted tables, creating Matplotlib plots (single and subplots),
incremental UI updates with `async`, appending vs replacing content. This
is how to present data and visualisations in the browser with PyScript.

[Run the app](./display-demo/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/display-demo) |
[Display](../user-guide/display.md)

### Workers

**[Prime Workers](prime-worker/info.md)** - A computationally intensive
application that finds prime numbers using workers to keep the interface
responsive. Includes both MicroPython and Pyodide implementations with an
optional NumPy comparison. Specifically, this code shows how to use web
workers for background computation, MicroPython vsPyodide performance,
worker-main thread communication, and responsive UI during computation.

[Run the app](./prime-worker/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/prime-worker) |
[Workers](../user-guide/workers.md)

### Filesystem

!!! warning

    This example application **only works on Chrome based browsers**.

**[Note Taker](note-taker/info.md)** - A simple note-taking application
that saves and loads data to/from the user's local filesystem. Shows file
operations and data persistence patterns via file-related I/O with `open()`,
reading and writing files, virtual filesystem concepts, mounting local
filesystems, permissions and user approvals, data persistence via the local
filesystem mounted to locations on the virtual filesystem.

[Run the app](./note-taker/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/note-taker) |
[Filesystems](../user-guide/filesystem.md)

### Media devices

**[Photobooth](photobooth/info.md)** - A webcam application demonstrating
media device access. Captures photos from the user's camera using the PyScript
media API. Demonstrates camera access with `pyscript.media`, requesting user
permissions, capturing still frames, canvas manipulation.

[Run the app](./photobooth/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/photobooth) |
[Media](../user-guide/media.md)

### PyGame

**[Bouncing Ball](bouncing-ball/info.md)** - A simple game demonstrating
PyGame-CE support in PyScript. Shows the classic bouncing ball with collision
detection running entirely in the browser. This shows idiomatic PyGame-CE
integration with PyScript, game loop with `await asyncio.sleep()`, loading
assets, basic game physics.

[Run the app](./bouncing-ball/index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/bouncing-ball) |
[PyGame Support](../user-guide/pygame-ce.md)

## Best practices demonstrated

All examples follow PyScript best practices:

**Idiomatic patterns** - Prefer `pyscript.web` over FFI unless FFI is
specifically needed (task-board-ffi allows you to compare and contrast
these approaches).

**Clear code** - Comprehensive comments explaining intent, meaningful
variable names, simple and direct implementations.

**Proper structure** - Separate concerns, use workers for heavy
computation, handle errors gracefully.

**Modern PyScript** - Use current APIs and patterns, avoid deprecated
features, follow the latest recommendations.

## Contributing examples

If you've built something useful with PyScript and think it would make a
good example, consider contributing it. Good example applications:

* Demonstrate specific PyScript features clearly.
* Are self-contained and easy to understand.
* Follow the established structure and style.
* Include comprehensive documentation.

## What's next

After exploring these examples, consult the
[PyScript user guide](../user-guide/index.md) for comprehensive documentation on
all features. The guide provides deeper explanations of concepts
demonstrated in these examples.

Visit [pyscript.net](https://pyscript.net) for additional resources,
community examples, and the latest PyScript news.

Join the [PyScript Discord](https://discord.gg/HxvBtukrg2) to discuss
examples, get help, and share your own creations with the community.