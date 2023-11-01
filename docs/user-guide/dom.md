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

The built-in Python module `pydom` wraps many (although not all) the features
available via the FFI in an idiomatically Pythonic manner.


The PyDom API is extensively described and demonstrated
[on this PyScript page](https://fpliger.pyscriptapps.com/pyweb/latest/pydom.html).

!!! warning

    PyDom is currently a work in progress.

    We welcome feedback and suggestions.

**TODO Fabio to finish**
