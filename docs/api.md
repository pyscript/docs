# Built-in APIs

PyScript makes available convenience objects, functions and attributes.

In Python this is done via the builtin `pyscript` module:

```python title="Accessing the document object via the pyscript module"
from pyscript import document
```

In HTML this is done via `py-*` and `mpy-*` attributes (depending on the
interpreter you're using):

```html title="An example of a py-click handler"
<button id="foo" py-click="handler_defined_in_python">Click me</button>
```

These APIs will work with both Pyodide and Micropython in exactly the same way.

!!! info

    Both Pyodide and MicroPython provide access to two further lower-level
    APIs:

    * Access to
      [JavaScript's `globalThis`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis)
      via importing the `js` module: `import js` (now `js` is a proxy for 
      `globalThis` in which all native JavaScript based browser APIs are
      found).
    * Access to interpreter specific versions of utilities and the foreign
      function interface. Since these are different for each interpreter, and
      beyond the scope of PyScript's own documentation, please check each
      project's documentation
      ([Pyodide](https://pyodide.org/en/stable/usage/api-reference.html) / 
      [MicroPython](https://docs.micropython.org/en/latest/)) for details of
      these lower-level APIs.

PyScript can run in two contexts: the main browser thread, or on a web worker.
The following three categories of API functionality explain features that are
common for both main thread and worker, main thread only, and worker only. Most
features work in both contexts in exactly the same manner, but please be aware
that some are specific to either the main thread or a worker context.

## Common features

These Python objects / functions are available in both the main thread and in
code running on a web worker:

### `pyscript.config`

A Python dictionary representing the configuration for the interpreter.

```python title="Reading the current configuration."
from pyscript import config


# It's just a dict.
print(config.get("files"))
# This will be either "mpy" or "py" depending on the current interpreter.
print(config["type"])
```

!!! info

    The `config` object will always include a `type` attribute set to either
    `mpy` or `py`, to indicate which version of Python your code is currently
    running in.

!!! warning

    Changing the `config` dictionary at runtime has no effect on the actual
    configuration.

    It's just a convenience to **read the configuration** at run time.

### `pyscript.current_target`

A utility function to retrieve the unique identifier of the element used
to display content. If the element is not a `<script>` and it already has
an `id`, that `id` will be returned.

```html title="The current_target utility"
<!-- current_target(): explicit-id -->
<mpy-script id="explicit-id">
    from pyscript import display, current_target
    display(f"current_target(): {current_target()}")
</mpy-script>

<!-- current_target(): mpy-0 -->
<mpy-script>
    from pyscript import display, current_target
    display(f"current_target(): {current_target()}")
</mpy-script>

<!-- current_target(): mpy-1 -->
<!-- creates right after the <script>:
    <script-py id="mpy-1">
        <div>current_target(): mpy-1</div>
    </script-py>
-->
<script type="mpy">
    from pyscript import display, current_target
    display(f"current_target(): {current_target()}")
</script>
```

!!! Note

    The return value of `current_target()` always references a visible element
    on the page, **not** at the current `<script>` that is executing the code.

    To reference the `<script>` element executing the code, assign it an `id`:

    ```html
    <script type="mpy" id="unique-id">...</script>
    ```

    Then use the standard `document.getElementById(script_id)` function to
    return a reference to it in your code.

### `pyscript.display`

A function used to display content. The function is intelligent enough to
introspect the object[s] it is passed and work out how to correctly display the
object[s] in the web page based on the following mime types:

* `text/plain` to show the content as text
* `text/html` to show the content as *HTML*
* `image/png` to show the content as `<img>`
* `image/jpeg` to show the content as `<img>`
* `image/svg+xml` to show the content as `<svg>`
* `application/json` to show the content as *JSON*
* `application/javascript` to put the content in `<script>` (discouraged)

The `display` function takes a list of `*values` as its first argument, and has
two optional named arguments:

* `target=None` - the DOM element into which the content should be placed.
  If not specified, the `target` will use the `current_script()` returned id
  and populate the related dedicated node to show the content.
* `append=True` - a flag to indicate if the output is going to be appended to
  the `target`.

There are some caveats:

* When used in the main thread, the `display` function automatically uses
  the current `<py-script>` or `<mpy-script>` tag as the `target` into which
  the content will be displayed.
* If the `<script>` tag has the `target` attribute, and is not a worker,
  the element on the page with that ID (or which matches that selector)
  will be used to display the content instead.
* When used in a worker, the `display` function needs an explicit
  `target="dom-id"` argument to identify where the content will be
  displayed.
* In both the main thread and worker, `append=True` is the default
  behaviour.


```html title="Various display examples"
<!-- will produce
    <py-script>PyScript</py-script>
-->
<py-script worker>
    from pyscript import display
    display("PyScript", append=False)
</py-script>

<!-- will produce
    <script type="py">...</script>
    <script-py>PyScript</script-py>
-->
<script type="py">
    from pyscript import display
    display("PyScript", append=False)
</script>

<!-- will populate <h1>PyScript</h1> -->
<script type="py" target="my-h1">
    from pyscript import display
    display("PyScript", append=False)
</script>
<h1 id="my-h1"></h1>

<!-- will populate <h2>PyScript</h2> -->
<script type="py" worker>
    from pyscript import display
    display("PyScript", target="my-h2", append=False)
</script>
<h2 id="my-h2"></h2>
```

### `pyscript.document`

On both main and worker threads, this object is a proxy for the web page's
[document object](https://developer.mozilla.org/en-US/docs/Web/API/Document).
The `document` is a representation of the
[DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Using_the_Document_Object_Model)
and can be used to read or manipulate the content of the web page.

### `pyscript.fetch`

A common task is to `fetch` data from the web via HTTP requests. The
`pyscript.fetch` function provides a uniform way to achieve this in both
Pyodide and MicroPython. It is closely modelled on the
[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) found
in browsers with some important Pythonic differences.

The simple use case is to pass in a URL and `await` the response. If this
request is in a function, that function should also be defined as `async`.

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

* `arrayBuffer()` returns a Python
  [memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview) of
  the response. This is equivalent to the
  [`arrayBuffer()` method](https://developer.mozilla.org/en-US/docs/Web/API/Response/arrayBuffer)
  in the browser based `fetch` API.
* `blob()` returns a JavaScript
  [`blob`](https://developer.mozilla.org/en-US/docs/Web/API/Response/blob)
  version of the response. This is equivalent to the
  [`blob()` method](https://developer.mozilla.org/en-US/docs/Web/API/Response/blob)
  in the browser based `fetch` API.
* `bytearray()` returns a Python
  [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray)
  version of the response.
* `json()` returns a Python datastructure representing a JSON serialised
  payload in the response.
* `text()` returns a Python string version of the response.

The underlying browser `fetch` API has
[many request options](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options)
that you should simply pass in as keyword arguments like this:

```python title="Supplying request options."
from pyscript import fetch


result = await fetch("https://example.com", method="POST", body="HELLO").text()
```

!!! Danger

    You may encounter
    [CORS](https://developer.mozilla.org/en-US/docs/Glossary/CORS)
    errors (especially with reference to a missing
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

### `pyscript.ffi`

The `pyscript.ffi` namespace contains foreign function interface (FFI) methods
that work in both Pyodide and MicroPython.

#### `pyscript.ffi.create_proxy`

A utility function explicitly for when a callback function is added via an
event listener. It ensures the function still exists beyond the assignment of
the function to an event. Should you not `create_proxy` around the callback
function, it will be immediately garbage collected after being bound to the
event.

!!! warning

    There is some technical complexity to this situation, and we have attempted
    to create a mechanism where `create_proxy` is never needed.

    *Pyodide* expects the created proxy to be explicitly destroyed when it's
    not needed / used anymore. However, the underlying `proxy.destroy()` method
    has not been implemented in *MicroPython* (yet).

    To simplify this situation and automatically destroy proxies based on
    JavaScript memory management (garbage collection) heuristics, we have
    introduced an **experimental flag**:

    ```toml
    experimental_create_proxy = "auto"
    ```

    This flag ensures the proxy creation and destruction process is managed for
    you. When using this flag you should never need to explicitly call
    `create_proxy`.

The technical details of how this works are
[described here](../user-guide/ffi#create_proxy).

#### `pyscript.ffi.to_js`

A utility function to convert Python references into their JavaScript
equivalents. For example, a Python dictionary is converted into a JavaScript
object literal (rather than a JavaScript `Map`), unless a `dict_converter`
is explicitly specified and the runtime is Pyodide.

The technical details of how this works are [described here](../user-guide/ffi#to_js).

### `pyscript.fs`

!!! danger

    This API only works in Chromium based browsers.

An API for mounting the user's local filesystem to a designated directory in
the browser's virtual filesystem. Please see
[the filesystem](../user-guide/filesystem) section of the user-guide for more
information.

#### `pyscript.fs.mount`

Mount a directory on the user's local filesystem into the browser's virtual
filesystem. If no previous
[transient user activation](https://developer.mozilla.org/en-US/docs/Glossary/Transient_activation)
has taken place, this function will result in a minimalist dialog to provide
the required transient user activation.

This asynchronous function takes four arguments:

* `path` (required) - indicating the location on the in-browser filesystem to
  which the user selected directory from the local filesystem will be mounted.
* `mode` (default: `"readwrite"`) - indicates how the code may interact with
  the mounted filesystem. May also be just `"read"` for read-only access.
* `id` (default: `"pyscript"`) - indicate a unique name for the handler
  associated with a directory on the user's local filesystem. This allows users
  to select different folders and mount them at the same path in the
  virtual filesystem.
* `root` (default: `""`) - a hint to the browser for where to start picking the
  path that should be mounted in Python. Valid values are: `desktop`,
  `documents`, `downloads`, `music`, `pictures` or `videos` as per
  [web standards](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker#startin).

```python title="Mount a local directory to the '/local' directory in the browser's virtual filesystem"
from pyscript import fs


# May ask for permission from the user, and select the local target.
await fs.mount("/local")
```

If the call to `fs.mount` happens after a click or other transient event, the
confirmation dialog will not be shown.

```python title="Mounting without a transient event dialog."
from pyscript import fs


async def handler(event):
    """
    The click event that calls this handler is already a transient event.
    """
    await fs.mount("/local")


my_button.onclick = handler
```

#### `pyscript.fs.sync`

Given a named `path` for a mount point on the browser's virtual filesystem,
asynchronously ensure the virtual and local directories are synchronised (i.e.
all changes made in the browser's mounted filesystem, are propagated to the
user's local filesystem).

```python title="Synchronise the virtual and local filesystems."
await fs.sync("/local")
```

#### `pyscript.fs.unmount`

Asynchronously unmount the named `path` from the browser's virtual filesystem
after ensuring content is synchronized. This will free up memory and allow you
to re-use the path to mount a different directory.

```python title="Unmount from the virtual filesystem."
await fs.unmount("/local")
```

### `pyscript.js_modules`

It is possible to [define JavaScript modules to use within your Python code](../user-guide/configuration#javascript-modules).

Such named modules will always then be available under the
`pyscript.js_modules` namespace.

!!! warning

    Please see the documentation (linked above) about restrictions and gotchas
    when configuring how JavaScript modules are made available to PyScript.

### `pyscript.storage`

The `pyscript.storage` API wraps the browser's built-in
[IndexDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
persistent storage in a synchronous Pythonic API.

!!! info 

    The storage API is persistent per user tab, page, or domain, in the same
    way IndexedDB persists.

    This API **is not** saving files in the interpreter's virtual file system
    nor onto the user's hard drive.

```python
from pyscript import storage


# Each store must have a meaningful name.
store = await storage("my-storage-name")

# store is a dictionary and can now be used as such.
```

The returned dictionary automatically loads the current state of the referenced
IndexDB. All changes are automatically queued in the background.

```python
# This is a write operation.
store["key"] = value

# This is also a write operation (it changes the stored data).
del store["key"]
```

Should you wish to be certain changes have been synchronized to the underlying
IndexDB, just `await store.sync()`.

Common types of value can be stored via this API: `bool`, `float`, `int`, `str`
and `None`. In addition, data structures like `list`, `dict` and `tuple` can
be stored.

!!! warning

    Because of the way the underlying data structure are stored in IndexDB,
    a Python `tuple` will always be returned as a Python `list`.

It is even possible to store arbitrary data via a `bytearray` or
`memoryview` object. However, there is a limitation that **such values must be
stored as a single key/value pair, and not as part of a nested data
structure**.

Sometimes you may need to modify the behaviour of the `dict` like object
returned by `pyscript.storage`. To do this, create a new class that inherits
from `pyscript.Storage`, then pass in your class to `pyscript.storage` as the
`storage_class` argument:

```python
from pyscript import window, storage, Storage


class MyStorage(Storage):

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        window.console.log(key, value)
        ...


store = await storage("my-data-store", storage_class=MyStorage)

# The store object is now an instance of MyStorage.
```

### `@pyscript/core/donkey`

Sometimes you need a Python worker ready and waiting to evaluate any code on
your behalf. This is the concept behind the JavaScript "donkey". We couldn't
think of a better way than "donkey" to describe something that is easy to
understand and shoulders the burden without complaint. This feature
means you're able to use PyScript without resorting to specialised
`<script type="py">` style tags. It's just vanilla JavaScript.

Simply `import { donkey } from '@pyscript/core/dist/core.js'` and automatically
have both a *pyscript* module running on your page and a utility to bootstrap a
terminal based worker to evaluate any Python code as and when needed in the
future.

```js title="A donkey worker"
import { donkey } from '@pyscript/core/dist/core.js';

const {
  process,              // process(code) code (visible in the terminal)
  execute,              // execute(statement) in Python exec way
  evaluate,             // evaluate(expression) in Python eval way
  clear,                // clear() the terminal
  reset,                // reset() the terminal (including colors)
  kill,                 // kill() the worker forever
} = donkey({
  type: 'py' || 'mpy',  // the Python interpreter to run
  persistent: false,    // use `true` to track globals and locals
  terminal: '',         // optionally set a target terminal container
  config: {},           // the worker config (packages, files, etc.)
});
```

By default PyScript creates a target terminal. If you don't want a terminal to
appear on your page, use the `terminal` option to point to a CSS addressable
container that is not visible (i.e. the target has `display: none`).

### `@pyscript/core/dist/storage.js`

The equivalent functionality based on the *JS* module can be found through our module.

The goal is to be able to share the same database across different worlds (interpreters) and the functionality is nearly identical except there is no *class* to provide because the storage in *JS* is just a dictionary proxy that synchronizes behind the scene all read, write or delete operations.

### `pyscript.web`

The classes and references in this namespace provide a Pythonic way to interact
with the DOM. An explanation for how to idiomatically use this API can be found
[in the user guide](../user-guide/dom/#pyscriptweb)

#### `pyscript.web.page`

This object represents a web page. It has four attributes and two methods:

* `html` - a reference to a Python object representing the [document's html](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/html) root element.
* `head` - a reference to a Python object representing the [document's head](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/head).
* `body` - a reference to a Python object representing the [document's body](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/body).
* `title` - the page's [title](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title) (usually displayed in the browser's title bar or a page's tab.
* `find` - a method that takes a single [selector](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors)
  argument and returns a collection of Python objects representing the matching
  elements.
* `append` - a shortcut for `page.body.append` (to add new elements to the
  page).

You may also shortcut the `find` method by enclosing a CSS selector in square
brackets: `page["#my-thing"]`.

These are provided as a convenience so you have several simple and obvious
options for accessing and changing the content of the page.

All the Python objects returned by these attributes and method are instances of
classes relating to HTML elements defined in the `pyscript.web` namespace.

#### `pyscript.web.*`

There are many classes in this namespace. Each is a one-to-one mapping of any
HTML element name to a Python class representing the HTML element of that
name. Each Python class ensures only valid properties and attributes can be
assigned, according to web standards.

Usage of these classes is
[explained in the user guide](../user-guide/dom/#pyscriptweb).

!!! info 

    The full list of supported element/class names is:

    ```
    grid
    a, abbr, address, area, article, aside, audio
    b, base, blockquote, body, br, button
    canvas, caption, cite, code, col, colgroup
    data, datalist, dd, del_, details, dialog, div, dl, dt
    em, embed
    fieldset, figcaption, figure, footer, form
    h1, h2, h3, h4, h5, h6, head, header, hgroup, hr, html
    i, iframe, img, input_, ins
    kbd
    label, legend, li, link
    main, map_, mark, menu, meta, meter
    nav
    object_, ol, optgroup, option, output
    p, param, picture, pre, progress
    q
    s, script, section, select, small, source, span, strong, style, sub, summary, sup
    table, tbody, td, template, textarea, tfoot, th, thead, time, title, tr, track
    u, ul
    var, video
    wbr
    ``` 

    These correspond to the standard
    [HTML elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
    with the caveat that `del_` and `input_` have the trailing underscore
    (`_`) because they are also keywords in Python, and the `grid` is a custom
    class for a `div` with a `grid` style `display` property.

    All these classes ultimately derive from the
    `pyscript.web.elements.Element` base class.

In addition to properties defined by the HTML standard for each type of HTML
element (e.g. `title`, `src` or `href`), all elements have the following
properties and methods (in alphabetical order):

* `append(child)` - add the `child` element to the element's children.
* `children` - a collection containing the element's child elements (that it
  contains).
* `classes` - a set of CSS classes associated with the element.
* `clone(clone_id=None)` - Make a clone of the element (and the underlying DOM
  object), and assign it the optional `clone_id`.
* `find(selector)` - use a CSS selector to find matching child elements.
* `parent` - the element's parent element (that contains it).
* `show_me` - scroll the element into view.
* `style` - a dictionary of CSS style properties associated with the element.
* `update(classes=None, style=None, **kwargs)` - update the element with the
  specified classes (set), style (dict) and DOM properties (kwargs).
* `_dom_element` - a reference to the proxy object that represents the
  underlying native HTML element.

!!! info

    All elements, by virtue of inheriting from the base `Element` class, may
    have the following properties:

    ```
    accesskey, autofocus, autocapitalize,
    className, contenteditable,
    draggable,
    enterkeyhint,
    hidden,
    innerHTML, id,
    lang,
    nonce,
    part, popover,
    slot, spellcheck,
    tabindex, text, title, translate,
    virtualkeyboardpolicy
    ```

The `classes` set-like object has the following convenience functions:

* `add(*class_names)` - add the class(es) to the element.
* `contains(class_name)` - indicate if `class_name` is associated with the
  element.
* `remove(*class_names)` - remove the class(es) from the element.
* `replace(old_class, new_class)` - replace the `old_class` with `new_class`.
* `toggle(class_name)` - add a class if it is absent, or remove a class if it
  is present.

Elements that require options (such as the `datalist`, `optgroup` and `select`
elements), can have options passed in when they are created:

```python
my_select = select_(option("apple", value=1), option("pear"))
```

Notice how options can be a tuple of two values (the name and associated value)
or just the single name (whose associated value will default to the given
name).

It's possible to access and manipulate the `options` of the resulting elements:

```python
selected_option = my_select.options.selected
my_select.options.remove(0)  # Remove the first option (in position 0).
my_select.clear()
my_select.options.add(html="Orange")
```

Finally, the collection of elements returned by `find` and `children` is
iterable, indexable and sliceable:

```python
for child in my_element.children[10:]:
    print(child.html)
```

Furthermore, four attributes related to all elements contained in the
collection can be read (as a list) or set (applied to all contained elements):

* `classes` - the list of classes associated with the elements.
* `innerHTML` - the innerHTML of each element.
* `style` - a dictionary like object for interacting with CSS style rules.
* `value` - the `value` attribute associated with each element.

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

### Or manually setting handler without a decorator
when("click", "#my-button", handler=click_handler)
```

This functionality is related to the `py-*` or `mpy-*` [HTML attributes](#html-attributes).

### `pyscript.window`

On the main thread, this object is exactly the same as `import js` which, in
turn, is a proxy of JavaScript's
[globalThis](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis)
object.

On a worker thread, this object is a proxy for the web page's
[global window context](https://developer.mozilla.org/en-US/docs/Web/API/Window).

!!! warning

    The reference for `pyscript.window` is **always** a reference to the main
    thread's global window context.

    If you're running code in a worker this is **not the worker's own global
    context**. A worker's global context is always reachable via `import js`
    (the `js` object being a proxy for the worker's `globalThis`).

### `pyscript.HTML`

A class to wrap generic content and display it as un-escaped HTML on the page.

```html title="The HTML class"
<script type="mpy">
    from pyscript import display, HTML

    # Escaped by default:
    display("<em>em</em>")  # &lt;em&gt;em&lt;/em&gt;
</script>

<script type="mpy">
    from pyscript import display, HTML

    # Un-escaped raw content inserted into the page:
    display(HTML("<em>em</em>"))  # <em>em</em>
</script>
```

### `pyscript.RUNNING_IN_WORKER`

This constant flag is `True` when the current code is running within a
*worker*. It is `False` when the code is running within the *main* thread.

### `pyscript.WebSocket`

If a `pyscript.fetch` results in a call and response HTTP interaction with a
web server, the `pyscript.Websocket` class provides a way to use
[websockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
for two-way sending and receiving of data via a long term connection with a
web server.

PyScript's implementation, available in both the main thread and a web worker,
closely follows the browser's own 
[WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) class.

This class accepts the following named arguments:

* A `url` pointing at the _ws_ or _wss_ address. E.g.:
  `WebSocket(url="ws://localhost:5037/")`
* Some `protocols`, an optional string or a list of strings as
  [described here](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/WebSocket#parameters).

The `WebSocket` class also provides these convenient static constants:

* `WebSocket.CONNECTING` (`0`) - the `ws.readyState` value when a web socket
  has just been created.
* `WebSocket.OPEN` (`1`) - the `ws.readyState` value once the socket is open.
* `WebSocket.CLOSING` (`2`) - the `ws.readyState` after `ws.close()` is
  explicitly invoked to stop the connection.
* `WebSocket.CLOSED` (`3`) - the `ws.readyState` once closed.

A `WebSocket` instance has only 2 methods:

* `ws.send(data)` - where `data` is either a string or a Python buffer,
  automatically converted into a JavaScript typed array. This sends data via
  the socket to the connected web server.
* `ws.close(code=0, reason="because")` - which optionally accepts `code` and
  `reason` as named arguments to signal some specific status or cause for
  closing the web socket. Otherwise `ws.close()` works with the default
  standard values.

A `WebSocket` instance also has the fields that the JavaScript
`WebSocket` instance will have:

* [binaryType](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/binaryType) -
  the type of binary data being received over the WebSocket connection.
* [bufferedAmount](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/bufferedAmount) -
  a read-only property that returns the number of bytes of data that have been
  queued using calls to `send()` but not yet transmitted to the network.
* [extensions](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/extensions) -
  a read-only property that returns the extensions selected by the server.
* [protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/protocol) -
  a read-only property that returns the name of the sub-protocol the server
  selected.
* [readyState](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/readyState) -
  a read-only property that returns the current state of the WebSocket
  connection as one of the `WebSocket` static constants (`CONNECTING`, `OPEN`,
  etc...).
* [url](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/url) -
  a read-only property that returns the absolute URL of the `WebSocket`
  instance.

A `WebSocket` instance can have the following listeners. Directly attach
handler functions to them. Such functions will always receive a single
`event` object.

* [onclose](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/close_event) -
  fired when the `WebSocket`'s connection is closed.
* [onerror](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/error_event) -
  fired when the connection is closed due to an error.
* [onmessage](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/message_event) -
  fired when data is received via the `WebSocket`. If the `event.data` is a
  JavaScript typed array instead of a string, the reference it will point
  directly to a _memoryview_ of the underlying `bytearray` data.
* [onopen](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/open_event) -
  fired when the connection is opened.

The following code demonstrates a `pyscript.WebSocket` in action.

```html
<script type="mpy" worker>
    from pyscript import WebSocket

    def onopen(event):
        print(event.type)
        ws.send("hello")

    def onmessage(event):
        print(event.type, event.data)
        ws.close()

    def onclose(event):
        print(event.type)

    ws = WebSocket(url="ws://localhost:5037/")
    ws.onopen = onopen
    ws.onmessage = onmessage
    ws.onclose = onclose
</script>
```

!!! info

    It's also possible to pass in any handler functions as named arguments when
    you instantiate the `pyscript.WebSocket` class:

    ```python
    from pyscript import WebSocket


    def onmessage(event):
        print(event.type, event.data)
        ws.close()


    ws = WebSocket(url="ws://example.com/socket", onmessage=onmessage)
    ```

### `pyscript.js_import`

If a JavaScript module is only needed under certain circumstances, we provide
an asynchronous way to import packages that were not originally referenced in
your configuration.

```html title="A pyscript.js_import example."
<script type="py">
from pyscript import js_import, window

escaper, = await js_import("https://esm.run/html-escaper")

window.console.log(escaper)
```

The `js_import` call returns an asynchronous tuple containing the JavaScript
modules referenced as string arguments.

### `pyscript.py_import`

!!! warning

    **This is an experimental feature.**

    Feedback and bug reports are welcome!

If you have a lot of Python packages referenced in your configuration, startup
performance may be degraded as these are downloaded.

If a Python package is only needed under certain circumstances, we provide an
asynchronous way to import packages that were not originally referenced in your
configuration.

```html title="A pyscript.py_import example."
<script type="py">
from pyscript import py_import

matplotlib, regex, = await py_import("matplotlib", "regex")

print(matplotlib, regex)
</script>
```

The `py_import` call returns an asynchronous tuple containing the Python
modules provided by the packages referenced as string arguments.

## Main-thread only features

### `pyscript.PyWorker`

A class used to instantiate a new worker from within Python.

!!! Note

    Sometimes we disambiguate between interpreters through naming conventions
    (e.g. `py` or `mpy`).

    However, this class is always `PyWorker` and **the desired interpreter 
    MUST be specified via a `type` option**. Valid values for the type of
    interpreter are either `micropython` or `pyodide`.

The following fragments demonstrate how to evaluate the file `worker.py` on a
new worker from within Python.

```python title="worker.py - the file to run in the worker."
from pyscript import RUNNING_IN_WORKER, display, sync

display("Hello World", target="output", append=True)

# will log into devtools console
print(RUNNING_IN_WORKER)  # True
print("sleeping")
sync.sleep(1)
print("awake")
```

```python title="main.py - starts a new worker in Python."
from pyscript import PyWorker

# type MUST be either `micropython` or `pyodide`
PyWorker("worker.py", type="micropython")
```

```html title="The HTML context for the worker."
<script type="mpy" src="./main.py">
<div id="output"></div>  <!-- The display target -->
```

### `pyscript.workers`

The `pyscript.workers` reference allows Python code in the main thread to
easily access named workers (and their exported functionality).

For example, the following Pyodide code may be running on a named worker
(see the `name` attribute of the `script` tag):

```html
<script type="py" worker name="py-version">
import sys

def version():
    return sys.version

# define what to export to main consumers
__export__ = ["version"]
</script>
```

While over on the main thread, this fragment of MicroPython will be able to
access the worker's `version` function via the `workers` reference:

```html
<script type="mpy">
from pyscript import workers

pyworker = await workers["py-version"]

# print the pyodide version
print(await pyworker.version())
</script>
```

Importantly, the `workers` reference will **NOT** provide a list of
known workers, but will only `await` for a reference to a named worker
(resolving when the worker is ready). This is because the timing of worker
startup is not deterministic.

Should you wish to await for all workers on the page at load time, it's
possible to loop over matching elements in the document like this:

```html
<script type="mpy">
from pyscript import document, workers

for el in document.querySelectorAll("[type='py'][worker][name]"):
    await workers[el.getAttribute('name')]

# ... rest of the code
</script>
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

These attributes, expressed as `py-*` or `mpy-*` attributes of an HTML element,
reference the name of a Python function to run when the event is fired. You
should replace the `*` with the _actual name of an event_ (e.g. `py-click` or
`mpy-click`). This is similar to how all
[event handlers on elements](https://html.spec.whatwg.org/multipage/webappapis.html#event-handlers-on-elements,-document-objects,-and-window-objects)
start with `on` in standard HTML (e.g. `onclick`). The rule of thumb is to
simply replace `on` with `py-` or `mpy-` and then reference the name of a
Python function.

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
