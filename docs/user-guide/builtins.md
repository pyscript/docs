# Builtin helpers

PyScript makes available convenience objects and functions inside
Python. This is done via the `pyscript` module:

```python title="Accessing the document object via the pyscript module"
from pyscript import document
```

## Common features

These objects / functions are available in both the main thread and in code
running on a web worker:

### `pyscript.window`

This object is a proxy for the web page's
[global window context](https://developer.mozilla.org/en-US/docs/Web/API/Window).

!!! warning

    Please note that in workers, this is still the main window, not the
    worker's own global context. A worker's global context is reachable instead
    via `import js` (the `js` object being a proxy for the worker's
    `globalThis`).

### `pyscript.document`

This object is a proxy for the the web page's
[document object](https://developer.mozilla.org/en-US/docs/Web/API/Document).
The `document` is a representation of the
[DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Using_the_Document_Object_Model)
and can be used to manipulate the content of the web page.

### `pyscript.display`

A function used to display content. The function is intelligent enough to
introspect the object[s] it is passed and work out how to correctly display the
object[s] in the web page.

The `display` function takes a list of `*values` as its first argument, and has
two optional named arguments:

* `target=None` - the DOM element into which the content should be placed.
* `append=True` - a flag to indicate if the output is going to be appended to
  the `target`.

There are some caveats:

* When used in the main thread, the `display` function automatically uses
  the current `<script>` tag as the `target` into which the content will
  be displayed.
* If the `<script>` tag has the `target` attribute, the element on the page
  with that ID (or which matches that selector) will be used to display
  the content instead.
* When used in a worker, the `display` function needs an explicit
  `target="dom-id"` argument to identify where the content will be
  displayed.
* In both the main thread and worker, `append=True` is the default
  behaviour.

### `pyscript.when`

A Python decorator to indicate the decorated function should handle the
specified events for selected elements.

The decorator takes two parameters:

* The `event_type` should be the name of the
  [browser event to handle](https://developer.mozilla.org/en-US/docs/Web/Events)
  as a string (e.g. `"click"`).
* The `selector` should be a string containing a
  [valid selector](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Locating_DOM_elements_using_selectors)
  to indicate the target elements in the DOM whose events of `event_type` are
  of interest.

The following example has a button with an id of `my_button` and a decorated
function that handles `click` events dispatched by the button.

```html title="The HTML button"
<button id="my_button">Click me!</button>
```

```python title="The decorated Python function to handle click events"
from pyscript import when, display


@when("click", "#my_button")
def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    display("I've been clicked!")
```

## Main-thread only features

### `pyscript.PyWorker`

A class used to instantiate a new worker from within Python.

!!! danger 

    Currently this only works with Pyodide.

The following fragment demonstrates who to start the Python code in the file
`worker.py` on a new worker from within Python.

```python title="Starting a new worker from Python"
from pyscript import PyWorker


a_worker = PyWorker("./worker.py")
```

## Worker only features

### `pyscript.sync`

A function used to pass serializable data from workers to the main thread. 

Imagine you have this code on the main thread:

```python title="Python code on the main thread"
from pyscript import PyWorker

def hello(name="world"):
    display(f"Hello, {name}")

worker = PyWorker("./worker.py")
worker.sync.hello = hello
```

In the code on the worker, you can pass data back to handler functions like
this:

```python title="Pass data back to the main thread from a worker"
from pyscript import sync

sync.hello("PyScript")
```
