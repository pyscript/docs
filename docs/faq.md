# Frequently Asked Questions

This page addresses common questions and troubleshooting scenarios
encountered by the PyScript community on
[Discord](https://discord.gg/HxvBtukrg2), in
[community calls](https://www.youtube.com/@PyScriptTV), and through
general usage.

The FAQ covers two main areas: [common errors](#common-errors) and
[helpful hints](#helpful-hints).

## Common errors

### Reading error messages

When your application doesn't run and you see no error messages on the
page, check
[your browser's console](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools).

The last line of an error message usually reveals the problem:

```text
Traceback (most recent call last):
  File "/lib/python311.zip/_pyodide/_base.py", line 501, in eval_code
    .run(globals, locals)
     ^^^^^^^^^^^^^^^^^^^^
  File "/lib/python311.zip/_pyodide/_base.py", line 339, in run
    coroutine = eval(self.code, globals, locals)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 1, in <module>
NameError: name 'failure' is not defined
```

```text
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'failure' isn't defined
```

Both examples show a
[`NameError`](https://docs.python.org/3/library/exceptions.html#NameError)
because the name `failure` doesn't exist. Everything above the error
message provides potentially useful technical detail for debugging.

These are the most common errors PyScript users encounter.

### SharedArrayBuffer

This is the most common error new PyScript users face:

!!! failure

    Your application doesn't run and your browser console shows:

    ```
    Unable to use `window` or `document` -> https://docs.pyscript.net/latest/faq/#sharedarraybuffer
    ```

#### When

This error occurs when code running in a worker tries to access `window`
or `document` objects that exist on the main thread.

The error indicates either **your web server is incorrectly configured**
or **a `service-worker` attribute is missing from your script element**.

Specifically, one of three situations applies:

Your web server configuration prevents the browser from enabling Atomics
(a technology for cross-thread communication). When your script element
has a `worker` attribute and your Python code uses `window` or
`document` objects that exist on the main thread, this browser
limitation causes failure unless you reconfigure your server.

You're using `<script type="py-editor">` (which always runs in a worker)
without providing a fallback via a `service-worker` attribute on that
element.

You've explicitly created a `PyWorker` or `MPWorker` instance somewhere
in your code without providing a `service_worker` fallback.

The [workers guide](./user-guide/workers.md) documents all these cases
with code examples and solutions.

#### Why

For `document.getElementById('some-id').value` to work in a worker,
JavaScript requires two primitives:

[SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)
allows multiple threads to read and write shared memory.

[Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics)
provides `wait(sab, index)` and `notify(sab, index)` to coordinate
threads, where `sab` is a SharedArrayBuffer.

Whilst a worker waits for a main thread operation, it doesn't consume
CPU. It idles until the referenced buffer index changes, effectively
never blocking the main thread whilst pausing its own execution.

These primitives make worker-main thread communication seamless for
developers. We encourage using workers over running Python on the main
thread, especially with Pyodide, because workers keep the user interface
responsive during heavy computation.

Unfortunately, we cannot patch or work around these primitives - they're
defined by web standards. However, various solutions exist for working
within these limitations. The [workers guide](./user-guide/workers.md)
explains how.

### Borrowed proxy

This common error occurs with event listeners, timers, or anywhere
JavaScript lazily invokes a Python callback:

!!! failure

    Your browser console shows:

    ```
    Uncaught Error: This borrowed proxy was automatically destroyed at the end of a function call.
    Try using create_proxy or create_once_callable.
    For more information about the cause of this error, use `pyodide.setDebug(true)`
    ```

#### When

This error happens when using Pyodide on the main thread and passing a
bare Python function as a JavaScript callback:

```python
import js

# This throws the error.
js.setTimeout(lambda msg: print(msg), 1000, "FAIL")
```

The garbage collector immediately cleans up the Python function after
passing it to JavaScript. For the function to work as a future callback,
it must not be garbage collected - hence the error.

!!! info

    This error doesn't occur when code executes in a worker and the
    JavaScript reference comes from the main thread:

    ```python
    from pyscript import window

    # This works fine in a worker.
    window.setTimeout(lambda x: print(x), 1000, "OK")
    ```

    Proxy objects cannot be communicated between a worker and the main
    thread. Behind the scenes, PyScript ensures references are
    maintained between workers and the main thread. Worker-based Python
    functions appear as JavaScript proxy objects on the main thread,
    avoiding the borrowed proxy problem.

Two solutions exist:

Manually wrap functions with
[`pyscript.ffi.create_proxy`](./api/ffi.md#pyscript.ffi.create_proxy):

```python
from pyscript import ffi, window

window.setTimeout(
    ffi.create_proxy(print),
    100,
    "print"
)
```

Or set
[`experimental_create_proxy = "auto"`](./user-guide/configuration.md#experimental_create_proxy)
in your configuration. This intercepts Python objects passed to
JavaScript callbacks and manages memory automatically via JavaScript's
garbage collector.

!!! note

    [FinalizationRegistry](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry)
    enables automatic memory management. It's not observable and you
    cannot predict when it frees proxy objects. Memory consumption might
    be slightly higher than manual `create_proxy`, but JavaScript's
    engine manages memory efficiently and frees retained proxies when
    memory pressure increases.

#### Why

Pyodide and MicroPython both have garbage collectors for automatic
memory management. When Python object references pass to JavaScript via
the FFI, Python interpreters cannot guarantee JavaScript's garbage
collector will free them. They may lose control since there's no
reliable way to know when JavaScript no longer needs the objects.

One solution expects users to explicitly create and destroy proxy
objects. But manual memory management defeats automatic collection and
risks dead references - destroying Python objects still active in
JavaScript. This creates difficulty.

Pyodide provides
[ffi.wrappers](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#module-pyodide.ffi.wrappers)
for common cases. PyScript's `experimental_create_proxy = "auto"`
configuration automates memory management via `FinalizationRegistry`.

### Python packages

Sometimes Python packages specified via
[`packages` configuration](./user-guide/configuration.md#packages) don't
work with PyScript's interpreters.

!!! failure

    **Using Pyodide**: Your browser console shows:

    ```
    ValueError: Can't find a pure Python 3 wheel for: 'package_name'
    ```

!!! failure

    **Using MicroPython**: Your browser console shows:

    ```
    Cross-Origin Request Blocked: The Same Origin Policy disallows reading the
    remote resource at https://micropython.org/pi/v2/package/py/package_name/latest.json.
    (Reason: CORS header 'Access-Control-Allow-Origin' missing).
    Status code: 404.
    ```

#### When

This is a complicated problem, but the summary is:

First, check you've used the correct package name. This is a remarkably
common mistake worth verifying first.

In Pyodide, the error indicates the package contains code written in C,
C++, or Rust. These compiled languages haven't been compiled for
WebAssembly. The Pyodide project and
[Python Packaging Authority](https://www.pypa.io/en/latest/) are working
to make WebAssembly a default compilation target. Until then, follow
[Pyodide's guidance](https://pyodide.org/en/stable/usage/faq.html#why-can-t-micropip-find-a-pure-python-wheel-for-a-package)
to overcome this limitation.

In MicroPython, the package hasn't been ported to the
[`micropython-lib` repository](https://github.com/micropython/micropython-lib).
To use pure Python packages with MicroPython, use the
[files configuration](./user-guide/configuration.md#files) to manually
copy the package onto the filesystem, or reference it via URL.

The [packaging pointers](#packaging-pointers) section provides hints and
tips about packaging with PyScript.

#### Why

Pyodide and MicroPython are different Python interpreters running in
WebAssembly. Packages built for Pyodide may not work for MicroPython,
and vice versa. Furthermore, packages containing compiled code may not
have been compiled for WebAssembly.

If a package is written in Python that both interpreters support (subtle
differences exist between them), you should be able to use it by getting
it into the Python path via configuration.

Currently, MicroPython cannot expose modules requiring native
compilation, but PyScript is working with the MicroPython team to
provide builds including commonly requested packages (like MicroPython's
versions of `numpy` or `sqlite`).

!!! warning

    Depending on complexity, seamlessly porting from Pyodide to
    MicroPython may be difficult. MicroPython has
    [comprehensive documentation](https://docs.micropython.org/en/latest/genrst/index.html)
    explaining differences from "regular" CPython (the version Pyodide
    provides).

### JavaScript modules

When [using JavaScript modules](./user-guide/dom.md#the-ffi-javascript-interoperability)
you may encounter these errors:

!!! failure

    Uncaught SyntaxError: The requested module './library.js' does not provide an export named 'default'

!!! failure

    Uncaught SyntaxError: The requested module './library.js' does not provide an export named 'util'

#### When

These errors occur because the JavaScript module isn't written as a
standards-compliant JavaScript module.

To solve this, various content delivery networks provide automatic
conversion to standard ESM (ECMAScript Modules). We recommend
[esm.run](https://esm.run/):

```html
<mpy-config>
[js_modules.main]
"https://esm.run/d3" = "d3"
</mpy-config>

<script type="mpy">
from pyscript.js_modules import d3
</script>
```

Alternatively, ensure referenced JavaScript code uses `export` or
request an `.mjs` version. The
[user guide](./user-guide/dom.md#the-ffi-javascript-interoperability) covers all
options and technical considerations for using JavaScript modules.

#### Why

Although the JavaScript module standard has existed since 2015, many
libraries still produce files incompatible with modern standards.

This reflects the JavaScript ecosystem's evolution rather than a
technical limitation. Developers are learning the new standard and
migrating legacy code from obsolete patterns.

While legacy code exists, JavaScript may require special handling.

### Possible deadlock

This error message indicates a serious problem:

!!! failure

    ```
    💀🔒 - Possible deadlock if proxy.xyz(...args) is awaited
    ```

#### When

This error occurs when code on a worker and the main thread are in
[deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science)).
Neither fragment can proceed without waiting for the other.

#### Why

Consider this worker code:

```python
from pyscript import sync

sync.worker_task = lambda: print('🔥 this is fine 🔥')

# Deadlock occurs here. 💀🔒
sync.main_task()
```

And this main thread code:

```html
<script type="mpy">
from pyscript import PyWorker


async def main_task():
    # Deadlock occurs here. 💀🔒
    await pw.sync.worker_task()


pw = PyWorker("./worker.py", {"type": "pyodide"})
pw.sync.main_task = main_task
</script>
```

The main thread calls `main_task()`, which awaits `worker_task()` on the
worker. But `worker_task()` can only execute after `main_task()`
completes. Neither can proceed - classic deadlock.

PyScript detects this situation and raises the error to prevent your
application from freezing.

#### Solution

Restructure your code to avoid circular dependencies between main thread
and worker. One thread should complete its work before the other begins,
or they should work independently without waiting for each other.

### TypeError: crypto.randomUUID is not a function

This error appears in specific browser environments:

!!! failure

    ```
    TypeError: crypto.randomUUID is not a function
    ```

#### When

This occurs when using PyScript in environments where the
`crypto.randomUUID` API isn't available. This typically happens in:

Older browsers not supporting this API.

Non-secure contexts (HTTP instead of HTTPS). The `crypto.randomUUID`
function requires a secure context.

Certain embedded browser environments or WebViews with restricted APIs.

#### Solution

Use HTTPS for your application. The `crypto` API requires secure
contexts.

Update to modern browsers supporting the full Web Crypto API.

If working in a restricted environment, you may need to polyfill
`crypto.randomUUID` or use an alternative approach for generating unique
identifiers.

## Helpful hints

This section provides guidance on common scenarios and best practices.

### PyScript `latest`

When including PyScript in your HTML, you can reference specific
versions or use `latest`:

```html
<!-- Specific version (recommended for production). -->
<script type="module" src="https://pyscript.net/releases/2025.11.2/core.js"></script>

<!-- Latest version (useful for development). -->
<script type="module" src="https://pyscript.net/latest/core.js"></script>
```

#### Production vs development

For production applications, always use specific version numbers. This
ensures your application continues working even when new PyScript
versions are released. Updates happen on your schedule, not
automatically.

For development and experimentation, `latest` provides convenient access
to new features without updating version numbers.

#### Version compatibility

When reporting bugs or asking questions, always mention which PyScript
version you're using. Different versions may behave differently, and
version information helps diagnose problems.

Check the [releases page](https://github.com/pyscript/pyscript/releases)
to see available versions and their release notes.

### Workers via JavaScript

You can create workers programmatically from JavaScript:

```html
<script type="module">
import { PyWorker } from "https://pyscript.net/releases/2025.11.2/core.js";

const worker = new PyWorker("./worker.py", {type: "pyodide"});

// Call Python functions from JavaScript.
await worker.sync.python_function();
</script>
```

This approach is useful when:

You're building primarily JavaScript applications that need Python
functionality.

You want dynamic worker creation based on runtime conditions.

You're integrating PyScript into existing JavaScript frameworks.

The worker runs Python code in a separate thread, keeping your main
thread responsive. Use `worker.sync` to call Python functions from
JavaScript, and vice versa through `pyscript.window`.

### JavaScript `Class.new()`

When creating JavaScript class instances from Python, use the `.new()`
method:

```python
from pyscript import window

# Create a new Date instance.
date = window.Date.new()

# Create other class instances.
map_instance = window.Map.new()
set_instance = window.Set.new()
```

This pattern exists because Python's `Date()` would attempt to call the
JavaScript class as a function rather than constructing an instance.

The `.new()` method explicitly invokes JavaScript's `new` operator,
ensuring proper class instantiation.

### PyScript events

PyScript dispatches custom events throughout the application lifecycle.
You can listen for these events to coordinate behaviour:

```html
<script type="module">
document.addEventListener('py:ready', (event) => {
    console.log('Python interpreter ready');
    console.log('Script:', event.detail.script);
});

document.addEventListener('py:done', (event) => {
    console.log('All scripts finished');
});

document.addEventListener('mpy:ready', (event) => {
    console.log('MicroPython interpreter ready');
});
</script>
```

#### Available events

**`py:ready`** - Pyodide interpreter is ready and about to run code.

**`mpy:ready`** - MicroPython interpreter is ready and about to run
code.

**`py:done`** - All Pyodide scripts have finished executing.

**`mpy:done`** - All MicroPython scripts have finished executing.

**`py:all-done`** - All PyScript activity has completed.

#### Event details

Events carry useful information in their `detail` property:

```javascript
document.addEventListener('py:ready', (event) => {
    // Access the script element.
    const script = event.detail.script;
    
    // Access the interpreter wrapper.
    const wrap = event.detail.wrap;
});
```

Use these events to:

Show loading indicators whilst Python initialises.

Coordinate between JavaScript and Python code.

Enable UI elements only after Python is ready.

Track application lifecycle for debugging or analytics.

### Packaging pointers

Understanding packaging helps you use external Python libraries
effectively.

#### Pyodide packages

Pyodide includes many pre-built packages. Check the
[package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)
to see what's available.

Install pure Python packages from PyPI using `micropip`:

```python
import micropip

await micropip.install("pillow")
```

Some packages with C extensions are available. If `micropip` reports it
cannot find a pure Python wheel, the package either:

Contains C extensions not compiled for WebAssembly.

Isn't compatible with the browser environment.

Has dependencies that aren't available.

#### MicroPython packages

MicroPython uses packages from
[micropython-lib](https://github.com/micropython/micropython-lib).
Reference them in configuration:

```toml
[packages]
"unittest" = ""
```

For packages not in micropython-lib, use the `files` configuration to
include them:

```toml
[files]
"my_package.py" = "https://example.com/my_package.py"
```

Or reference local files:

```toml
[files]
"my_package.py" = "./my_package.py"
```

#### Package size considerations

Pyodide packages can be large. The `numpy` package alone is several
megabytes. Consider:

Using MicroPython for applications where package access isn't critical.

Loading only necessary packages.

Showing loading indicators whilst packages download.

Caching packages for offline use in production applications.

### Filesystem

PyScript provides virtual filesystems through Emscripten. Understanding
how they work helps you manage files effectively.

#### Virtual filesystem basics

Both Pyodide and MicroPython run in sandboxed environments with virtual
filesystems. These aren't the user's actual filesystem - they're
in-memory or browser-storage-backed filesystems provided by Emscripten.

Files you create or modify exist only in this virtual environment. They
persist during the session but may not survive page reloads unless
explicitly saved to browser storage.

#### Loading files

Use the `files` configuration to make files available:

```toml
[files]
"data.csv" = "./data.csv"
"config.json" = "https://example.com/config.json"
```

PyScript downloads these files and places them in the virtual
filesystem. Your Python code can then open them normally:

```python
with open("data.csv") as f:
    data = f.read()
```

It's also possible to manually upload files onto the virtual file system
from the browser (`<input type="file">`), using the DOM API.

The following fragment is just one way to achieve this:

```python
# Assume an input element of type "file" with an id of "upload" in
# the DOM.
# E.g. <input type="file" id="upload">

from pyscript import when, fetch, window


@when("change", "#upload")
async def on_change(event):
    """
    Activated when the user has selected a file to upload via
    the file input element.
    """
    # For each file the user has selected to upload...
    for file in input.files:
        # Create a temporary URL.
        tmp = window.URL.createObjectURL(file)
        # Fetch and save its content somewhere.
        with open(f"./{file.name}", "wb") as dest:
            dest.write(await fetch(tmp).bytearray())
        # Then revoke the tmp URL.
        window.URL.revokeObjectURL(tmp)
```

#### Writing files

You can create and write files in the virtual filesystem:

```python
with open("output.txt", "w") as f:
    f.write("Hello, world!")
```

These files exist in memory. To provide them for download, use the
browser's download mechanism:

```python
from pyscript import window, ffi


def download_file(filename, content):
    """
    Trigger browser download of file content.
    """
    # Ensure you use the correct mime-type!
    blob = window.Blob.new([content], ffi.to_js({"type": "text/plain"}))
    # Create a temporary download link/URL.
    url = window.URL.createObjectURL(blob)
    link = window.document.createElement("a")
    link.href = url
    link.download = filename
    # Activate the link (pretend to click it).
    link.click()
    # Then revoke the temporary URL.
    window.URL.revokeObjectURL(url)


# Use it.
download_file("output.txt", "File contents here")
```

#### Browser storage

For persistent storage across sessions, use browser storage APIs:

```python
from pyscript import window


# Save data to localStorage.
window.localStorage.setItem("key", "value")

# Retrieve data.
value = window.localStorage.getItem("key")
```

Or use the File System Access API for actual file access (requires user
permission):

```python
from pyscript import window


# Request file picker (modern browsers only).
file_handle = await window.showSaveFilePicker()
writable = await file_handle.createWritable()
await writable.write("content")
await writable.close()
```

### create_proxy

The `create_proxy` function manages Python-JavaScript reference
lifecycles.

#### When to use create_proxy

In Pyodide on the main thread, wrap Python functions passed as
JavaScript callbacks:

```python
from pyscript import ffi, window


def callback(event):
    """
    Handle events.
    """
    print(event.type)


# Create proxy before passing to JavaScript.
window.addEventListener("click", ffi.create_proxy(callback))
```

#### When create_proxy isn't needed

In workers, PyScript automatically manages references. You don't need
`create_proxy`:

```python
from pyscript import window


def callback(event):
    """
    Handle events in worker.
    """
    print(event.type)


# No create_proxy needed in workers.
window.addEventListener("click", callback)
```

With `experimental_create_proxy = "auto"` in configuration, PyScript
automatically wraps functions:

```toml
[experimental_create_proxy]
auto = true
```

```python
from pyscript import window


def callback(event):
    """
    Handle events with auto proxying.
    """
    print(event.type)


# No create_proxy needed with auto mode.
window.addEventListener("click", callback)
```

#### In MicroPython

MicroPython creates proxies automatically. The `create_proxy` function
exists for code portability between Pyodide and MicroPython, but it's
just a pass-through in MicroPython:

```python
from pyscript import ffi, window


def callback(event):
    """
    Handle events.
    """
    print(event.type)


# Works with or without create_proxy in MicroPython.
window.addEventListener("click", callback)
window.addEventListener("click", ffi.create_proxy(callback))
```

Both versions work identically in MicroPython.

#### Manual proxy destruction

If manually managing proxies in Pyodide, destroy them when done:

```python
from pyscript import ffi, window


def callback(event):
    """
    One-time handler.
    """
    print(event.type)


proxy = ffi.create_proxy(callback)
window.addEventListener("click", proxy, ffi.to_js({"once": True}))

# After the event fires once, destroy the proxy.
# (In practice, the "once" option auto-removes it, but this shows the
# pattern for cases where you manage lifecycle manually.)
proxy.destroy()
```

Manual destruction prevents memory leaks when callbacks are no longer
needed.

### to_js

The `to_js` function converts Python objects to JavaScript equivalents.

#### Python dicts to JavaScript objects

Python dictionaries convert to JavaScript object literals, not Maps:

```python
from pyscript import ffi, window


config = {"async": False, "cache": True}

# Converts to JavaScript object literal.
js_config = ffi.to_js(config)

# Pass to JavaScript APIs expecting objects.
window.someAPI(js_config)
```

This differs from Pyodide's default behaviour (which creates Maps).
PyScript's `to_js` always creates object literals for better JavaScript
compatibility.

#### When to use to_js

Use `to_js` when passing Python data structures to JavaScript APIs:

```python
from pyscript import ffi, window


# Passing configuration objects.
options = {"method": "POST", "headers": {"Content-Type": "application/json"}}
window.fetch("/api", ffi.to_js(options))

# Passing arrays.
numbers = [1, 2, 3, 4, 5]
window.console.log(ffi.to_js(numbers))

# Passing nested structures.
data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
window.processData(ffi.to_js(data))
```

#### Important caveat

!!! warning

    Objects created by `to_js` are detached from the original Python
    object. Changes to the JavaScript object don't affect the Python
    object:

    ```python
    from pyscript import ffi, window
    
    python_dict = {"key": "value"}
    js_object = ffi.to_js(python_dict)
    
    # Modify JavaScript object.
    js_object.key = "new value"
    
    # Python dict unchanged.
    print(python_dict["key"])  # Still "value"
    ```

This detachment is usually desirable - you're passing data to
JavaScript, not sharing mutable state. But be aware of this behaviour.

#### MicroPython differences

MicroPython's `to_js` already creates object literals by default. You
may not need `to_js` in MicroPython unless ensuring cross-interpreter
compatibility:

```python
from pyscript import window

# Works in MicroPython without to_js.
config = {"async": False}
window.someAPI(config)

# But using to_js ensures Pyodide compatibility.
from pyscript import ffi
window.someAPI(ffi.to_js(config))
```

For code that might run with either interpreter, use `to_js`
consistently.