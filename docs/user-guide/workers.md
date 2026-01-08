# Workers

Workers run Python code in background threads, keeping your user interface
responsive. Without workers, long computations block the main thread and freeze
the page. With workers, heavy tasks run in the background whilst the UI stays
smooth and interactive.

This guide explains how to use workers in PyScript, when to use them, and how
to structure your applications to take advantage of background processing.

## Understanding the problem

JavaScript (and therefore PyScript) runs on a single "main" thread. When Python
code executes, nothing else can happen. Long computations freeze the interface.
Users cannot click buttons, scroll, or interact with the page until the
computation completes.

Workers solve this problem by running Python in separate threads. The main
thread handles the UI. Workers handle computation. Both run simultaneously, so
your application remains responsive even during heavy processing.

## Defining workers

Workers are defined with `<script>` tags that have a `worker` attribute:

```html
<script type="py" worker name="calculator" config='{"packages":["numpy"]}'>
import numpy as np


def add_arrays(a, b):
    """
    Add two arrays using numpy.
    """
    return (np.array(a) + np.array(b)).tolist()


# Export functions to make them accessible.
__export__ = ["add_arrays"]
</script>
```

The `worker` attribute marks the script as a worker. The `name` attribute
provides a unique identifier for accessing the worker from other code. The
`type` attribute specifies the interpreter: `py` for Pyodide or `mpy` for
MicroPython.

Workers must explicitly export functions using the `__export__` list. Only
exported functions are accessible from the main thread. This keeps the API
clear and prevents accidental exposure of internal implementation details.

## Accessing workers

Access workers from the main thread using the `workers` object:

```python
from pyscript import workers


# Get the worker by name.
calc = await workers["calculator"]

# Call its exported function.
result = await calc.add_arrays([1, 2, 3], [4, 5, 6])
print(result)  # [5, 7, 9]
```

Worker access is asynchronous because workers may not be ready immediately.
They need time to download and initialise the interpreter, load configured
packages, execute the worker script, and register exported functions. The
`await` ensures the worker is fully ready before you use it.

Once you have a worker reference, call its exported functions like normal async
functions. **All calls must be awaited, and all data passed between the main
thread and workers must be serialisable (numbers, strings, lists, dictionaries,
booleans, None)**. You cannot pass functions, classes, or complex objects.

## Choosing interpreters

PyScript supports two Python interpreters, and you can mix them based on your
needs. The main thread and workers can use different interpreters.

Pyodide (`type="py"`) provides full CPython compatibility with access to
weighty packages like numpy and pandas. It has a larger download size and
slower startup, but offers the complete Python ecosystem. Use Pyodide for heavy
computation requiring numerical libraries, tasks needing the full Python
ecosystem, or complex data processing.

MicroPython (`type="mpy"`) provides fast startup with a small footprint. It
includes core Python only, with no pip packages. Use MicroPython for
lightweight tasks, quick worker startup, or simple computations when you don't
need packages.

A common pattern is MicroPython on the main thread for a fast, responsive UI,
with Pyodide in workers for powerful computation when needed:

```html
<!-- Fast main thread. -->
<script type="mpy" src="./main.py"></script>

<!-- Powerful worker. -->
<script type="py" worker name="compute" config='{"packages":["numpy"]}'>
import numpy as np


def crunch_numbers(data):
    return np.array(data).sum()


__export__ = ["crunch_numbers"]
</script>
```

## Creating workers dynamically

Create workers from Python code using `create_named_worker()`:

```python
from pyscript import create_named_worker


# Create a Pyodide worker.
worker = await create_named_worker(
    src="./background_tasks.py",
    name="task-processor",
    config={"packages": ["pandas"]}
)

# Use it immediately.
result = await worker.process_data()
```

This is useful for spawning workers based on user actions, creating multiple
workers for parallel processing, or loading workers conditionally based on
application state.

