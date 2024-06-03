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

    Once clicked, the *Run* button will show a spinner until the code is executed. This might not be visible if the code took nothing to execute, but if the code took any measurable time longer, one will notice such spinner before results will be shown.


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

Behind the scene, we bootstrap an editor that provides:

  * highlights around the Python code in it
  * a Run button to execute the code
  * a `target` reference where the code output lands, once printed

This is all great and sound, but there is also a way to read the *editor* code, and update it with ease, that's the `code` accessor any editor gets, once bootstrapped:

```python
from pyscript import document

# grab the editor script reference
editor = document.querySelector('#editor')

# output its content
print(editor.code)

# or update its content
editor.code = """
a = 1
b = 2
print(a + b)
"""
```

To execute that new editor content a user might click the *Run* button one more time, or the driver of such editor can use `editor.process(editor.code)`, or any other arbitrary code, to actually bypass the need to click *Run* and execute the code passed along the `.process(...)` invoke.

These utilities are helpful to let consumers of the editor change its view state and/or execute it out the box.

## Config

Differently from `<script type="py">` or `<py-script>`, and the `mpy` counterpart, a *PyEditor* is not affected by the presence of `<py-config>` elements in the page: it requires an explicit `config="..."` attribute to specify its dependencies, behavior and whatnot.

If a `setup` editor is present though, that's the only *PyEditor* that needs a config, so that any further related editor will have already such config parsed and bootstrapped.

That is: do not expect `<py-config>` to dictate the behavior of a `py-editor`, these are *two different kind of custom script* so that an editor, when needed, must use a `config` attribute.


## Still missing

The PyEditor is currently under active development and refinement, so features
may change (depending on user feedback). For instance, there is currently no
way to stop or kill a web worker that has got into difficulty from the editor
(hint: refreshing the page will reset things).
