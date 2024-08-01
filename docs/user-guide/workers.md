# Workers

Workers run code that won't block the "main thread" controlling the user
interface. If you block the main thread, your web page becomes annoyingly
unresponsive. **You should never block the main thread.**

Happily, PyScript makes it very easy to use workers and uses a feature recently
added to web standards called
[Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics).
**You don't need to know about Atomics to use web workers**, but it's useful to
know that the underlying [coincident library](architecture.md#coincident)
uses it under the hood.

!!! info

    Sometimes you only need to `await` in the main thread on a method in a
    worker when neither `window` nor `document` are referenced in the code
    running on the worker.

    In these cases, you don't need any special header or service worker
    as long as **the method exposed from the worker returns a serializable
    result**.

## HTTP headers

To use the `window` and `document` objects from within a worker (i.e. use
synchronous Atomics) **you must ensure your web server enables the following
headers** (this is the default behavior for
[pyscript.com](https://pyscript.com)):

```
Access-Control-Allow-Origin: *
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Resource-Policy: cross-origin
```

If you're unable to configure your server's headers, you have two options:

1. Use the [mini-coi](https://github.com/WebReflection/mini-coi#readme) project
   to enforce headers.
2. Use the `service-worker` attribute with the `script` element.

### Option 1: mini-coi

For performance reasons, this is the preferred option so Atomics works at
native speed.

The simplest way to use mini-coi is to copy the
[mini-coi.js](https://raw.githubusercontent.com/WebReflection/mini-coi/main/mini-coi.js)
file content and save it in the root of your website (i.e. `/`), and reference
it as the first child tag in the `<head>` of your HTML documents:

```html
<html>
  <head>
    <script src="/mini-coi.js"></script>
    <!-- etc -->
  </head>
  <!-- etc -->
</html>
```

### Option 2: `service-worker` attribute

This allows you to slot in a custom
[service worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
to handle requirements for synchronous operations.

Each `<script type="m/py">` or `<m/py-script>` may optionally have
a `service-worker` attribute pointing to a locally served file (the
same way `mini-coi.js` needs to be served).

* You can chose `mini-coi.js` itself or *any other custom service worker*,
  as long as it provides either the right headers to enable synchronous
  operations via Atomics, or it enables
  [sabayon polyfill events](https://github.com/WebReflection/sabayon?tab=readme-ov-file#service-worker).
* Alternatively, you can copy and paste the
  [sabayon Service Worker](https://raw.githubusercontent.com/WebReflection/sabayon/main/dist/sw.js)
  into your local project and point at that in the attribute. This will
  not change the original behavior of your project, it will not interfere with
  all default or pre-defined headers your application uses already but it will
  **fallback to a (slower but working) synchronous operation** that allows 
  both `window` and `document` access in your worker logic.

```html
<html>
  <head>
    <!-- PyScript link and script -->
  </head>
  <body>
    <script type="py" service-worker="./sw.js" worker>
      from pyscript import window, document

      document.body.append("Hello PyScript!")
    </script>
  </body>
</html>
```

!!! warning 

    Using sabayon as the fallback for synchronous operations via Atomics
    should be **the last solution to consider**. It is inevitably
    slower than using native Atomics.

    If you must use sabayon, always reduce the amount of synchronous
    operations by caching references from the *main* thread.

    ```python
    # ❌ THIS IS UNNECESSARILY SLOWER
    from pyscript import document

    # add a data-test="not ideal attribute"
    document.body.dataset.test = "not ideal"
    # read a data-test attribute
    print(document.body.dataset.test)

    # - - - - - - - - - - - - - - - - - - - - -

    # ✔️ THIS IS FINE
    from pyscript import document

    # if needed elsewhere, reach it once
    body = document.body
    dataset = body.dataset

    # add a data-test="not ideal attribute"
    dataset.test = "not ideal"
    # read a data-test attribute
    print(dataset.test)
    ```

In latter example the number of operations has been reduced from six to just
four. The rule of thumb is: _if you ever need a DOM reference more than once,
cache it_. 👍


## Start working

To start your code in a worker, simply ensure the `<script>`, `<py-script>` or
`<mpy-script>` tag pointing to the code you want to run has a `worker`
attribute flag:

```HTML title="Evaluating code in a worker"
<script type="py" src="./my-worker-code.py" worker></script>
```

You may also want to add a `name` attribute to the tag, so you can use
`pyscript.workers` in the main thread to retrieve a reference to the worker:

```html
<script type="py" src="./my-worker-code.py" worker name="my-worker"></script>
```

```python
from pyscript import workers

my_worker = await workers["my-worker"]
```

Alternatively, to launch a worker from within Python running on the main thread
use the [pyscript.PyWorker](../../api/#pyscriptpyworker) class and you must
reference both the target Python script and interpreter type:

```python title="Launch a worker from within Python"
from pyscript import PyWorker

# The type MUST be given and can be either `micropython` or `pyodide`
my_worker = PyWorker("my-worker-code.py", type="micropython")
```

## Worker interactions

Code running in the worker needs to be able to interact with code running in
the main thread and perhaps have access to the web page. This is achieved via
some helpful [builtin APIs](../../api).

!!! note

    For ease of use, the worker related functionality in PyScript is
    a simpler presentation of more sophisticated and powerful behaviour
    available via PolyScript.

    **If you are a confident advanced user**, please
    [consult the XWorker](https://pyscript.github.io/polyscript/#xworker)
    related documentation from the PolyScript project for how to make use of
    these features.

To synchronise serializable data between the worker and the main thread use
[the `sync` function](../../api/#pyscriptsync) in the worker to reference a
function registered on the main thread:

```python title="Python code running on the main thread."
from pyscript import PyWorker

def hello(name="world"):
    return(f"Hello, {name}")

# Create the worker.
worker = PyWorker("./worker.py", type="micropython")

# Register the hello function as callable from the worker.
worker.sync.hello = hello
```

```python title="Python code in the resulting worker."
from pyscript import sync, window

greeting = sync.hello("PyScript")
window.console.log(greeting)
```

Alternatively, for the main thread to call functions in a worker, specify the
functions in a `__export__` list:

```python title="Python code on the worker."
import sys

def version():
    return sys.version

# Define what to export to the main thread.
__export__ = ["version", ]
```

Then ensure you have a reference to the worker in the main thread (for
instance, by using the `pyscript.workers`):

```html title="Creating a named worker in the web page."
<script type="py" src="./my-worker-code.py" worker name="my-worker"></script>
```

```python title="Referencing and using the worker from the main thread."
from pyscript import workers

my_worker = await workers["my-worker"]

print(await my_worker.version())
```

The values passed between the main thread and the worker **must be
serializable**. Try the example given above via
[this project on PyScript.com](https://pyscript.com/@ntoll/tiny-silence/latest).

No matter if your code is running on the main thread or in a web worker,
both the [`pyscript.window`](../../api/#pyscriptwindow) (representing the main
thread's global window context) and
[`pyscript.document`](../../api/#pyscriptdocument) (representing the web
page's
[document object](https://developer.mozilla.org/en-US/docs/Web/API/Document))
will be available and work in the same way. As a result, a worker can reach
into the DOM and access some `window` based APIs.

!!! warning

    Access to the `window` and `document` objects is a powerful feature. Please
    remember that:

    * Arguments to and the results from such calls, when used in a worker,
      **must be serializable**, otherwise they won't work.
    * If you manipulate the DOM via the `document` object, and other workers or
      code on the main thread does so too, **they may interfere with each other
      and produce unforeseen problematic results**. Remember, with great power
      comes great responsibility... and we've given you a bazooka (so please
      remember not to shoot yourself in the foot with it).

## Common Use Case

While it is possible to start a MicroPython or Pyodide worker from either
MicroPython or Pyodide running on the main thread, the most common use case
we have encountered is MicroPython on the main thread starting a Pyodide
worker.

Here's how:

**index.html**
```HTML title="Evaluate main.py via MicroPython on the main thread"
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <!-- PyScript CSS -->
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.8.1/core.css">
    <!-- This script tag bootstraps PyScript -->
    <script type="module" src="https://pyscript.net/releases/2024.8.1/core.js"></script>
    <title>PyWorker - mpy bootstrapping pyodide example</title>
    <!-- the async attribute is useful but not mandatory -->
    <script type="mpy" src="main.py" async></script>
  </head>
</html>
```

**main.py**
```Python title="MicroPython's main.py: bootstrapping a Pyodide worker."
from pyscript import PyWorker, document

# Bootstrap the Pyodide worker, with optional config too.
# The worker is:
#   * Owned by this script, no JS or Pyodide code in the same page can access
#     it.
#   * It allows pre-sync methods to be exposed.
#   * It has a ready Promise to await for when Pyodide is ready in the worker. 
#   * It allows the use of post-sync (methods exposed by Pyodide in the
#     worker).
worker = PyWorker("worker.py", type="pyodide")

# Expose a utility that can be immediately invoked in the worker. 
worker.sync.greetings = lambda: print("Pyodide bootstrapped")

print("before ready")
# Await until Pyodide has completed its bootstrap, and is ready.
await worker.ready
print("after ready")

# Await any exposed methods exposed via Pyodide in the worker.
result = await worker.sync.heavy_computation()
print(result)

# Show the result at the end of the body.
document.body.append(result)

# Free memory and get rid of everything in the worker.
worker.terminate()
```

**worker.py**
```Python title="The worker.py script runs in the Pyodide worker."
from pyscript import sync

# Use any methods from main.py on the main thread.
sync.greetings()

# Expose any methods meant to be used from main.
sync.heavy_computation = lambda: 6 * 7
```

Save these files in a `tmp` folder, ensure [your headers](#http-headers) (just
use `npx mini-coi ./tmp` to serve via localhost) then see the following
outcome in the browser's devtools. 

```
before ready
Pyodide bootstrapped
after ready
42
```
