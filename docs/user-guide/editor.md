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

!!! info

    Notice that the interpreter type, and optional environment name is shown
    at the top right above the Python editor.

    Hovering over the Python editor reveals the "run" button.

Finally, it is possible to specify a target node into which the code editor is
created:

```html title="Specify a target for the Python editor."
<script type="mpy-editor" target="editor">
  import sys
  print(sys.version)
</script>
<div id="editor"></div> <!-- will eventually contain the Python editor -->
```
