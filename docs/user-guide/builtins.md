# Builtin helpers

PyScript makes available convenience objects and functions inside
Python as well as custom attributes in HTML.

In Python this is done via the `pyscript` module:

```python title="Accessing the document object via the pyscript module"
from pyscript import document
```

In HTML this is done via `py-*` attributes:

```html title="An example of a py-click handler"
<button id="foo" py-click="handler_defined_in_python">Click me</button>
```

## Common features

These Python objects / functions are available in both the main thread and in
code running on a web worker:

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

This functionality is related to the [HTML py-*](#html-attributes) attributes.

### `pyscript.js_modules`

It is possible to [define JavaScript modules to use within your Python code](configuration.md#javascript-modules).

Such named modules will always then be available under the
`pyscript.js_modules` namespace.

!!! warning

    Please see the documentation (linked above) about restrictions and gotchas
    when configuring how JavaScript modules are made available to PyScript.

### `pyscript.fetch`

A common task is to `fetch` data from the web via HTTP requests. The
`pyscript.fetch` function provides a uniform way to achieve this in both
Pyodide and MicroPython. It is closely modelled on the
[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) found
in browsers with some important Pythonic differences.

The simple use case is to pass in a URL and `await` the response. Remember, in
order to use `await` you must have the `async` attribute in the `script` tag
that references your code. If this request is in a function, that function
should also be defined as `async`.

```python title="A simple HTTP GET with pyscript.fetch"
from pyscript import fetch


response = await fetch("https://example.com")
if response.ok:
    data = await response.text()
else:
    print(response.status)
```

The object returned from an `await fetch` call will have attributes that
correspond to the
[JavaScript response object](https://developer.mozilla.org/en-US/docs/Web/API/Response).
This is useful for getting response codes, headers and other metadata before
processing the response's data.

Alternatively, rather than using a double `await` (one to get the response, the
other to grab the data), it's possible to chain the calls into a single
`await` like this:

```python title="A simple HTTP GET as a single await"
from pyscript import fetch

data = await fetch("https://example.com").text()
```

The following awaitable methods are available to you to access the data
returned from the server:

* `arrayBuffer()` returns a Python [memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview) of the response. This is equivalent to the [`arrayBuffer()` method](https://developer.mozilla.org/en-US/docs/Web/API/Response/arrayBuffer) in the browser based `fetch` API.
* `blob()` returns a JavaScript [`blob`](https://developer.mozilla.org/en-US/docs/Web/API/Response/blob) version of the response. This is equivalent
to the [`blob()` method](https://developer.mozilla.org/en-US/docs/Web/API/Response/blob) in the browser based `fetch` API.
* `bytearray()` returns a Python [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray) version of the response.
* `json()` returns a Python datastructure representing a JSON serialised payload in the response.
* `text()` returns a Python string version of the response.

The underlying browser `fetch` API has [many request options](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options)
that you should simply pass in as keyword arguments like this:

```python title="Supplying request options."
from pyscript import fetch


response = await fetch("https://example.com", method="POST", body="HELLO").text()
```

!!! Danger

    You may encounter [CORS](https://developer.mozilla.org/en-US/docs/Glossary/CORS) errors (especially with reference to a missing
    [Access-Control-Allow-Origin header](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin).

    This is a security feature of modern browsers where the site to which you
    are making a request **will not process a request from a site hosted at
    another domain**.

    For example, if your PyScript app is hosted under `example.com` and you
    make a request to `bbc.co.uk` (who don't allow requests from other domains)
    then you'll encounter this sort of CORS related error.

    There is nothing PyScript can do about this problem (it's a feature, not a
    bug). However, you could use a pass-through proxy service to get around
    this limitation (i.e. the proxy service makes the call on your behalf).

### `pyscript.ffi.to_js`

A utility function to convert Python references into their JavaScript
equivalents. For example, a Python dictionary is converted into a JavaScript
object literal (rather than a JavaScript `Map`), unless a `dict_converter`
is explicitly specified and the runtime is Pyodide.

### `pyscript.ffi.create_proxy`

A utility function explicitly for when a callback function is added via an
event listener. It ensures the function still exists beyond the assignment of
the function to an event. Should you not `create_proxy` around the callback
function, it will be immediately garbage collected after being bound to the
event.

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

## HTML attributes

As a convenience, and to ensure backwards compatibility, PyScript allows the
use of inline event handlers via custom HTML attributes.

!!! warning

    This classic pattern of coding (inline event handlers) is no longer
    considered good practice in web development circles.

    We include this behaviour for historic reasons, but the folks at
    Mozilla [have a good explanation](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#inline_event_handlers_%E2%80%94_dont_use_these)
    of why this is currently considered bad practice.

These attributes are expressed as `py-*` attributes of an HTML element that
reference the name of a Python function to run when the event is fired. You
should replace the `*` with the _actual name of an event_ (e.g. `py-click`).
This is similar to how all
[event handlers on elements](https://html.spec.whatwg.org/multipage/webappapis.html#event-handlers-on-elements,-document-objects,-and-window-objects)
start with `on` in standard HTML (e.g. `onclick`). The rule of thumb is to
simply replace `on` with `py-` and then reference the name of a Python
function.

```html title="A py-click event on an HTML button element."
<button py-click="handle_click" id="my_button">Click me!</button>
```

```python title="The related Python function."
from pyscript import window


def handle_click(event):
    """
    Simply log the click event to the browser's console.
    """
    window.console.log(event)    
```

Under the hood, the [`pyscript.when`](#pyscriptwhen) decorator is used to
enable this behaviour.

!!! note

    In earlier versions of PyScript, the value associated with the attribute
    was simply evaluated by the Python interpreter. This was unsafe:
    manipulation of the attribute's value could have resulted in the evaluation
    of arbitrary code.

    This is why we changed to the current behaviour: just supply the name
    of the Python function to be evaluated, and PyScript will do this safely.
