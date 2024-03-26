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


## PyDom

The Standard Web APIs are massive and not always very user-friendly. `PyDom` is a
Python module that exposes the power of the web with an easy and idiomatic Pythonic
interface on top.

While the [FFI](#ffi) interface described above focuses on giving full access to
the entire Standard Web APIs, `pydom` focuses on providing a small, intuitive and yet
powerful API that prioritises common use cases fist. For this reason, its first
layer is simple and intuitive (but limited to the most common use cases), but `pydom`
also provides a secondary layer that can be used to directly use full FFI interface
of a specific element.

It does not aim to replace the regular Web [Javascript] API nor to be as wide and offer
feature parity. On the contrary, it's intentionally small and focused on the most popular
use cases while still providing [a backdoor] access to the full JS API.

`Pydom` draws inspiration from popular Python APIs/Libraries known to be friendly and
easy to learn, and other successful projects related the web as well (for instance,
`JQuery` was a good source of inspiration).

!!! warning

    PyDom is currently a work in progress.

    We welcome feedback and suggestions.


### Core Concepts

`Pydom` builds on topic of very few and simple core concepts:

* __`Element`:__ any component that is part of a web page. This is a rough abstraction of an
[HTMLElement](https://developer.mozilla.org/en-US/docs/Glossary/Element). In general,
`pydom` elements always map to an underlying `HTML` `Element` in a web page
* __`ElementCollection`:__ a collection of one or more `Elements`. It is a rough abstraction
of a [HTMLCollection](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCollection).
* __Querying:__ a method to query elements on a page based on a
[selector](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors). Pydom supports
standard HTML DOM query selectors to [locate DOM elements](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Locating_DOM_elements_using_selectors) as other native `JavaScript` methods like
`querySelector` or `querySelectorAll`.

Following, we'll look into each one of these aspects a bit more in detail.

### Element

`pydom` `Element` is simply just an abstraction of a tranditional `Element` in a web page.
Every `Element` always maps to an underlying `JavaScript` `Element` in a web page. These 2
elements are always in sync and any change of state in one is reflected in the other.

#### Creating a new element

New elements can be created by using the `pydom.create` method and passing the type of element
being created. Here's an example of what it looks like:

(To execute and explore the following code, click on the "load" button. The result will be
conveniently displayed in the box on the below of the code example)

```python
from pyweb import pydom

# Creating an element directly from pydom creates an unbounded element.
new_div = pydom.create("div")

# Creating an element from another element automatically creates that element
# as a child of the original element
new_p = new_div.create("p", classes=["code-description"], html="Ciao PyScripters!")

# elements can be appended to any other element on the page
pydom['#element-creation-example'][0].append(new_div)
```

<div>
  <h5>Result will go here</h5>
  <div id="pydom-element-createion-example"></div>
</div>


For more details about `pydom.create` please refer to its reference documentation.

#### Setting the content of an element

The Element interface offers 2 main ways to set an element content: the `html` and the
`content` attributes:

* `content`: sets the `innerHTML` field via the PyScript `display` function. This takes care
of properly rendering the object being passed based on the object mimetype. So, for instance,
if the objects is an image, it'll be properly rendered on the element
* `html`: directly sets the `innerHTML` field of the underlying element without attemnpting
any conversion.

In general, we suggest using `content` directly as it'll take care of most use cases without
requiring any extra logic from the user.

#### Changing the element style

Elements have a `style` attribute that can be used to change the element style rules.
The style attribute can be used as a dictionary and, to set a style rule for the element,
simply set the correct key on the `.style` attribute. For instance, the following
code changes the background color of the element just created in the example above:

```python
new_p.style["background-color"] = "yellow"
```

to remove a specific style key, simply use the `pop` method as you'd to to remove
a key from a dictionary:

```python
new_p.style.pop("background-color")
```

In addition to the dictionary interface to explicitly set CSS rules, the `style` attribute
also offers a convenient `visible` property that can be use show/hide an element.

```python
new_p.style.visible = False
```

#### Other useful aspects of the Element API

* `append`: method to append a new child to the element.
* `children`: list of the children of the element.
* `value`: allows to set the `value` attribute of an element.
* `clone`: method that creates a clone of the element. NODE: The clone elements will not be
attached to any element.
* `show_me`: method to scroll the page to where the element is placed.


### ElementCollection

Element Collections represent a collection of elements typically returned from a query. For instance:

```python
paragraphs = pydom['p']
```

In the example above, `paragraphs` is an `ElementCollection` that maps to all `p` elements in the page.

As any collections, `ElementCollection` can be used to iterate over a collection of elements or to pick
specific elements or slices of elements in the collection. For instance:

```python
for element in paragraphs: 
  display(element.html)

# let's now display only the last 2 elements
for element in paragraphs[-2:]:
  display(element.html)
```

#### Interacting with an ElementCollection

Besides from allowing operations as an iterable object, `ElementCollection` objects also offer a few
convenient methods to directly interact with th elements in the collection. For instance, it's possible
to ask for specific attributes of the elements in the collection directly:

```python
display(paragraphs.html)
```

The example above displays a list with the value of the `html` attribute for all the elements in the
`paragraphs` collection.

The same way we can read attributes, we can also set an attribute directly in the collection. For instance,
you can directly set the html content of all the elements in the collection

```python
# This will change the text of all H1 elements in the page
pydom['h1'].html = "That's cool :)"
```

or perhaps change their style

```
paragraphs.style['background-color'] = 'lightyellow'
```

`ElementCollection` currently support the following attributes:

* `style`: just like in `Element`, this proxy attribute can be used to change the style of the elements in
a collection by setting the proper CSS rules, using `style` with the same API as a dictionary.
* `html`: allows to change the `html` attribute on all the elements of a collection.
* `value`: allows to change the `value` attribute on all the elements of a collection.

## Working with JavaScript

There are three ways in which JavaScript can get into a web page.

1. As a global reference attached to the `window` object in the web page
   because the code was referenced as the source of a `script` tag in your HTML
   (the very old school way to do this).
2. Using the [Universal Module Definition](https://github.com/umdjs/umd) (UMD)
   - an out-of-date and non-standard way to create JavaScript modules.
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
    import { escape, unescape } from "https://esm.run/html-escape";
    // esm.run returns a module       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
