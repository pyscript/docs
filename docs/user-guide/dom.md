# The DOM

The DOM
([document object model](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model))
is a tree like data structure representing the web page displayed by the
browser. PyScript interacts with the DOM to change the user interface and react
to things happening in the browser.

There are currently two ways to interact with the DOM:

1. Through the [foreign function interface](#ffi) (FFI) to interact with objects found
   in the browser's `globalThis` or `document` objects.
2. Through the [`pydom` module](#pydom) that acts as a Pythonic wrapper around
   the FFI and comes as standard with PyScript.

## FFI

The foreign function interface (FFI) gives Python access to all the
[standard web capabilities and features](https://developer.mozilla.org/en-US/docs/Web),
such as the browser's built-in
[web APIs](https://developer.mozilla.org/en-US/docs/Web/API).

This is available via the `pyscript.window` module which is a proxy for
the main thread's `globalThis` object, or `pyscript.document` which is a proxy
for the website's `document` object in JavaScript:

```Python title="Accessing the window and document objects in Python"
from pyscript import window, document


my_element = document.querySelector("#my-id")
my_element.innerText = window.location.hostname
```

The FFI creates _proxy objects_ in Python linked to _actual objects_ in
JavaScript.

The proxy objects in your Python code look and behave like Python
objects but have related JavaScript objects associated with them. It means the
API defined in JavaScript remains the same in Python, so any
[browser based JavaScript APIs](https://developer.mozilla.org/en-US/docs/Web/API)
or third party JavaScript libraries that expose objects in the web page's
`globalThis`, will have exactly the same API in Python as in JavaScript.

The FFI automatically transforms Python and JavaScript objects into the
equivalent in the other language. For example, Python's boolean `True` and
`False` will become JavaScript's `true` and `false`, while a JavaScript array
of strings and integers, `["hello", 1, 2, 3]` becomes a Python list of the
equivalent values: `["hello", 1, 2, 3]`.

!!! info

    Instantiating classes into objects is an interesting special case that the
    FFI expects you to handle.

    **If you wish to instantiate a JavaScript class in your Python
    code, you need to call the class's `new` method:**

    ```python
    from pyscript import window


    my_obj = window.MyJavaScriptClass.new("some value")

    ```

    The underlying reason for this is simply JavaScript and Python do
    instantiation very differently. By explicitly calling the JavaScript
    class's `new` method PyScript both signals and honours this difference.

    More technical information about instantiating JavaScript classes can be
    [found in the FAQ](../../faq/#javascript-classnew)

Should you require lower level API access to FFI features, you can find such
builtin functions under the `pyscript.ffi` namespace in both Pyodide and
MicroPython. The available functions are described in our section on the
[builtin API](../../api).

Advanced users may wish to explore the
[technical details of the FFI](../ffi).

## `pyscript.web` 

!!! warning

    The `pyscript.web` module is currently a work in progress.

    We welcome feedback and suggestions.

The `pyscript.web` module is an idiomatically Pythonic API for interacting with
the DOM. It wraps the FFI in a way that is more familiar to Python developers
and works natively with the Python language. Technical documentation for this
module can be found in [the API](../../api/#pyscriptweb) section.

There are three core concepts to remember:

* Find elements on the page via
  [CSS selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors).
  The `find` API uses exactly the [same queries](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Locating_DOM_elements_using_selectors)
  as those used by native browser methods like `qurerySelector` or
  `querySelectorAll`.
* Use classes in the `pyscript.web` namespace to create and organise
  new elements on the web page.
* Collections of elements allow you to access and change attributes en-mass.
  Such collections are returned from `find` queries and are also used for the
  [children](https://developer.mozilla.org/en-US/docs/Web/API/Element/children)
  of an element.

You have several options for accessing the content of the page, and these are
all found in the `pyscript.web.page` object. The `html`, `head` and `body`
attributes reference the page's top-level html, head and body. As a convenience
the `page`'s `title` attribute can be used to get and set the web page's title
(usually shown in the browser's tab). The `append` method is a shortcut for
adding content to the page's `body`. Whereas, the `find` method is used to
return collections of elements matching a CSS query. You may also shortcut
`find` via a CSS query in square brackets. Finally, all elements have a `find`
method that searches within their children for elements matching your CSS
query.

```python
from pyscript.web import page


# Print all the child elements of the document's head.
print(page.head.children)
# Find all the paragraphs in the DOM.
paragraphs = page.find("p")
# Or use square brackets.
paragraphs = page["p"]
```

The object returned from a query, or used as a reference to an element's
children is iterable:

```python
from pyscript.web import page


# Get all the paragraphs in the DOM.
paragraphs = page["p"]

# Print the inner html of each paragraph.
for p in paragraphs:
    print(p.html)
```

Alternatively, it is also indexable / sliceable:

```python
from pyscript.web import page


# Get an ElementCollection of all the paragraphs in the DOM
paragraphs = page["p"]

# Only the final two paragraphs.
for p in paragraphs[-2:]:
    print(p.html)
```

You have access to all the standard attributes related to HTML elements (for
example, the `innerHTML` or `value`), along with a couple of convenient ways
to interact with classes and CSS styles:

* `classes` - the list of classes associated with the elements.
* `style` - a dictionary like object for interacting with CSS style rules.

For example, to continue the example above, `paragraphs.innerHTML` will return
a list of all the values of the `innerHTML` attribute on each contained
element. Alternatively, set an attribute for all elements contained in the
collection like this: `paragraphs.style["background-color"] = "blue"`.

It's possible to create new elements to add to the page:

```python
from pyscript.web import page, div, select, option, button, span, br 


page.append(
    div(
        div("Hello!", classes="a-css-class", id="hello"),
        select(
            option("apple", value=1),
            option("pear", value=2),
            option("orange", value=3),
        ),
        div(
            button(span("Hello! "), span("World!"), id="my-button"),
            br(),
            button("Click me!"),
            classes=["css-class1", "css-class2"],
            style={"background-color": "red"}
        ),
        div(
            children=[
                button(
                    children=[
                        span("Hello! "),
                        span("Again!")
                    ],
                    id="another-button"
                ),
                br(),
                button("b"),
            ],
            classes=["css-class1", "css-class2"]
        )
    )
)
```

This example demonstrates a declaritive way to add elements to the body of the
page. Notice how the first (unnamed) arguments to an element are its children.
The named arguments (such as `id`, `classes` and `style`) refer to attributes
of the underlying HTML element. If you'd rather be explicit about the children
of an element, you can always pass in a list of such elements as the named
`children` argument (you see this in the final `div` in the example above).

Of course, you can achieve similar results in an imperative style of
programming:

```python
from pyscript.web import page, div, p 


my_div = div()
my_div.style["background-color"] = "red"
my_div.classes.add("a-css-class")

my_p = p()
my_p.content = "This is a paragraph."

my_div.append(my_p)

# etc...
```

It's also important to note that the `pyscript.when` decorator understands
element references from `pyscript.web`:

```python
from pyscript import when
from pyscript.web import page 


btn = page["#my-button"]


@when("click", btn)
def my_button_click_handler(event):
    print("The button has been clicked!")
```

Should you wish direct access to the proxy object representing the underlying
HTML element, each Python element has a `_dom_element` property for this
purpose.

Once again, the technical details of these classes are described in the
[built-in API documentation](../../api/#pyscriptweb).

## Working with JavaScript

There are three ways in which JavaScript can get into a web page.

1. As a global reference attached to the `window` object in the web page
   because the code was referenced as the source of a `script` tag in your HTML
   (the very old school way to do this).
2. Using the [Universal Module Definition](https://github.com/umdjs/umd) (UMD),
   an out-of-date and non-standard way to create JavaScript modules.
3. As a standard
   [JavaScript Module](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
   which is the modern, standards compliant way to define and use a JavaScript
   module. If possible, this is the way you should do things.

Sadly, this being the messy world of the web, methods 1 and 2 are still quite
common, and so you need to know about them so you're able to discern and work
around them. There's nothing WE can do about this situation, but we can
suggest "best practice" ways to work around each situation.

Remember, as mentioned
[elsewhere in our documentation](../configuration/#javascript-modules),
the standard way to get JavaScript modules into your PyScript Python context is
to link a _source_ standard JavaScript module to a _destination_ name:

```toml title="Reference a JavaScript module in the configuration."
[js_modules.main]
"https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet-src.esm.js" = "leaflet"
```

Then, reference the module via the destination name in your Python code, by
importing it from the `pyscript.js_modules` namespace:

```python title="Import the JavaScript module into Python"
from pyscript.js_modules import leaflet as L

map = L.map("map")

# etc....
```

We'll deal with each of the potential JavaScript related situations in turn:

### JavaScript as a global reference

In this situation, you have some JavaScript code that just globally defines
"stuff" in the context of your web page via a `script` tag. Your HTML will
contain something like this:

```html title="JavaScript as a global reference"
<!doctype html>
<!--
This JS utility escapes and unescapes HTML chars. It adds an "html" object to
the global context.
-->
<script src="https://cdn.jsdelivr.net/npm/html-escaper@3.0.3/index.js"></script>

<!--
Vanilla JS just to check the expected object is in the global context of the
web page.
-->
<script>
    console.log(html);
</script>
```

When you find yourself in this situation, simply use the `window` object in
your Python code (found in the `pyscript` namespace) to interact with the
resulting JavaScript objects:

```python title="Python interaction with the JavaScript global reference"
from pyscript import window, document


# The window object is the global context of your web page.
html = window.html

# Just use the object "as usual"...
# e.g. show escaped HTML in the body: &lt;&gt;
document.body.append(html.escape("<>"))
```

You can find an example of this technique here:

[https://pyscript.com/@agiammarchi/floral-glade/v1](https://pyscript.com/@agiammarchi/floral-glade/v1)

### JavaScript as a non-standard UMD module

Sadly, these sorts of non-standard JavaScript modules are still quite
prevalent. But the good news is there are strategies you can use to help you
get them to work properly.

The non-standard UMD approach tries to check for `export` and `module` fields
in the JavaScript module and, if it doesn’t find them, falls back to treating
the module in the same way as a global reference described above.

If you find you have a UMD JavaScript module, there are services online to
automagically convert it to the modern and standards compliant way to d
o JavaScript modules. A common (and usually reliable) service is provided by
[https://esm.run/your-module-name](https://esm.run/your-module-name), a
service that provides an out of the box way to consume the module in the
correct and standard manner:

```html title="Use esm.run to automatically convert a non-standard UMD module"
<!doctype html>
<script type="module">
    // this utility escapes and unescape HTML chars
    import { escape, unescape } from "https://esm.run/html-escaper";
    // esm.run returns a module       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    console.log(escape("<>"));
    // log: "&lt;&gt;"
</script>
```

If a similar test works for the module you want to use, use the esm.run CDN
service within the `py` or `mpy` configuration file as explained at the start
of this section on JavaScript (i.e. you'll use it via the `pyscript.js_modules`
namespace).

If this doesn't work, assume the module is not updated nor migrated to a state
that can be automatically translated by services like esm.run. You could try an
alternative (more modern) JavaScript module to achieve you ends or (if it
really must be this module), you can wrap it in a new JavaScript module that
conforms to the modern standards.

The following four files demonstrate this approach:

```html title="index.html - still grab the script so it appears as a global reference."
<!doctype html>
...
<!-- land the utility still globally as generic script -->
<script src="https://cdn.jsdelivr.net/npm/html-escaper@3.0.3/index.js"></script>
...
```

```js title="wrapper.js - this grabs the JavaScript functionality from the global context and wraps it (exports it) in the modern standards compliant manner."
// get all utilities needed from the global.
const { escape, unescape } = globalThis.html;

// export utilities like a standards compliant module would do.
export { escape, unescape };
```

```toml title="pyscript.toml - configure your JS modules as before, but use your wrapper instead of the original module."
[js_modules.main]
# will simulate a standard JS module
"./wrapper.js" = "html_escaper"
```

```python title="main.py - just import the module as usual and make use of it."
from pyscript import document

# import the module either via
from pyscript.js_modules import html_escaper
# or via
from pyscript.js_modules.html_escaper import escape, unescape

# show on body: &lt;&gt;
document.body.append(html.escape("<>"))
```

You can see this approach in action here:

[https://pyscript.com/@agiammarchi/floral-glade/v2](https://pyscript.com/@agiammarchi/floral-glade/v2)

### A standard JavaScript module

This is both the easiest and best way to import any standard JS module into
Python.

You don't need to reference the script in your HTML, just define how the source
JavaScript module maps into the `pyscript.js_modules` namespace in your
configuration file, as explained above.

That's it!

Here is an example project that uses this approach:

[https://pyscript.com/@agiammarchi/floral-glade/v3](https://pyscript.com/@agiammarchi/floral-glade/v3)


### My own JavaScript code

If you have your own JavaScript work, just remember to write it as a standard
JavaScript module. Put simply, ensure you `export` the things you need to. For
instance, in the following fragment of JavaScript, the two functions are
exported from the module:

```js title="code.js - containing two functions exported as capabilities of the module."
/*
Some simple JavaScript functions for example purposes.
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

Next, just reference this module in the usual way in your TOML or JSON
configuration file:

```TOML title="pyscript.toml - references the code.js module so it will appear as the code module in the pyscript.js_modules namespace."
[js_modules.main]
"code.js" = "code"
```

In your HTML, reference your Python script with this configuration file:

```html title="Reference the expected configuration file."
<script type="py" src="./main.py" config="./pyscript.toml" terminal></script>
```

Finally, just use your JavaScript module’s exported functions inside PyScript:

```python title="Just call your bespoke JavaScript code from Python."
from pyscript.js_modules import code


# Just use the JS code from Python "as usual".
greeting = code.hello("Chris")
print(greeting)
result = code.fibonacci(12)
print(result)
```

You can see this in action in the following example project:

[https://pyscript.com/@ntoll/howto-javascript/latest](https://pyscript.com/@ntoll/howto-javascript/latest)
