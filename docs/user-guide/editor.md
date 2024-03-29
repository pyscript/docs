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

!!! info

    Notice that the interpreter type, and optional environment name is shown
    at the top right above the Python editor.

    Hovering over the Python editor reveals the "run" button.

Finally, the `target` attribute allows you to specify a node into which the
editor will be rendered:

```html title="Specify a target for the Python editor."
<script type="mpy-editor" target="editor">
  import sys
  print(sys.version)
</script>
<div id="editor"></div> <!-- will eventually contain the Python editor -->
```
