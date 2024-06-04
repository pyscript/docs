# Workers

Workers run code that won't block the "main thread" controlling the user
interface. If you block the main thread, your web page becomes annoyingly
unresponsive. **You should never block the main thread.**

Happily, PyScript makes it very easy to use workers and uses a feature recently
added to web standards called
[Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics).
You don't need to know about Atomics to use web workers, but the underlying
[coincident library](architecture.md#coincident)
uses it under the hood.

!!! info

    Sometimes you only need to `await` in the main thread the result of a call
    to a method exposed in a worker.

    In such a limited case, and on the understanding that **code in the worker
    will not be able to reach back into the main thread**, you should
    use the [`sync_main_only` flag](../configuration/#sync_main_only) in your
    configuration.

    While this eliminates the need for the Atomics related header configuration
    (see below), the only possible use case is to **return a serialisable
    result from the method called on the worker**.

## HTTP headers

For Atomics to work **you must ensure your web server enables the following
headers** (this is the default behaviour for
[pyscript.com](https://pyscript.com)):

```
Access-Control-Allow-Origin: *
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Resource-Policy: cross-origin
```

If you are not able to configure your server's headers, use the
[mini-coi](https://github.com/WebReflection/mini-coi#readme) project to
achieve the same end.

!!! Info

    The simplest way to use mini-coi is to place the
    [mini-coi.js](https://raw.githubusercontent.com/WebReflection/mini-coi/main/mini-coi.js)
    file in the root of your website (i.e. `/`), and reference it as the first
    child tag in the `<head>` of your HTML documents:

    ```html
    <html>
      <head>
        <script src="/mini-coi.js" scope="./"></script> 
        <!-- etc -->
      </head>
      <!-- etc --> 
    </html>
    ```

## Start working

To start your code in a worker, simply ensure the `<script>`, `<py-script>` or
`<mpy-script>` tag pointing to the code you want to run has a `worker`
attribute flag:

```HTML title="Evaluating code in a worker"
<script type="py" src="./my-worker-code.py" worker></script>
```

Alternatively, to launch a worker from within Python running on the main thread
use the [pyscript.PyWorker](../builtins/#pyscriptpyworker) class and you must
reference both the target Python script and interpreter type:

```python title="Launch a worker from within Python"
from pyscript import PyWorker

# The type MUST be given and can be either `micropython` or `pyodide`
PyWorker("my-worker-code.py", type="micropython")
```

## Worker interactions

Code running in the worker needs to be able to interact with code running in
the main thread and perhaps have access to the web page. This is achieved via
some helpful [builtin utilities](../builtins).

!!! note

    For ease of use, the worker related functionality in PyScript is
    a simpler presentation of more sophisticated and powerful behaviour
    available via PolyScript.

    **If you are a confident advanced user**, please
    [consult the XWorker](https://pyscript.github.io/polyscript/#xworker)
    related documentation from the PolyScript project for how to make use of
    these features.

To synchronise serializable data between the worker and the main thread use
[the `sync` function](../builtins/#pyscriptsync) in the worker to reference a
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

The values passed between the main thread and the worker **must be
serializable**. Try the example given above via
[this project on PyScript.com](https://pyscript.com/@ntoll/tiny-silence/latest).

No matter if your code is running on the main thread or in a web worker,
both the [`pyscript.window`](../builtins/#pyscriptwindow) (representing the main
thread's global window context) and
[`pyscript.document`](../builtins/#pyscriptdocument) (representing the web
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
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.5.2/core.css">
    <!-- This script tag bootstraps PyScript -->
    <script type="module" src="https://pyscript.net/releases/2024.5.2/core.js"></script>
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
use `npx mini-coi ./tmp` and update `index.html`) then see the following
outcome in the browser's devtools. 

```
before ready
Pyodide bootstrapped
after ready
42
```
