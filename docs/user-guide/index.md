# Introduction (start here)

!!! note

    This guide provides detailed technical guidance for developers who want
    an in depth explanation of the PyScript platform.

    As a result, while we endeavour to write clearly, some of the content in
    this user guide will not be suitable for beginners. We assume the folks who
    will get most from this guide will already have some Python or web
    development experience.

    We welcome feedback to help us improve.

This guide is in three parts:

1. The brief overview, context setting and sign-posting contained within this
   page.
2. The other pages of the guide, referenced from this page, that explore the
   different aspects of PyScript in substantial technical detail.
3. The example projects, listed at the end of this page, that demonstrate the
   various features of PyScript working together in real-world applications.

We suggest you _read this page in full_: it will ensure you have a 
comprehensive overview of the PyScript platform along with suggestions for
where next to explore.

When you require depth and technical detail you should consult the other pages
of this guide that are referenced from this page. They provide clear and
precise details along with example code fragments and descriptions of the APIs
available via PyScript.

Finally, the examples listed at the end of this page are all freely available
and copiously commented on [pyscript.com](pyscript.com). You should consult
these for practical "real world" use of the various features of the PyScript
platform. Many of these examples come from contributors to our wonderful
community. If you believe you have a project that would make a good example,
please don't hesitate to get in touch.

## What is PyScript?

PyScript is a platform for Python in the browser.

PyScript's aim is to bring together two of the most vibrant technical
ecosystems on the planet. If the web and Python had a baby, you'd get PyScript.

