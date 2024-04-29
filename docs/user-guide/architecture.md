# Architecture, Lifecycle &amp; Interpreters

## Core concepts 

PyScript's architecture has three core concepts:

1. A small, efficient and powerful kernel called
   [PolyScript](https://github.com/pyscript/polyscript) is the foundation
   upon which PyScript and plugins are built.
2. A library called [coincident](https://github.com/WebReflection/coincident#readme)
   that simplifies and coordinates interactions with web workers.
3. The PyScript [stack](https://en.wikipedia.org/wiki/Solution_stack) inside
   the browser is simple and clearly defined.

### PolyScript

[PolyScript](https://github.com/pyscript/polyscript) is the core of PyScript.

!!! danger 

    Unless you are an advanced user, you only need to know that PolyScript
    exists, and it can be safely ignored.

PolyScript's purpose is to bootstrap the platform and provide all the necessary
core capabilities. Setting aside PyScript for a moment, to use
*just PolyScript* requires a `<script>` reference to it, along with a further
`<script>` tag defining how to run your code.

```html title="Bootstrapping with just PolyScript"
<!doctype html>
<html>
    <head>
        <!-- this is a way to automatically bootstrap polyscript -->
        <script type="module" src="https://cdn.jsdelivr.net/npm/polyscript"></script>
    </head>
    <body>
        <!--
            Run some Python code with the MicroPython interpreter, but without
            the extra benefits provided by PyScript.
        -->
        <script type="micropython">
            from js import document
            document.body.textContent = 'polyscript'
        </script>
    </body>
</html>
```

!!! warning

    **PolyScript is not PyScript.**

    PyScript enhances the available Python interpreters with convenient
    features, helper functions and easy-to-use yet powerful capabilities.

    These enhancements are missing from PolyScript.

PolyScript's capabilities, upon which PyScript is built, can be summarised as:

* Evaluation of code via [`<script>` tags](https://pyscript.github.io/polyscript/#how-scripts-work).
* Handling
  [browser events](https://pyscript.github.io/polyscript/#how-events-work)
  via code evaluated with an interpreter supported by PolyScript.
* A [clear way to use workers](https://pyscript.github.io/polyscript/#xworker)
  via the `XWorker` class and its related reference, `xworker`.
* [Custom scripts](https://pyscript.github.io/polyscript/#custom-scripts) to
  enrich PolyScript's capabilities.
* A [ready event](https://pyscript.github.io/polyscript/#ready-event)
  dispatched when an interpreter is ready and about to run code, and a
  [done event](https://pyscript.github.io/polyscript/#done-event) when an
  interpreter has finished evaluating code.
* [Hooks](https://pyscript.github.io/polyscript/#hooks), called at clearly
  defined moments in the page lifecycle, provide a means of calling user
  defined functions to modify and enhance PolyScript's default behaviour.
* [Multiple interpreters](https://pyscript.github.io/polyscript/#interpreter-features)
  (in addition to Pyodide and MicroPython, PolyScript works with Lua and Ruby -
  although these are beyond the scope of this project).

PolyScript may become important if you encounter problems with PyScript. You
should investigate PolyScript if any of the following is true about your
problem:

* The interpreter fails to load.
* There are errors about the interpreter starting.
* HTML events (e.g. `py-*` or `mpy-*`) are not triggered.
* An explicit feature of PolyScript is not reflected in PyScript.

We encourage you to engage and ask questions about PolyScript on our
[discord server](https://discord.gg/HxvBtukrg2). But in summary, as a user of
PyScript you should probably never encounter PolyScript. However, please be
aware that specific features of bug fixes my happen in the PolyScript layer in
order to then land in PyScript.

### Coincident

!!! danger 

    Unless you are an advanced user, you only need to know that coincident
    exists, and it can be safely ignored. As with PolyScript, we include these
    details only for those interested in the more fundamental aspects of
    PyScript.

PolyScript uses the
[coincident](https://github.com/WebReflection/coincident#readme) library to
seamlessly interact with web workers and coordinate interactions between the
browser's main thread and such workers.

Any `SharedArrayBuffer` issues are the responsibility of coincident and, to
some extent, anything related to memory leaks.

In a nutshell, this project is likely responsible for the following modes of
failure:

* Failing to invoke something from a worker that refers to the main thread.
* A reproducible and cross platform (browser based) memory leak.
* Invoking a function with a specific argument from a worker that doesn't
  produce the expected result.

We hope all these scenarios are unlikely to happen within a *PyScript* project.
They are all battle tested and covered with general purpose cross-environment
testing before landing in *PyScript*. But, if you feel something is odd,
leaking, or badly broken, please feel free to file an issue in
[the coincident project](https://github.com/WebReflection/coincident/issues).
As usual, there is never a silly question, so long as you provide a minimal
reproducible example in your bug reports or query.

### The stack

The stack describes how the different building blocks _inside_ a PyScript
application relate to each other:

<img src="../../assets/images/platform.png"/>

* Everything happens inside the context of the browser (represented by the
  black border). **The browser tab for your PyScript app is your
  sandboxed computing environment**.

!!! failure

    PyScript is simply Python running in the browser. **Please remember**:

    * PyScript isn't running on a server hosted in the cloud.
    * PyScript doesn't use the version of Python running natively on the user's
      operating system.
    * **PyScript only runs IN THE BROWSER (and nowhere else).**

* At the bottom of the stack are the Python interpreters compiled to WASM. They
  evaluate your code and interact with the browser via the [FFI](dom.md/#ffi).
* The PyScript layer makes it easy to use and configure the Python
  interpreters. There are two parts to this:
    1. The PolyScript kernel (see above), that bootstraps everything and
       provides the core capabilities.
    2. PyScript and related plugins that sit atop PolyScript to give us an
       easy-to-use Python platform _in the browser_.
* Above the PyScript layer are either:
    1. Application frameworks, modules and libraries written in Python that you
       use to create useful applications.
    2. Your code (that's your responsibility).

## Lifecycle

If the architecture explains how components relate to each other, the lifecycle
explains how things unfold. It's important to understand both: it will
help you think about your own code and how it sits within PyScript.

Here's how PyScript unfolds through time:

* The browser is directed to a URL. The response is HTML.
* When parsing the HTML response the browser encounters the `<script>`
  tag that references PyScript. PyScript is loaded and evaluated as a
  [JavaScript module](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules),
  meaning it doesn't hold up the loading of the page and is only evaluated when
  the HTML is fully parsed.
* The PyScript module does broadly six things:
    1. Discover Python code referenced in the page.
    2. Evaluate any [configuration](configuration.md) on the page (either via
       single `<py-config>` or `<mpy-config>` tags **or** the `config`
       attribute of a `<script>`, `<py-script>` or `<mpy-script>` tag).
    3. Given the detected configuration, download the required interpreter.
    4. Setup the interpreter's environment. This includes any
       [plugins](configuration.md/#plugins), [packages](configuration.md/#packages), [files](configuration.md/#files) or [JavaScript modules](configuration.md/#javascript-modules) 
       that need to be loaded.
    5. Make available various
       [builtin helper objects and functions](builtins.md) to the
       interpreter's environment (accessed via the `pyscript` module).
    6. Only then use the interpreter in the correctly configured environment to
       evaluate the detected Python code.
* When an interpreter is ready the `py:ready` or `mpy:ready` events are
  dispatched, depending which interpreter you've specified (Pyodide or
  MicroPython respectively).
* Finally, a `py:done` event is dispatched after every single script
  referenced from the page has finished.

In addition, various "hooks" are called at different moments in the lifecycle
of PyScript. These can be used by plugin authors to modify or enhance the
behaviour of PyScript. The hooks, and how to use them, are explored further in
[the section on plugins](plugins.md).

!!! warning

    A web page's workers have completely separate environments to the main
    thread.

    It means configuration in the main thread can be different to that for
    an interpreter running on a worker. In fact, you can use different
    interpreters and configuration in each context (for instance, MicroPython
    on the main thread, and Pyodide on a worker).

    Think of workers as completely separate sub-processes inside your browser
    tab.

## Interpreters

Python is an interpreted language, and thus needs an interpreter to work.

PyScript currently supports two versions of the Python interpreter that have
been compiled to WASM: Pyodide and MicroPython. You should select which one to
use depending on your use case and acceptable trade-offs.

!!! info

    In future, and subject to progress, we hope to make available a third
    Pythonic option: [SPy](https://github.com/spylang/spy), a staticially typed
    version of Python compiled directly to WASM.

Both interpreters make use of [emscripten](https://emscripten.org/), a compiler
toolchain (using [LLVM](https://llvm.org/)), for emitting WASM assets for the
browser. Emscripten also provides APIs so operating-system level features such
as a sandboxed [file system](https://emscripten.org/docs/api_reference/Filesystem-API.html)
(**not** the user's local machine's filesystem), [IO](https://emscripten.org/docs/api_reference/console.h.html)
(`stdin`, `stdout`, `stderr` etc,) and [networking](https://emscripten.org/docs/api_reference/fetch.html) are
available within the context of a browser.

Both Pyodide and MicroPython implement the same robust
[Python](https://pyodide.org/en/stable/usage/api/python-api.html)
⟺ [JavaScript](https://pyodide.org/en/stable/usage/api/js-api.html)
[foreign function interface](dom.md/#ffi) (FFI). This
bridges the gap between the browser and Python worlds.

### Pyodide

<a href="https://pyodide.org/"><img src="../../assets/images/pyodide.png"/></a>

[Pyodide](https://pyodide.org/) is a version of the standard
[CPython](https://python.org/) interpreter, patched to compile to WASM and
work in the browser.

It includes many useful features:

* The installation of pure Python packages from [PyPI](https://pypi.org/) via
  the [micropip](https://micropip.pyodide.org/en/stable/index.html) package
  installer.
* An active, friendly and technically outstanding team of volunteer
  contributors (some of whom have been supported by the PyScript project).
* Extensive official
  [documentation](https://micropip.pyodide.org/en/stable/index.html), and many
  tutorials found online.
* Builds of Pyodide that include popular packages for data science like
  [Numpy](https://numpy.org/), [Scipy](https://scipy.org/) and
  [Pandas](https://pandas.pydata.org/).

!!! warning 

    You may encounter an error message from `micropip` that explains it can't
    find a "pure Python wheel" for a package. Pyodide's documentation
    [explains what to do in this situation](https://pyodide.org/en/stable/usage/faq.html#why-can-t-micropip-find-a-pure-python-wheel-for-a-package).

    Briefly, some
    [packages with C extensions](https://docs.python.org/3/extending/building.html)
    have versions compiled for WASM and these can be installed with `micropip`.
    Packages containing C extensions that _are not compiled for WASM_ cause the
    "pure Python wheel" error.

    There are plans afoot to make WASM a target in PyPI so packages with C
    extensions are automatically compiled to WASM.

### MicroPython

<a href="https://micropython.org/"><img src="../../assets/images/micropython.png"/></a>

[MicroPython](https://micropython.org/) is a lean and efficient implementation
of the Python 3 programming language that includes a small subset of the Python
standard library and is optimised to run on microcontrollers and in constrained
environments (like the browser). 

Everything needed to view a web page in a browser needs to be delivered
over the network. The smaller the asset to be delivered can be, the better.
MicroPython, when compressed for delivery to the browser, is only around
170k in size - smaller than many images found on the web.

This makes MicroPython particularly suited to browsers running in a more
constrained environment such as on a mobile or tablet based device. Browsing
with these devices often uses (slower) mobile internet connections.
Furthermore, because MicroPython is lean and efficient it still performs
exceptionally well on these relatively underpowered devices.

Thanks to collaboration between the MicroPython, Pyodide and PyScript projects,
there is a foreign function interface for MicroPython. The MicroPython FFI
deliberately copies the API of the FFI originally written for Pyodide - meaning
it is relatively easy to migrate between the two supported interpreters via the
`pyscript.ffi` namespace.
