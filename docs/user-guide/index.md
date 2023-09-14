# Introduction (start here)

!!! note

    This guide provides detailed technical guidance for developers who want
    in depth explanation of the PyScript platform.

    As a result, while we endeavour to write clearly, some of the content in
    this user guide will not be suitable for beginners. We assume folks who
    will get the most from this guide will already have some Python or web
    development experience.

    We welcome feedback to help us improve.

This guide is in three parts:

1. The brief overview, context setting and sign-posting contained within this
   page.
2. The other pages of the guide, referenced from this page, that explore the
   different aspects of PyScript in substantial technical detail.
3. The example projects, listed at the end of this page, that demonstrate the
   various features of PyScript working together in real-world applications.

We suggest you _read this page in full_: it will ensure you have a complete and
comprehensive overview of the PyScript platform along with suggestions for
where next to explore.

When you require depth and technical detail you should consult the other pages
of this guide that are referenced from this page. They provide clear and
precise details along with example code fragments and descriptions of the APIs
available via PyScript.

Finally, the examples listed at the end of this page, are all freely available
and copiously commented on [pyscript.com](pyscript.com). You should consult
these for practical "real world" use of the various features of the PyScript
platform. Many of these examples come from a diversity of members and
contributors to our wonderful community. If you believe you have a project that
would make a good example, please don't hesitate to get in touch.

## What is PyScript?

PyScript is a platform for Python in the browser.

PyScript's aim is to bring together two of the most vibrant technical
ecosystems on the planet. If the web and Python had a baby, you get PyScript.

PyScript works because modern browsers support
[web assembly](https://webassembly.org/) (abbreviated to WASM) - a virtual
machine with an open specification and near native performance. PyScript takes
versions of the Python interpreter compiled to WASM, and makes them easy to use
from within your browser.

That's it!

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
    access to the complete
    <a href="https://developer.mozilla.org/en-US/docs/Web/API">web
    APIs implemented by your browser</a>.</p>

    <p>The FFI makes it easy for Python to work with all the capabilities in
    scope in your browser, including third party JavaScript libraries that may
    be included with the <code>script</code> tag.</p>

    <p>The FFI even allows JavaScript to access the power of PyScript.</p></dd>
    <dt><strong>All of Python</strong></dt>
    <dd>
    <p>PyScript brings you two Python interpreters:</p>
    <ol>
        <li><a href="https://pyodide.org/">Pyodide</a> - the original standard CPython
        interpreter you know and love, but compiled to web assembly.</li>
        <li><a href="https://micropython.org/">MicroPython</a> - a lean and efficient
        reimplementation of Python3 that includes a comprehensive subset of the
        standard library, compiled to web assembly.</li>
    </ol>
    <p>Because it is just regular CPython, Pyodide brings the deep and diverse
    ecosystem of libraries, frameworks and modules at your disposal. If you
    find yourself encountering some sort of computing problem, there's probably
    a Python library to help you with it. If you're used to using a favourite
    library in Python, now you can use it in your browser and share it with
    the ease of a URL.</p>
    <p>MicroPython, because of its small size (170k) and speed, is especially
    suited to running on more constrained browsers, such as those on mobile
    or tablet devices.</p>
    <p>Both Python interpreters supported by PyScript implement the same
    FFI to bridge the gap between the worlds of Python and the browser.</p>
    </dd>
    <dt><strong>Data science built in</strong></dt>
    <dd>Python is famous for its extraordinary usefulness in data science
    and artificial intelligence. The Pyodide interpreter comes with many of the
    libraries you need for this sort of work, already baked in.</dd>
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
    expensive and blocking computation can be run somewhere other than the
    main application thread that controls the user interface. Were such work to
    be done on the main thread your browser would appear frozen, but web
    workers ensure expensive and blocking computation happens elsewhere. Think
    of workers as independent subprocesses in your web page.</dd>
    <dt><strong>Rich and powerful plugins</strong></dt>
    <dd>
    <p>As you'll see, PyScript has a small, efficient yet powerful core called
    <a href="https://github.com/pyscript/polyscript">PolyScript</a>.</p>
    <p>Most of the functionality of PyScript is actually implemented through
    PolyScript's plugin system.</p>

    <p>The advantage of this approach is that we get
    a clear separation of concerns: PolyScript can focus on being small,
    efficient and powerful, whereas the PyScript related plugins allow us to
    customise the generic features provided by PolyScript. More importantly,
    because there is a plugin system, folks independent of the PyScript core
    team can create their own plugins so we get a rich ecosystem of
    functionality that reflects the needs of PyScript's users.</p>
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

[PolyScript](https://pyscript.github.io/polyscript/) is the core of PyScript.

Its purpose is to bootstrap everything and provide all the core capabilities
we need. It does so as a small, efficient and powerful kernel. Setting aside
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

* Evaluating code via `<script>` tags.
* Handling events with code controlled by PolyScript.
* Use of workers via the `XWorker` class and its reference `xworker`.
* Custom scripts to enrich PolyScript's capabilities (as PyScript does).
* Certain events fired during the lifecycle of the page (see below).
* Multipe interpreters (in addition to Pyodide and MicroPython we have had
  PolyScript work with Lua and Ruby - although these are beyond the scope of
  this project).

Please refer to the PolyScript project for more information about its
capabilities.

### The stack

The following diagram sums up everything you need to know:

<img src="/assets/images/platform.png"/>

* Everything happens inside the context of the browser (represented by the
  black border). **PyScript code does not run anywhere BUT THE BROWSER.** It
  means the browser tab for your PyScript app is your sandbox.
* At the bottom of the stack are the Python interpreters compiled to WASM. They
  evaluate your code and interact with the browser via the FFI.
* The PyScript layer makes it easy to use and configure the Python
  interpreters. There are two parts to this:
    1. The PolyScript kernel (see above), that bootstraps everything and
       provides the core capabilities.
    2. The PyScript capabilities and related plugins that sit atop PolyScript
       and give us the easy-to-use platform.
* Above the PyScript layer are either:
    1. Application frameworks, modules and libraries written in Pyton that you
       use to create useful applications.
    2. Your code (that's your responsibility).

## Lifecycle

TBD - talk to Andrea to ensure this is correct.

## Core concepts

### Interpreters

### The DOM

### Configuration

### Workers

### Plugins

### FFI

## Examples

### Lots of DOM manipulation

### Data science-y

### Graphical

### Blocking with workers

### Calling an API
