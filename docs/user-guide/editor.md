# Python editor 

The PyEditor is a core plugin.

!!! warning

    Work on the Python editor is in its early stages. We have made it available
    in this version of PyScript to give the community an opportunity to play,
    experiment and provide feedback.

    Future versions of PyScript will include a more refined, robust and perhaps
    differently behaving version of the Python editor.

If you specify the type of a `<script>` tag as either `py-editor` (for Pyodide)
or `mpy-editor` (for MicroPython), the plugin creates a visual code editor,
with code highlighting and a "run" button to execute the editable code
contained therein in a non-blocking worker.

!!! info

    Once clicked, the "run" button will show a spinner until the code is
    executed. This may not be visible if the code evaluation completed quickly.


The interpreter is not loaded onto the page until the run button is clicked. By
default each editor has its own independent instance of the specified
interpreter:

```html title="Two editors, one with Pyodide, the other with MicroPython."
<script type="py-editor">
  import sys
  print(sys.version)
</script>
<script type="mpy-editor">
  import sys
  print(sys.version)
  a = 42
  print(a)
</script>
```

However, different editors can share the same interpreter if they share the
same `env` attribute value.

```html title="Two editors sharing the same MicroPython environment."
<script type="mpy-editor" env="shared">
  if not 'a' in globals():
    a = 1
  else:
    a += 1
  print(a)
</script>
<script type="mpy-editor" env="shared">
  # doubled a
  print(a * 2)
</script>
```

The outcome of these code fragments should look something like this:

<img src="../../assets/images/pyeditor1.gif" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

!!! info

    Notice that the interpreter type, and optional environment name is shown
    at the top right above the Python editor.

    Hovering over the Python editor reveals the "run" button.

### Setup

Sometimes you need to create a pre-baked Pythonic context for a shared
environment used by an editor. This need is especially helpful in educational
situations where boilerplate code can be run, with just the important salient
code available in the editor.

To achieve this end use the `setup` attribute within a `script` tag. The
content of this editor will not be shown, but will bootstrap the referenced
environment automatically before any following editor within the same
environment is evaluated.

```html title="Bootstrapping an environment with `setup`"
<script type="mpy-editor" env="test_env" setup>
# This code will not be visible, but will run before the next editor's code is
# evaluated.
a = 1
</script>

<script type="mpy-editor" env="test_env">
# Without the "setup" attribute, this editor is visible. Because it is using
# the same env as the previous "setup" editor, the previous editor's code is
# always evaluated first.
print(a)
</script>
```

Finally, the `target` attribute allows you to specify a node into which the
editor will be rendered:

```html title="Specify a target for the Python editor."
<script type="mpy-editor" target="editor">
  import sys
  print(sys.version)
</script>
<div id="editor"></div> <!-- will eventually contain the Python editor -->
```

## Editor VS Terminal

The editor and terminal are commonly used to embed interactive Python code into
a website. However, there are differences between the two plugins, of which you
should be aware.

The main difference is that a `py-editor` or `mpy-editor` is an isolated
environment (from the rest of PyScript that may be running on the page) and
its code always runs in a web worker. We do this to prevent accidental blocking
of the main thread that would freeze your browser's user interface.

Because an editor is isolated from regular *py* or *mpy* scripts, one should
not expect the same behavior regular *PyScript* elements follow, most notably:

  * The editor's user interface is based on
    [CodeMirror](https://codemirror.net/) and not on XTerm.js
    [as it is for the terminal](../terminal).
  * Code is evaluated all at once and asynchronously when the *Run* button is
    pressed (not each line at a time, as in the terminal).
  * The editor has listeners for `Ctrl-Enter` or `Cmd-Enter`, and
    `Shift-Enter` to shortcut the execution of all the code. These shortcuts
    make no sense in the terminal as each line is evaluated separately.
  * There is a clear separation between the code and any resulting output.
  * You may not use blocking calls (like `input`) with the editor, whereas
    these will work if running the terminal via a worker.
  * It's an editor! So simple or complex programs can be fully written without
    running the code until ready. In the terminal, code is evaluated one line
    at a time as it is typed in.
  * There is no special reference to the underlying editor instance, while
    there is both `script.terminal` or `__terminal__` in the terminal.

## Read / Write / Execute

Sometimes you need to programatically read, write or execute code in an
editor. Once PyScript has started, every py-editor/mpy-editor script tag gets
a `code` accessor attached to it.

```python
from pyscript import document

# Grab the editor script reference.
editor = document.querySelector('#editor')

# Output the live content of the editor.
print(editor.code)

# Update the live content of the editor.
editor.code = """
a = 1
b = 2
print(a + b)
"""

# Evaluate the live code in the editor.
# This could be any arbitrary code to evaluate in the editor's Python context.
editor.process(editor.code)
```

## Configuration

Unlike `<script type="py">` or `<py-script>` (and the `mpy` equivalents), a
PyEditor is not influenced by the presence of `<py-config>` elements in the
page: it requires an explicit `config="..."` attribute.

If a `setup` editor is present, that's the only PyEditor that needs a config.
Any subsequent related editor will reuse the config parsed and bootstrapped for
the `setup` editor.

## Run via keyboard

Depending on your operating system, a combination of either `Ctrl-Enter`,
`Cmd-Enter` or `Shift-Enter` will execute the code in the editor (no need to
move the mouse to click the run button).

## Override run

Sometimes you just need to override the way the editor runs code.

The editor's `handleEvent` can be overridden to achieve this:

```html title="Overriding execution via handleEvent."
<script type="mpy-editor" id="foreign">
print(6 * 7)
</script>

<script type="mpy">
from pyscript import document

def handle_event(event):
    # will log `print(6 * 7)`
    print(event.code)
    # prevent default execution
    return False

# Grab reference to the editor
foreign = document.getElementById("foreign")
# Override handleEvent with your own customisation.
foreign.handleEvent = handle_event
</script>
```

This
[live example](https://agiammarchi.pyscriptapps.com/pyeditor-iot-example/latest/)
shows how the editor can be used to execute code via a USB serial connection to
a connected MicroPython microcontroller.

## Tab behavior

We currently trap the `tab` key in a way that reflects what a regular code
editor would do: the code is simply indented, rather than focus moving to
another element.

We are fully aware of the implications this might have around accessibility so
we followed
[this detailed advice from Codemirror's documentation](https://codemirror.net/examples/tab/)
We have an *escape hatch* to move focus outside the editor. Press `esc` before
`tab` to move focus to the next focusable element. Otherwise `tab` indents
code.


## Still missing

The PyEditor is currently under active development and refinement, so features
may change (depending on user feedback). For instance, there is currently no
way to stop or kill a web worker that has got into difficulty from the editor
(hint: refreshing the page will reset things).
