# The DOM

The DOM
([document object model](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model))
is a tree-like data structure representing the web page displayed by
the browser. PyScript interacts with the DOM to change the user
interface and react to things happening in the browser.

PyScript provides two ways to work with the DOM:

1. **The `pyscript.web` module** - A Pythonic interface that feels
   natural to Python developers. This is the recommended approach for
   most tasks.
2. **The FFI (foreign function interface)** - Direct access to
   JavaScript APIs for advanced use cases or when you need complete
   control.

Both approaches are powerful and can accomplish the same goals. We'll
explore each one, starting with the Pythonic `pyscript.web` module.

!!! tip

    **New to PyScript?** Start with `pyscript.web`. It's designed to
    feel natural if you know Python, and it handles many common tasks
    more elegantly than direct JavaScript API calls.
    
    The FFI becomes useful when you need to integrate specific
    JavaScript libraries or when you're already familiar with web
    development in JavaScript.

## Quick start: pyscript.web

The `pyscript.web` module provides an idiomatic Python interface to the
DOM. It wraps the FFI in a way that feels natural to Python developers,
with familiar patterns like dictionary-style access, set-like class
management, and Pythonic method names.

### Finding elements

The `page` object represents your web page. Use it to find elements by
their ID or with CSS selectors:

```python
from pyscript import web


# Get an element by ID (returns single Element or None).
header = web.page["header-id"]
header = web.page["#header-id"]  # The "#" prefix is optional.

# Find by CSS selector (returns an ElementCollection).
divs = web.page.find("div")
buttons = web.page.find(".button-class")
items = web.page.find("#list .item")

# Access page structure.
web.page.body.append(some_element)
web.page.title = "New Page Title"
```

CSS selectors work exactly like they do in CSS or JavaScript's
[`querySelector`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector).
If you can select it in CSS, you can find it with `pyscript.web`.

### Creating elements

