# Terminal

Traditional Python development often happens in terminals where you run
scripts, interact with the REPL, and see output from `print()`
statements. PyScript brings this familiar environment to the browser
through a built-in terminal based on
[XTerm.js](https://xtermjs.org/).

This guide explains how to use PyScript's terminal for output, input,
and interactive Python sessions in your browser applications.

## Basic terminal output

Enable the terminal by adding the `terminal` attribute to your script
tag:

```html title="Hello world (in a terminal)."
<script type="py" terminal>
print("hello world")
</script>
```

This creates a read-only terminal displaying your program's output.
Output appears in a terminal window on your page, familiar to anyone
who's used Python in a traditional environment.

<img src="../../assets/images/pyterm1.png" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

The terminal captures standard output, so all `print()` statements write
to it automatically. This works with both Pyodide and MicroPython.

## Interactive input

To accept user input with the `input()` function, you must run your code
in a worker. Interactive terminals require workers to handle blocking
input without freezing the page:

```html title="Use a worker for blocking input."
<script type="py" terminal worker>
name = input("What is your name? ")
print(f"Hello, {name}")
</script>
```

The `worker` attribute ensures input operations don't block the main
thread. Users can type into the terminal, and your code receives their
input through the familiar `input()` function.

<img src="../../assets/images/pyterm2.gif" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

Without the worker, interactive input would freeze your page. The worker
keeps the UI responsive whilst waiting for user input.

## Interactive REPL

For an interactive Python REPL session, use Python's `code` module:

```python title="Start an interactive REPL in the terminal."
import code

code.interact()
```

This starts a full Python REPL in the terminal where users can type
Python expressions and see results immediately:

<img src="../../assets/images/pyterm3.gif" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

The REPL provides command history, tab completion, and all the features
you'd expect from a traditional Python interactive session. This is
particularly useful for educational applications or debugging tools.

## Programmatic control

You can send code to the terminal programmatically from JavaScript. Give
your script an ID, then call the `process()` method:

```html title="Use JavaScript to send Python to the terminal."
<script id="my-terminal" type="mpy" terminal worker></script>

<script>
// From JavaScript, send Python code to the terminal.
const term = document.querySelector("#my-terminal");
await term.process('print("Hello from JavaScript!")');
</script>
```

This lets you build interfaces where buttons or other controls trigger
Python execution in the terminal, useful for tutorials or interactive
demonstrations.

## Customising the terminal

Each terminal provides access to the underlying XTerm.js Terminal
instance through the `__terminal__` reference in Python or the
`terminal` property in JavaScript.

### Changing appearance

Customise terminal appearance through XTerm.js options:

```html title="Customise appearances."
<script type="py" terminal worker>
from pyscript import ffi

# Change the font.
__terminal__.options = ffi.to_js({"fontFamily": "monospace"})

print("Custom font terminal")
</script>
```

This accesses [XTerm.js's full configuration API](https://xtermjs.org/docs/),
letting you adjust colours, fonts, cursor styles, and other visual properties.

### Resizing

Control terminal dimensions programmatically:

```python title="Resize the terminal."
if '__terminal__' in locals():
    __terminal__.resize(60, 10)  # (width, height)
```

This adjusts terminal size dynamically, useful when building responsive
interfaces or compact terminal displays.

### Clearing output

Clear the terminal programmatically:

```html title="Clear output."
<script type="mpy" terminal worker>
print("This will disappear")
__terminal__.clear()
print("This remains")
</script>
```

Only output after the clear appears in the terminal.

### Colours and formatting

The terminal supports ANSI escape codes for text formatting:

```html title="Terminal colour support."
<script type="mpy" terminal worker>
print("This is \033[1mbold\033[0m")
print("This is \033[32mgreen\033[0m")
print("This is \033[1m\033[35mbold and purple\033[0m")
</script>
```

Use standard terminal control sequences for bold text, colours, and
other formatting. This works like traditional terminal applications.

## XTerm.js addons

Extend terminal functionality using
[XTerm.js addons](https://xtermjs.org/docs/guides/using-addons/):

```html title="Using addons."
<py-config>
[js_modules.main]
"https://cdn.jsdelivr.net/npm/@xterm/addon-web-links/+esm" = "weblinks"
</py-config>

<script type="py" terminal>
from pyscript import js_modules

addon = js_modules.weblinks.WebLinksAddon.new()
__terminal__.loadAddon(addon)

print("Visit https://pyscript.net/")
</script>
```

PyScript enables the WebLinksAddon by default, making URLs in terminal
output automatically clickable. You can load
[other addons](https://github.com/xtermjs/xterm.js/tree/master/addons/)
following the same pattern.

## MicroPython REPL features

MicroPython includes a comprehensive built-in REPL with several
convenience features:

Command history works through up and down arrows, letting you recall and
edit previous commands. Tab completion shows available variables and
object attributes when you press tab. Copy and paste works naturally for
both single commands and
[paste mode](https://docs.micropython.org/en/latest/reference/repl.html#paste-mode)
for multi-line code.

Control sequences like Ctrl+X work as expected, including paste mode
toggles and interrupt signals.

## Worker versus main thread

MicroPython terminals work in both environments with different
characteristics:

**Main thread terminals** delegate `input()` to the browser's native
`prompt()` dialog. This works but feels less integrated. Blocking code
like infinite loops can freeze your page, so avoid long-running
operations on the main thread.

**Worker terminals** provide proper `input()` support directly in the
terminal without blocking. Long-running code executes without freezing
the page. The UI stays responsive even during computation.

We recommend using the `worker` attribute for MicroPython terminals
unless you have specific reasons to use the main thread. Workers provide
a better user experience and prevent blocking issues.

## What's next

Now that you understand terminals, explore these related topics:

**[Editor](editor.md)** - Create interactive Python coding environments in
web pages with the built-in code editor.

**[PyGame](pygame-ce.md)** - Use PyGame-CE with PyScript, covering the
differences from traditional PyGame development and techniques for making
games work well in the browser.

**[PyScript in JavaScript](from_javascript.md)** - drive PyScript from the
world JavaScript. 

**[Plugins](plugins.md)** - Understand the plugin system, lifecycle hooks,
and how to write plugins that integrate with PyScript.