The function accepts four parameters. The `src` parameter specifies the path to
the worker's Python file. The `name` parameter provides a unique identifier for
the worker. The `config` parameter accepts a configuration dictionary or JSON
string (optional). The `type` parameter specifies the interpreter: `"py"`
(default) or `"mpy"` (optional).

## Configuration

Workers support the same configuration as main thread scripts. You can specify
packages to install, files to fetch, and JavaScript modules to import. See the
[Configuration guide](configuration.md) for complete details on available
options.

The configuration is provided either inline as a JSON string in the `config`
attribute, or as a path to a configuration file:

```html
<!-- Inline configuration. -->
<script type="py" worker name="processor" config='{"packages":["pandas"]}'>
...
</script>

<!-- Configuration file. -->
<script type="py" worker name="processor" config="./worker-config.json">
...
</script>
```

## Example: Prime number calculator

Here's a complete example demonstrating workers in action:

<iframe src="../../example-apps/prime-worker/" style="border: 1px solid black; width:100%; min-height: 600px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/prime-worker).

This application finds prime numbers using the
[Sieve of Eratosthenes algorithm](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes).
The heavy computation runs in a worker, keeping the main thread responsive.

The HTML page defines two scripts. The main thread uses MicroPython and
handles the UI:

```html
<script type="mpy" src="./main.py"></script>
```

The worker uses Pyodide with numpy and does the computation:

```html
<script type="py" worker name="primes" config="./pyscript.json">
```

When you click "Find Primes", the main thread gets a reference to the
worker, calls the worker's function, and displays the results when they
arrive:

```python
from pyscript import workers
from pyscript.web import page


@when("click", "#find-btn")
async def find_primes(event):
    # Get the worker.
    worker = await workers["primes"]
    
    # Check if numpy should be used.
    use_numpy = page["#use-numpy"].checked
    
    # Call its exported function.
    result = await worker.find_primes(limit, use_numpy)
    
    # Display the results.
    print(f"Found {result['count']} primes")
```

The worker script defines the computation and exports it:

```python
import numpy as np


def find_primes(limit, use_numpy=True):
    # Use numpy's efficient array operations or pure Python.
    # ... Sieve of Eratosthenes algorithm ...
    return {"count": len(primes), "first_20": first_20_primes}


__export__ = ["find_primes"]
```

Watch the pulsing green indicator whilst computing. It never stops,
proving the main thread stays responsive. Try entering different values
to see the worker handle various workloads. The "Use NumPy" checkbox
lets you compare the performance of numpy's array operations against
pure Python - a nice demonstration of why numerical libraries matter for
computational tasks.

## Understanding limitations

Workers have separate memory spaces. Each worker has its own memory, and
you cannot share objects between workers or with the main thread. All
communication happens via function calls with serialised data.

Only serialisable data can pass between threads. Function arguments and
return values must be JSON-serialisable: numbers, strings, lists,
dictionaries, booleans, and None work. Functions, classes, file handles,
and numpy arrays (convert to lists first) do not work.

Workers need time to initialise. Pyodide workers especially may take time
to download packages and start up. The first call may be slow. Plan your
application accordingly and consider showing loading indicators during
initialisation.

User activation requirements apply. Creating workers dynamically with
`create_named_worker()` during page load works fine. However, if your
worker needs to access certain browser features, those features may
require user activation (a button click or similar interaction).

## What's next

Now that you understand workers, explore these related topics to deepen
your knowledge.

**[Architecture guide](architecture.md)** - provides technical details about
how PyScript implements workers using PolyScript and Coincident if you're
interested in the underlying mechanisms.

**[Filesystem](filesystem.md)** - Learn more about the virtual
filesystem and how the `files` option works.

**[FFI](ffi.md)** - Understand how JavaScript modules integrate with
Python through the foreign function interface.

**[Media](media.md)** - Capture photos and video with the camera or 
record audio with your microphone.

**[Offline](offline.md)** - Use PyScript while not connected to the internet.