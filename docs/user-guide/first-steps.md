# First steps

It's simple:

* tell your browser to use PyScript, then,
* tell PyScript how to run your Python code.

That's it!

For the browser to use PyScript, simply add a `<script>` tag, whose `src`
attribute references a CDN url for `pyscript.core`, to your HTML document's
`<head>`. We encourage you to add a reference to optional PyScript related
CSS:

```html title="Reference PyScript in your HTML"
<!doctype html>
<html>
    <head>
        <!-- Recommended meta tags -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <!-- PyScript CSS -->
        <link rel="stylesheet" href="https://pyscript.net/releases/2024.6.2/core.css">
        <!-- This script tag bootstraps PyScript -->
        <script type="module" src="https://pyscript.net/releases/2024.6.2/core.js"></script>
    </head>
    <body>
        <!-- your code goes here... -->
    </body>
</html>
```

There are two ways to tell PyScript how to find your code.

* With a standard HTML `<script>` tag whose `type` attribute is either `py`
  (for Pyodide) or `mpy` (for MicroPython). **This is the recommended way**.
* Via the bespoke `<py-script>` (Pyodide) and `<mpy-script>` (MicroPython)
  tags. Historically, `<py-script>` used to be the only way to reference your
  code.

These should be inserted into the `<body>` of your HTML document.

In both cases either use the `src` attribute to reference a Python
file containing your code, or inline your code between the opening and closing
tags. **We recommend you use the `src` attribute method**, but retain the
ability to include code between tags for convenience.

Here's a `<script>` tag with a `src` attribute containing a URL
pointing to a `main.py` Python file.

```html title="A &lt;script&gt; tag with a source file"
<script type="mpy" src="main.py"></script>
```

...and here's a `<py-script>` tag with inline Python code.

```html title="A &lt;py-script&gt; tag with inline code"
<py-script>
import sys
from pyscript import display


display(sys.version)
</py-script>
```

The `<script>` and `<py-script>` / `<mpy-script>` tags may have the following
attributes:

* `src` - the content of the tag is ignored and the Python code in the
  referenced file is evaluated instead. **This is the recommended way to
  reference your Python code.**
* `config` - your code will only be evaluated after the referenced
  [configuration](configuration.md) has been parsed. Since configuration can be
  JSON or a TOML file,
  `config='{"packages":["numpy"]}'` and `config="./config.json"` or
  `config="./config.toml"` are all valid.
* `async` - your Python code can contain a
  [top level await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await#top_level_await).
* `worker` - a flag to indicate your Python code is to be run on a
  [web worker](workers.md) instead of the "main thread" that looks after the user
  interface.
* `target` - The id or selector of the element where calls to
  [`display()`](builtins.md/#pyscriptdisplay) should write their values. 
* `terminal` - A traditional [terminal](terminal.md) is shown on the page.
  As with conventional Python, `print` statements output here. **If the
  `worker` flag is set the terminal becomes interactive** (e.g. use 
  the `input` statement to gather characters typed into the terminal by the
  user).

!!! warning

    The `packages` setting used in the example configuration shown above is
    **for Pyodide** using PyPI.

    When using MicroPython, and because MicroPython doesn't support code
    packaged on PyPI, you should use a valid URL to a _MicroPython friendly_
    package.

    For more information please refer to the [packages section](configuration.md/#packages) of
    this user guide.

!!! question

    Why do we recommend use of the `<script>` tag with a `src` attribute?

    Within the [HTML standard](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script),
    the `<script>` tag is used to embed executable code. Its use case
    completely aligns with our own, as does its default behaviour.

    By referencing a separate Python source file via the `src` attribute, your
    code is just a regular Python file your code editor will understand. Python
    code embedded within a `<script>` tag in an HTML file won't benefit from
    the advantages code editors bring: syntax highlighting, code analysis,
    language-based contextual awareness and perhaps even an AI co-pilot.

    Both the `<py-script>` and `<mpy-script>` tags with inline code are
    [web components](https://developer.mozilla.org/en-US/docs/Web/API/Web_Components)
    that are _not built into the browser_. While they are convenient, there is
    a performance cost to their use.

!!! info
    The browser's tab displaying the website running PyScript is an isolated
    computing sandbox. Define the Python environment in which your code will
    run with [configuration options](configuration.md) (discussed later in this
    document).

!!! tip 

    If you want to run code on both the main thread and in a worker, be
    explicit and use separate tags.

    ```html
    <script type="mpy" src="main.py"></script>  <!-- on the main thread -->
    <script type="py" src="worker.py" worker config="pyconfig.toml"></script> <!-- on the worker -->
    ```

    Notice how different interpreters can be used with different
    configurations.