Create new HTML elements using simple Python classes. Element
names correspond to HTML tags, and are lower-case to match web
conventions. Compose elements together in a
[declarative style](https://en.wikipedia.org/wiki/Declarative_programming):

```python
from pyscript import web


# Create simple elements.
div = web.div("Hello, World!")
paragraph = web.p("Some text", id="my-para", classes=["intro"])

# Compose elements together.
container = web.div(
    web.h1("My Task List"),
    web.p("Keep track of your work"),
    web.ul(
        web.li("First task"),
        web.li("Second task"),
        web.li("Third task")
    ),
    id="task-container",
    classes=["panel", "primary"]
)

# Add to the page.
web.page.body.append(container)
```

The first (unnamed) arguments to an element become its children. Named
arguments like `id`, `classes`, and `style` set HTML attributes.

You can also create elements
[imperatively](https://en.wikipedia.org/wiki/Imperative_programming):

```python
from pyscript import web


# Create an empty div.
my_div = web.div(id="my-container")

# Add content and styling.
my_div.innerHTML = "<p>Hello!</p>"
my_div.classes.add("active")
my_div.style["background-color"] = "lightblue"

# Create a paragraph and add it.
my_p = web.p("This is a paragraph.")
my_div.append(my_p)
```

### Modifying content and attributes

Once you have an element, you can modify its content and attributes
using idiomatic Python:

```python
from pyscript import web


element = web.page["my-element"]

# Update content.
element.innerHTML = "<b>Bold text</b>"
element.textContent = "Plain text"

# Update attributes.
element.id = "new-id"
element.title = "Tooltip text"

# Bulk update with convenience method.
element.update(
    classes=["active", "highlighted"],
    style={"color": "red", "font-size": "16px"},
    title="Updated tooltip"
)
```

### Working with classes and styles

Element classes behave like a Python `set`, and styles behave like a
Python `dict`:

```python
from pyscript import web


element = web.page["my-button"]

# Classes work like sets.
element.classes.add("active")
element.classes.add("highlighted")
element.classes.remove("hidden")
element.classes.discard("maybe-not-there")  # No error if missing.

# Check membership.
if "active" in element.classes:
    print("Element is active")

# Clear all classes.
element.classes.clear()

# Styles work like dictionaries.
element.style["color"] = "red"
element.style["background-color"] = "#f0f0f0"
element.style["font-size"] = "16px"

# Remove a style.
del element.style["margin"]

# Check if style is set.
if "color" in element.style:
    print(f"Colour is {element.style['color']}")
```

### Working with collections

When you find multiple elements, you get an `ElementCollection` that
you can iterate over, slice, or update in bulk:

```python
from pyscript import web


# Find multiple elements (returns an ElementCollection).
items = web.page.find(".list-item")

# Iterate over collection.
for item in items:
    item.innerHTML = "Updated"
    item.classes.add("processed")

# Bulk update all elements.
items.update_all(
    innerHTML="New content",
    classes=["updated-item"]
)

# Index and slice collections.
first = items[0]
last = items[-1]
subset = items[1:3]

# Get an element by ID within the collection.
special = items["special-id"]

# Find descendants within the collection.
subitems = items.find(".sub-item")
```

### Managing select elements

The `select` element contains a list of `option` instances from which you
select. When rendered on a web page, it looks like this:

<label for="example_option">Choose an option: </label>
<select id="example_option">
  <option>Option 1</option>
  <option>Option 2</option>
  <option>Option 3</option>
</select>

The `options` property of `select` elements provides convenient methods
for managing such options:

```python
from pyscript import web


# Get an existing select element.
select = web.page["my-select"]

# Add options.
select.options.add(value="1", html="Option 1")
select.options.add(value="2", html="Option 2", selected=True)

# Get the selected option.
selected = select.options.selected
print(f"Selected: {selected.value}")

# Iterate over options.
for option in select.options:
    print(f"{option.value}: {option.innerHTML}")

# Clear all options.
select.options.clear()

# Remove specific option by index.
select.options.remove(0)
```

This also works for `datalist` and `optgroup` elements, that also require
lists of options to function.

### Event handling with pyscript.web

The `@when` decorator works seamlessly with `pyscript.web` elements:

```python
from pyscript import when, web


# Create a button.
button = web.button("Click me", id="my-button")
web.page.body.append(button)

# Attach event handler with decorator.
@when("click", button)
def handle_click(event):
    print("Button clicked!")

# Or attach during creation.
def another_handler(event):
    print("Another handler")

button2 = web.button("Click too", on_click=another_handler)
```

Learn more about event handling in the [events guide](events.md).

### Direct DOM access

When needed, you can access the underlying DOM element directly:

```python
from pyscript import web


element = web.page["my-element"]

# Most DOM methods are accessible directly.
element.scrollIntoView()
element.focus()
element.blur()

# Convenience method for scrolling.
element.show_me()  # Calls scrollIntoView().

# Access the raw underlying DOM element for special cases.
dom_element = element._dom_element
```

!!! info

    For complete API documentation of `pyscript.web`, including all
    available element types and methods, see the
    [API reference](../../api/web).

## Example: Task board with pyscript.web

Let's look at a complete example that demonstrates these concepts. This
task board application lets users add tasks, mark them complete, filter
by priority, and delete tasks:

<iframe src="../../example-apps/task-board-web/" style="border: 1px solid black; width:100%; min-height: 500px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-web).

Notice how the code uses Pythonic patterns throughout: dictionary-style
access for elements, set operations for classes, and familiar Python
syntax for creating and modifying elements.

## The FFI: JavaScript interoperability

The foreign function interface (FFI) gives Python direct access to all
the [standard web capabilities and features](https://developer.mozilla.org/en-US/docs/Web),
including the browser's built-in
[web APIs](https://developer.mozilla.org/en-US/docs/Web/API).

This is available via the `pyscript.window` and `pyscript.document`
objects, which are proxies for JavaScript's `globalThis` and `document`
objects:

```python
from pyscript import window, document


# Access browser APIs.
hostname = window.location.hostname
current_url = window.location.href

# Find and manipulate DOM elements.
my_element = document.querySelector("#my-id")
my_element.innerText = "Hello from Python!"

# Query all matching elements.
paragraphs = document.querySelectorAll("p")
for p in paragraphs:
    p.style.color = "blue"
```

### Proxy objects

The FFI creates _proxy objects_ in Python that are linked to _actual
objects_ in JavaScript. These proxy objects look and behave like Python
objects but have related JavaScript objects associated with them
"in the background" and automatically managed for you by the FFI.

This means the API defined in JavaScript remains the same in Python, so
any [browser-based JavaScript APIs](https://developer.mozilla.org/en-US/docs/Web/API)
or third-party JavaScript libraries that expose objects in the web
page's `globalThis` will have exactly the same API in Python as in
JavaScript.

### Type conversions

The FFI automatically transforms Python and JavaScript objects into
their equivalent in the other language:

| Python | JavaScript |
|--------|------------|
| `True`, `False` | `true`, `false` |
| `None` | `null` or `undefined` |
| `int`, `float` | `number` |
| `str` | `string` |
| `list` | `Array` |
| `dict` | `Object` |

For example, a JavaScript array `["hello", 1, 2, 3]` becomes a Python
list `["hello", 1, 2, 3]`, and vice versa.

### JavaScript class instantiation

Instantiating JavaScript classes requires special handling because
Python and JavaScript do it differently:

```python
from pyscript import window


# To instantiate a JavaScript class, call its .new() method.
my_obj = window.MyJavaScriptClass.new("some value")

# This is equivalent to JavaScript: new MyJavaScriptClass("some value")
```

The `.new()` method is required because Python and JavaScript handle
class instantiation very differently. By explicitly calling `.new()`,
PyScript signals and honours this difference.

!!! info

    For more technical details about JavaScript class instantiation,
    see the [FAQ](../../faq/#javascript-classnew).

### Lower-level FFI features

Advanced users who need lower-level access to FFI features can use
functions in the `pyscript.ffi` namespace, available in both Pyodide
and MicroPython. These functions are documented in the
[API reference](../../api/ffi).

For deep technical details about how the FFI works, see the
[FFI technical guide](ffi.md).

## Example: Task board with FFI

Here's the same task board application implemented using the FFI and
direct JavaScript APIs instead of `pyscript.web`:

<iframe src="../../example-apps/task-board-ffi/" style="border: 1px solid black; width:100%; min-height: 500px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/task-board-ffi).

Compare this implementation with the `pyscript.web` version above.
Notice how the FFI version uses JavaScript method names like
`querySelector` and `createElement`, whilst the `pyscript.web` version
uses Pythonic patterns.


## Working with JavaScript libraries

There are three ways JavaScript code typically appears in web pages.
Understanding these helps you integrate JavaScript libraries into your
PyScript applications.

### Standard JavaScript modules (recommended)

Modern JavaScript uses ES6 modules with `import` and `export`
statements. This is the best way to integrate JavaScript:

```toml title="pyscript.toml - Configure JavaScript modules"
[js_modules.main]
"https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet-src.esm.js" = "leaflet"
```

Then import the module in your Python code:

```python title="main.py - Use the JavaScript module"
from pyscript.js_modules import leaflet as L


map = L.map("map")
# Use the library...
```

That's it! PyScript handles loading the module and making it available
in Python.

!!! tip

    This is the recommended approach. Most modern JavaScript libraries
    provide ES6 module builds that work perfectly with this method.

### JavaScript as a global reference (legacy)

Older JavaScript code may add objects directly to the global `window`
object via a `<script>` tag:

```html title="HTML with global JavaScript"
<!doctype html>
<html>
  <head>
    <!-- This adds an 'html' object to the global scope. -->
    <script src="https://cdn.jsdelivr.net/npm/html-escaper@3.0.3/index.js"></script>
  </head>
  <body>
    <!-- Your content -->
  </body>
</html>
```

Access these global objects via the `window` object in Python:

```python title="main.py - Access global JavaScript"
from pyscript import window, document


# The window object is the global context.
html = window.html

# Use the object normally.
escaped = html.escape("<>")
document.body.append(escaped)
```

### UMD modules (legacy)

The Universal Module Definition (UMD) is an outdated, non-standard way
to create JavaScript modules. If you encounter UMD modules, you have
two options:

**Option 1: Use esm.run** - This service automatically converts UMD
modules to standard ES6 modules:

```toml title="pyscript.toml - Use esm.run to convert UMD"
[js_modules.main]
"https://esm.run/html-escaper" = "html_escaper"
```

**Option 2: Create a wrapper** - If esm.run doesn't work, wrap the
module yourself:

```html title="index.html - Load the UMD module globally"
<script src="https://cdn.jsdelivr.net/npm/html-escaper@3.0.3/index.js"></script>
```

```js title="wrapper.js - Wrap it as a standard module"
// Get utilities from the global scope.
const { escape, unescape } = globalThis.html;

// Export as a standard module.
export { escape, unescape };
```

```toml title="pyscript.toml - Reference your wrapper"
[js_modules.main]
"./wrapper.js" = "html_escaper"
```

```python title="main.py - Use it normally"
from pyscript.js_modules import html_escaper


escaped = html_escaper.escape("<>")
```

### Your own JavaScript code

Write your own JavaScript as standard ES6 modules by using `export`:

```js title="code.js - Your JavaScript module"
/*
Simple JavaScript functions for example purposes.
*/

export function hello(name) {
    return "Hello " + name;
}

export function fibonacci(n) {
    if (n == 1) return 0;
    if (n == 2) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

Reference it in your configuration:

```toml title="pyscript.toml"
[js_modules.main]
"code.js" = "code"
```

Use it from Python:

```python title="main.py"
from pyscript.js_modules import code


greeting = code.hello("Chris")
print(greeting)

result = code.fibonacci(12)
print(result)
```

For more details on configuring JavaScript modules, see the
[configuration guide](configuration.md/#javascript-modules).

## When to use which approach

Both `pyscript.web` and the FFI are powerful tools. Here's when to use
each:

### Use pyscript.web when:

- **You're comfortable with Python** - The API feels natural to Python
  developers, with Pythonic naming and patterns.
- **You're building from scratch** - Creating new elements and
  composing interfaces is elegant and concise.
- **You value readability** - The code is self-documenting and easy to
  understand.
- **You're teaching or learning** - The interface is easier to
  explain and understand to Python learners.

### Use the FFI when:

- **You're integrating JavaScript libraries** - Direct access to
  JavaScript APIs means no translation layer.
- **You're porting existing JavaScript code** - The API is identical,
  making translation straightforward.
- **You need a specific browser API** - Some browser features don't
  have `pyscript` based wrappers (yet!).
- **You're already familiar with web development** - If you know
  JavaScript, the FFI feels natural.

!!! tip

    You can mix both approaches in the same application. Use
    `pyscript.web` for most tasks and drop down to the FFI when needed.
    They work together seamlessly.

## What's next

Now that you understand DOM manipulation, explore these related topics:

**[Events](events.md)** - Learn how to respond to user actions and
browser events with the `@when` decorator and event handlers.

**[Display](display.md)** - Discover how to show Python objects, images,
charts, and rich content on your page with the `display()` function.

**[Configuration](configuration.md)** - Configure your Python
environment, specify packages, and customise PyScript's behaviour.

**[Workers](workers.md)** - Run Python code in background threads for
responsive applications.