PyScript works because modern browsers support
[web assembly](https://webassembly.org/) (abbreviated to WASM) - a virtual
machine with an open specification and near native performance. PyScript takes
versions of the Python interpreter compiled to WASM, and makes them easy to use
from within your browser.

At the core of PyScript is a philosophy of digital empowerment. The web is the
world's most ubiquitous computing platform, mature and familiar to billions of
people. Python is one of the world's most popular programming languages:
easy to teach and learn, used in a plethora of existing domains
such as data science, games, embedded systems, artificial intelligence and
film making (to name but a few), and the Python ecosystem contains a huge
number of libraries to address its many uses.

PyScript brings together the ubiquity and accessibility of the web with the
power, depth and expressiveness of Python. It means PyScript isn't just for
programming experts but, as we like to say, for the 99% of the rest of the
planet who use computers.

## Features

<dl>
    <dt><strong>All the web</strong></dt>
    <dd>
    <p>Thanks to the foreign function interface (FFI), PyScript gives you
    access to all the
    <a href="https://developer.mozilla.org/en-US/docs/Web/API">web
    APIs implemented by your browser</a>.</p>

    <p>The FFI makes it easy for Python to work within your browser, including
    with third party JavaScript libraries that may be included via the
    <code>script</code> tag.</p>

    <p>The FFI is bi-directional ~ it also enables JavaScript to access the
    power of PyScript.</p></dd>
    <dt><strong>All of Python</strong></dt>
    <dd>
    <p>PyScript brings you two Python interpreters:</p>
    <ol>
        <li><a href="https://pyodide.org/">Pyodide</a> - the original standard
        CPython interpreter you know and love, but compiled to web
        assembly.</li>
        <li><a href="https://micropython.org/">MicroPython</a> - a lean and
        efficient reimplementation of Python3 that includes a comprehensive
        subset of the standard library, compiled to web assembly.</li>
    </ol>
    <p>Because it is just regular CPython, Pyodide puts Python's deep and
    diverse ecosystem of libraries, frameworks and modules at your disposal. If
    you find yourself encountering some sort of computing problem, there's
    probably a Python library to help you with it. If you're used to using a
    favourite library in Python, now you can use it in your browser and share
    it with the ease of a URL.</p>
    <p>MicroPython, because of its small size (170k) and speed, is especially
    suited to running on more constrained browsers, such as those on mobile
    or tablet devices. It includes a powerful sub-set of the Python standard
    library and efficiently exposes the expressiveness of Python to the
    browser.</p>
    <p>Both Python interpreters supported by PyScript implement the same
    API to bridge the gap between the worlds of Python and the browser.</p>
    </dd>
    <dt><strong>Data science built in</strong></dt>
    <dd>Python is famous for its extraordinary usefulness in data science
    and artificial intelligence. The Pyodide interpreter comes with many of the
    libraries you need for this sort of work already baked in.</dd>
    <dt><strong>Mobile friendly MicroPython</strong></dt>
    <dd>
    <p>Thanks to MicroPython in PyScript, there is a compelling story for
    Python on mobile.</p>

    <p>MicroPython is small and fast enough that your app will start quickly
    on first load, and almost instantly (due to the cache) on subsequent
    runs.</p></dd>
    <dt><strong>Parallel execution</strong></dt>
    <dd>Thanks to a browser technology called
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API">web workers</a>
    expensive and blocking computation can run somewhere other than the
    main application thread that controls the user interface. When such work is
    done on the main thread, the browser appears frozen. Web
    workers ensure expensive blocking computation happens elsewhere. Think
    of workers as independent subprocesses in your web page.</dd>
    <dt><strong>Rich and powerful plugins</strong></dt>
    <dd>
    <p>As you'll see, PyScript has a small, efficient yet powerful core called
    <a href="https://github.com/pyscript/polyscript">PolyScript</a>.</p>
    <p>Most of the functionality of PyScript is actually implemented through
    PolyScript's plugin system.</p>

    <p>This approach means we get a clear separation of concerns: PolyScript
    can focus on being small, efficient and powerful, whereas the PyScript
    related plugins allow us to build upon the generic features provided by
    PolyScript. More importantly, because there is a plugin system, folks
    _independent of the PyScript core team_ have a way to create their own
    plugins so we get a rich ecosystem of functionality that reflects the
    unique and many needs of PyScript's users.</p>
    </dd>
</dl>

## Architecture

There are two important pieces of information you should know about the
architecture of PyScript:

1. A small, efficient and powerful kernel called
   [PolyScript](https://github.com/pyscript/polyscript) is the foundation
   upon which PyScript and plugins are built.
2. The stack inside the browser is relatively simple and easy to understand.

Let's dive into each in turn.

### PolyScript

[PolyScript](https://github.com/pyscript/polyscript) is the core of PyScript.

Its purpose is to bootstrap the platform and provide all the necessary core
capabilities. It is a small, efficient and powerful kernel. Setting aside
PyScript for a moment, to use *just PolyScript* requires a `<script>` reference
to it, along with a further `<script>` tag defining how to run some code.

```html title="Bootstrapping with PolyScript"
<!doctype html>
<html>
    <head>
        <!-- this is a way to automatically bootstrap polyscript -->
        <script type="module" src="https://cdn.jsdelivr.net/npm/polyscript"></script>
    </head>
    <body>
        <!-- run some Python code with the micropython interpreter -->
        <script type="micropython">
            from js import document
            document.body.textContent = 'polyscript'
        </script>
    </body>
</html>
```

PolyScript provides a
[small yet powerful set of capabilities](https://pyscript.github.io/polyscript/)
upon which PyScript itself is built.

These can be summarised as:

* Evaluation of code via `<script>` tags.
* The handling of events with code controlled by PolyScript.
* A clear way to use workers via the `XWorker` class and its related reference,
  `xworker`.
* Custom scripts to enrich PolyScript's capabilities (as used by PyScript).
* Certain events fired during the lifecycle of the page (see below).
* Multipe interpreters (in addition to Pyodide and MicroPython, PolyScript
  works with Lua and Ruby - although these are beyond the scope of this
  project).

Please refer to the
[PolyScript project](https://github.com/pyscript/polyscript) for more
information about its capabilities.

### The stack

The stack describes how the different building blocks of a PyScript
application relate to each other:

<img src="../assets/images/platform.png"/>

* Everything happens inside the context of the browser (represented by the
  black border). **PyScript does not run anywhere BUT THE BROWSER.** It
  means the browser tab for your PyScript app is your sandboxed computing
  environment.
* At the bottom of the stack are the Python interpreters compiled to WASM. They
  evaluate your code and interact with the browser via the FFI.
* The PyScript layer makes it easy to use and configure the Python
  interpreters. There are two parts to this:
    1. The PolyScript kernel (see above), that bootstraps everything and
       provides the core capabilities.
    2. PyScript and related plugins that sit atop PolyScript to give us the
       easy-to-use Python platform.
* Above the PyScript layer are either:
    1. Application frameworks, modules and libraries written in Python that you
       use to create useful applications.
    2. Your code (that's your responsibility).

## Lifecycle

TBD - talk to Andrea to ensure this is correct.

## Core concepts

There are only a handful of core concepts you really need to understand in
order to master PyScript.

The following sections introduce each core concept and link to the in-depth
documentation so you can explore in more detail.

### Code

First you need to tell your browser to use PyScript, then you need to tell
PyScript where to find your Python code.

To tell your browser to use PyScript, simply add a `<script>` tag, whose `src`
attribute references a CDN url for `pyscript.core`, to your HTML document's
`<head>`.

Like this **TODO: USE CORRECT CDN URL**:

```html title="Reference PyScript in your HTML"
<!doctype html>
<html>
    <head>
        <!-- Recommended meta tags -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <!-- optional PyScript CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@pyscript/core/dist/core.css">
        <!-- This script tag bootstraps PyScript -->
        <script type="module" src="https://cdn.jsdelivr.net/npm/@pyscript/core"></script>
    </head>
    <body>
        <!-- your code goes here... -->
    </body>
</html>
```

There are two ways to tell PyScript where to find your code.

* With a standard HTML `<script>` tag. **This is currently the recommended
  way**.
* Via the bespoke `<py-script>` tag. Historically, this used to be the only
  way to reference your code.

These should be inserted into the `<body>` of your HTML document.

In both cases either use the `src` attribute to reference a Python
file containing your code, or inline your code between the opening and closing
tags. **We recommend you use the `src` attribute method**, but retain the
ability to include code between tags for convenience.

Here's the `<script>` tag method using the `src` attribute to reference the URL
for a `main.py` Python file.

```html title="Using the script tag with a source file"
<script type="py" src="main.py"></script>
```

...and here's the `<py-script>` tag with inline Python code.

```html title="Using the py-script tag with inline code"
<py-script>
import sys


print(sys.version)
</py-script>
```

Both tags accept various attributes to control their behaviour. More detailed
information can be found on the [page about code](code).

### Interpreters

Python is an interpreted language, and thus needs an interpreter to work.

PyScript currently supports two versions of the Python interpreter that have
been compiled to WASM: Pyodide and MicroPython. You should select which one to
use depending on your use case and acceptable trade-offs.

Both interpreters make use of [emscripten](https://emscripten.org/), a compiler
toolchain (using LLVM), for emitting WASM assets for the browser. Emscripten
also provides APIs so operating-system level features such as a sandboxed file
system (**not** the user's local machine's filesystem), IO (`stdin`, `stdout`,
`stderr` etc,) and networking are available within the context of a browser.

#### Pyodide

[Pyodide](https://pyodide.org/) is a version of the standard
[CPython](https://python.org/) interpreter, patched to compile to WASM and
work in the browser.

It is a mature and stable build of the CPython interpreter and includes many
useful features:

* A robust [Python](https://pyodide.org/en/stable/usage/api/python-api.html)
  ⟺ [JavaScript](https://pyodide.org/en/stable/usage/api/js-api.html) foreign
  function interface (FFI). This bridges the gap between the browser and Python
  worlds.
* The installation of pure Python packages from [PyPI](https://pypi.org/) via
  the [micropip](https://micropip.pyodide.org/en/stable/index.html) package
  installer. Some packages with C extensions have versions compiled for WASM
  and these can also be installed with `micropip`. There are plans afoot to
  make WASM a target in PyPI so packages with C extenions can be automatically
  compiled to WASM.
* An active, friendly and technically outstanding team of volunteer
  contributors (some of whom have been supported by the PyScript project).
* Extensive official
  [documentation](https://micropip.pyodide.org/en/stable/index.html), and many
  tutorials found online.
* Builds of Pyodide that include popular packages for data science like
  [Numpy](https://numpy.org/), [Scipy](https://scipy.org/) and
  [Pandas](https://pandas.pydata.org/).

#### MicroPython

[MicroPython](https://micropython.org/) is a lean and efficient implementation
of the Python 3 programming language that includes a small subset of the Python
standard library and is optimised to run on microcontrollers and in constrained
environments (like the browser). 

Everything needed to view a web page in a browser needs to be delivered
over the network. The smaller the asset to be delivered can be, the better.
MicroPython, when compressed for delivery to the browser, is only around
170k in size - smaller than most images you find on most websites.

This makes MicroPython particularly suited to browsers running in a more
constrained environment such as on a mobile or tablet based device. Browsing
with these devices usually uses (slower) mobile internet connections.
Furthermore, because MicroPython is lean and efficient it still performs
exceptionally well on these relatively underpowered devices.

Thanks to collaboration between the MicroPython and PyScript projects, there is
a foreign function interface for MicroPython. The MicroPython FFI deliberately
copies the API of the FFI originally written for Pyodide - meaning it is
relatively easy to migrate between the two supported interpreters.

Further details and more in-depth discussion of the interpreters supported by 
PyScript can be found on [the interpreters page](interpreters).

### The DOM

The DOM
([document object model](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model))
refers to a tree like data structure that represents the web page in the
browser. PyScript needs to be able to interact with the DOM in order to change
the user interface and react to things happening in the browser.

There are currently two ways to interact with the DOM:

1. Through the FFI and by directly interacting with the objects found in the
   `globalThis` object.
2. Through the `pydom` module that comes as standard with PyScript.

The first option gives you access to all the [standard web capabilities and
features](https://developer.mozilla.org/en-US/docs/Web), such as the browser's
built-in [web APIs](https://developer.mozilla.org/en-US/docs/Web/API), and the
`document` object at the root of the [DOM tree](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Using_the_Document_Object_Model#what_is_a_dom_tree).

The second is a Python module called `pydom` that wraps many (although not all)
the features available via the FFI in a more idiomatically Pythonic library...
**TODO: Fabio to finish this bit...**

Explore the PyScript story of working with the DOM in [the DOM page](dom).

### Configuration

Sometimes we need to tell PyScript about how we want our Python environment to
be configured. To this end there are three core options:

* `fetch` files from URLs onto the filesystem emulated by the browser for your
  web page.
* A list of Python `packages` to be installed from [PyPI](https://pypi.org/)
  onto the filesystem by Pyodide's 
  [micropip](https://micropip.pyodide.org/en/stable/index.html) package
  installer.
* A list of `plugins` to be enabled by PyScript to add extra functionality to
  the platform.

!!! warning

    Because `micropip` is a Pyodide-only feature, and MicroPython doesn't
    support code packaged on PyPI, **the `packages` option is only available
    if you use Pyodide as your interpreter**.

#### TOML or JSON

Configuration can be expressed in two formats:

* [TOML](https://toml.io/en/) is the configuration file format most often used
  by folks in the Python community.
* [JSON](https://www.json.org/json-en.html) is a data format most often used
  by folks in the web community.

Since PyScript is the marriage of Python and the web, we support both.

However, because JSON is built into all browsers by default and TOML requires
an additional download of a specialist parser before PyScript can work, the
use of JSON is more efficient from a performance point of view.

The following two configurations are equivalent, and simply tell PyScript to
ensure the packages `arrr` and `numberwang` are installed from PyPI

```TOML title="Configuration via TOML"
packages = ["arrr", "numberwang" ]
```

```JSON title="Configuration via JSON"
{
    "packages": ["arrr", "numberwang"]
}
```

#### File based or inline configuration

The recommended way to write configurations is via a separate file and
referencing it from the tag used to specify the Python code:

```HTML title="Reference a configuration file"
<script type="py" src="main.py" config="pyscript.toml"></script>
```

For historical and convenience reasons we still support the inline
specification of configuration information via the `<py-config>` tag used
in your HTML document:

```HTML title="Inline configuration via the &lt;py-config&gt; tag"
<py-config>
{
    "packages": ["arrr", "numberwang" ]
}
</py-config>
```

Fully worked out examples of how to configure each of the `fetch`, `packages`
and `plugins` options, along with details of how to define arbitrary
additional configuration options (that plugins may require) can be found on
[the configuration page](configuration).

### Workers

### Plugins

### FFI

## Examples

### Lots of DOM manipulation

### Data science-y

### Graphical

### Blocking with workers

### Calling an API
