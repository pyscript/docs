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
powerful API that prioritizes common use cases first. For this reason, it's first
layer is simple and intuitive (but limited to the most common use cases), but `pydom`
also provides a secondary layer that can be used to directly use full the FFI interface
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

`Pydom` is built on the following core concepts:

* __`Element`:__ any component that is part of a web page. This is a rough abstraction of an
[HTMLElement](https://developer.mozilla.org/en-US/docs/Glossary/Element). In general,
`pydom` elements always map to an underlying `HTML` `Element` in a web page
* __`ElementCollection`:__ a collection of one or more `Elements`. It is a rough abstraction
of a [HTMLCollection](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCollection).
* __Querying:__ a method to query elements on a page based on a
[selector](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors). Pydom supports
standard HTML DOM query selectors to [locate DOM elements](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Locating_DOM_elements_using_selectors) as other native `JavaScript` methods like
`querySelector` or `querySelectorAll`.

In the following sections, we'll look into each one of these concepts.

### Element

`pydom` `Element` is an abstraction of a traditional `Element` in a web page.
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

The Element interface offers 2 main ways to set an element's content: the `html` and the
`content` attributes:

* `content`: sets the `innerHTML` field via the PyScript `display` function. This takes care
of properly rendering the object being passed based on the object mimetype. So, for instance,
if the objects is an image, it'll be properly rendered on the element.
* `html`: directly sets the `innerHTML` field of the underlying element without attempting
any conversion.

In general, we suggest using `content` directly as it'll take care of most use cases without
requiring any extra logic from the user.

#### Changing the element style

Elements have a `style` attribute that can be used to change the element style rules.
The style attribute can be used as a dictionary. To set a style rule for the element,
simply set the correct key on the `.style` attribute. For instance, the following
code changes the background color of the element just created in the example above:

```python
new_p.style["background-color"] = "yellow"
```

to remove a specific style key, simply use the same `pop` method you would use to remove
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
* `clone`: method that creates a clone of the element. NOTE: The clone elements will not be
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

Besides allowing operations as an iterable object, `ElementCollection` objects also offer a few
convenience methods to directly interact with the elements in the collection. For instance, it's possible
to ask for specific attributes of the elements in the collection directly:

```python
display(paragraphs.html)
```

The example above displays a list with the value of the `html` attribute for all the elements in the
`paragraphs` collection.

We can also set an attribute directly in the collection the same way we would read an attribute. For instance,
you can directly set the html content of all the elements in the collection:

```python
# This will change the text of all H1 elements in the page
pydom['h1'].html = "That's cool :)"
```

or perhaps change their style:

```
paragraphs.style['background-color'] = 'lightyellow'
```

`ElementCollection` currently supports the following attributes:

* `style`: just like in `Element`, this proxy attribute can be used to change the style of the elements in
a collection by setting the proper CSS rules, using `style` with the same API as a dictionary.
* `html`: allows you to change the `html` attribute on all the elements of a collection.
* `value`: allows you to change the `value` attribute on all the elements of a collection.
