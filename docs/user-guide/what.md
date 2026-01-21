# What is PyScript?

[PyScript](https://pyscript.net) is an
[open source](../license.md) platform for running
[Python](https://python.org) in modern
[web browsers](https://en.wikipedia.org/wiki/Web_browser).

PyScript brings together two of the most vibrant technical ecosystems
on the planet: the web and Python. It lets you build rich, interactive
web applications using Python, without the need for a backend server or
entanglements with browser-based JavaScript (although PyScript also works
well in these two contexts).

Write your application logic in Python, use Python libraries for data
processing or visualisation, and deploy your work with just a URL. Your
users run everything locally in their browser, making PyScript
applications fast, secure, and easy to share.

## How it works

PyScript is built on [WebAssembly](https://webassembly.org/)
(abbreviated to WASM) - an
[instruction set](https://en.wikipedia.org/wiki/Instruction_set_architecture)
for a [virtual machine](https://en.wikipedia.org/wiki/Virtual_machine)
with an open specification and near-native performance. Modern browsers
all support WebAssembly, making it a universal platform for running code
beyond JavaScript.

PyScript takes versions of the Python interpreter compiled to
WebAssembly and makes them easy to use inside the browser. You write
Python code, and PyScript handles all the complexity of loading the
interpreter, managing the environment, and bridging between Python and
the browser's JavaScript APIs.

### Two Python interpreters

PyScript supports two Python interpreters, letting you choose the right
tool for your application:

<a href="https://pyodide.org/"><img src="../../assets/images/pyodide.png" alt="Pyodide logo"/></a>

**[Pyodide](https://pyodide.org/)** is the full CPython interpreter
compiled to WebAssembly. It's the standard Python you already know: the same
interpreter that runs on your laptop, with the same standard library and the same
behaviour. Because it's genuine CPython, Pyodide gives you access to
Python's vast ecosystem of packages from [PyPI](https://pypi.org/). Want
to use NumPy, Pandas, Matplotlib, Scikit-learn, or thousands of other
libraries? Pyodide makes it possible.

!!! info

    Want to check if a third party package works with PyScript/Pyodide?

    [Use this handy site!](https://packages.pyscript.net/)

<a href="https://micropython.org/"><img src="../../assets/images/micropython.png" alt="MicroPython logo"/></a>

**[MicroPython](https://micropython.org/)** is a lean, efficient
reimplementation of Python 3 that includes a comprehensive subset of the
standard library. At just 170KB, MicroPython loads almost instantly,
making it ideal for mobile devices, slow connections, or any time you
want your app to start quickly. Despite its small size, MicroPython is
surprisingly capable, exposing Python's full expressiveness to the
browser.

Both interpreters implement almost identical foreign function interfaces (FFI)
to bridge Python and JavaScript, so your code works consistently
regardless of which interpreter you choose (and PyScript provides abstractions
around the differences between their FFIs).

!!! tip

    **When to use which interpreter:**

    Choose **Pyodide** when you need access to Python's extensive
    computing stack (NumPy, Pandas, Matplotlib, etc.), when you're
    working with complex Python packages, or when you need full CPython
    compatibility.

    Choose **MicroPython** for mobile applications, when fast startup
    time matters, or when you're building lightweight applications that
    don't need heavy libraries.

### The foreign function interface

The FFI (foreign function interface) is how Python and JavaScript
communicate in PyScript. It automatically translates between Python and
JavaScript objects, letting you use browser APIs directly from your
Python code.

This bridge is bidirectional: Python can call JavaScript functions and
access JavaScript objects, while JavaScript can call Python functions
and access Python objects. The FFI handles all the type conversions
automatically, so you can focus on writing your application logic.

Want to manipulate the DOM? Access the browser's `document` object.
Need to use a JavaScript library? Import it and call its functions from
Python. The FFI makes it seamless.

Put simply, PyScript helps Python and JavaScript to be friends that
complement and amplify each others strengths.

Learn more about the FFI in the high level [DOM interaction guide](dom.md#the-ffi-javascript-interoperability)
or dive deep into the [FFI's technical details](ffi.md).

## Key capabilities

PyScript provides a rich set of features that make building web
applications with Python both powerful and enjoyable:

### Full web platform access

PyScript gives you complete access to the [DOM](dom.md) and all the
[web APIs](https://developer.mozilla.org/en-US/docs/Web/API)
implemented by your browser. Through the FFI, Python works seamlessly
with everything the browser offers, including any third-party JavaScript
libraries included in your page.

The `pyscript.web` module provides a Pythonic interface to the DOM,
making it feel natural to work with web page elements from Python. Find
elements with CSS selectors, manipulate content and attributes, handle
events - all with idiomatic Python code.

### Python's vast ecosystem

Because Pyodide is genuine CPython compiled to WebAssembly, you have
access to Python's deep and diverse ecosystem of libraries, frameworks,
and modules. Whether you're doing data science, building visualisations,
processing text, or working with APIs, there's probably a Python library
to help.

Got a favourite library in Python? Now you can use it in the browser and
share your work with just a URL. No server required, no complex
deployment - just Python running where your users are.

Need to check if a package is supported by PyScript? Use our
[PyScript Packages](https://packages.pyscript.net/) website
to check and/or report the status of any third party packages.

### AI and data science built in

Python is famous for its extraordinary usefulness in artificial
intelligence and data science. The Pyodide interpreter comes with many
of the libraries needed for this sort of work already included: NumPy,
Pandas, Matplotlib, Scikit-learn, and more.

Build interactive data visualisations, create machine learning
demonstrations, or develop educational tools that let users experiment
with algorithms - all running locally in the browser with no backend
required!

### Mobile-friendly MicroPython

Thanks to MicroPython's tiny size and fast startup, PyScript
provides a compelling story for Python on mobile devices. Your
application loads quickly on first visit and almost instantly on
subsequent visits (thanks to browser caching).

This makes PyScript practical for mobile web applications, progressive
web apps, or any scenario where fast initial load matters.

### Background processing with workers

Expensive computation can block the main thread, making your application
appear frozen. PyScript supports
[web workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API),
letting you run Python code in background threads that don't interfere
with the user interface.

Think of workers as independent subprocesses in your web page. They're
perfect for data processing, simulations, or any CPU-intensive work.
Learn more in the [workers guide](workers.md).

### Device capabilities

PyScript gives your Python code access to modern browser capabilities:
capture photos and video with the [camera](media.md), record
[media](media.md#capturing-media-streams), read and write [files](filesystem.md), store
data [locally](../api/storage.md), and integrate with all the other available
web APIs.

Build applications that feel native, with access to device hardware and
local storage, all from Python.

### Extensible plugin system

PyScript has a small, efficient core called
[PolyScript](https://github.com/pyscript/polyscript). Most of
PyScript's functionality is actually implemented through PolyScript's
[plugin system](plugins.md).

This architecture ensures a clear separation of concerns: PolyScript
focuses on being small, efficient, and powerful, whilst the PyScript
plugins build Pythonically upon these solid foundations.

The plugin system also means developers independent of the PyScript core
team can create and contribute plugins whose functionality reflects the
unique and diverse needs of PyScript's users.

## Our aim: digital empowerment

At the core of PyScript is a philosophy of digital empowerment.

The web is the world's most ubiquitous computing platform, mature and
familiar to billions of people. Python is one of the
[world's most popular programming languages](https://spectrum.ieee.org/top-programming-languages-2025):
it's easy to teach and learn, used across countless domains (data
science, education, games, embedded systems, artificial intelligence,
finance, physics, film production - to name but a few), and the Python
ecosystem contains a vast number of popular and powerful libraries.

PyScript brings together the ubiquity, familiarity, and accessibility of
the web with the power, depth, and expressiveness of Python.

This means PyScript isn't just for programming experts but, as we like
to say, **for the 99% of the rest of the planet who use computers**.

By making Python accessible in the browser, PyScript lowers barriers to
creating and sharing software. You don't need to understand server
deployment, database management, or complex build processes. You don't
need to learn a new language or framework. You just need Python and a
web browser.

This democratisation of web development means more people can create
tools to solve their own problems, share their knowledge with others,
and contribute to the digital world we all inhabit.

## What you can build

PyScript opens up new possibilities for Python developers and new
capabilities for web applications:

**Educational tools and interactive tutorials** - Create lessons where
students can experiment with code directly in their browser, see
visualisations update in real-time, and learn by doing.

**Data analysis dashboards** - Build interactive visualisations of your
data using Pandas and Matplotlib, then share them with colleagues who
can explore the data themselves without installing anything.

**Scientific simulations** - Develop models and simulations that run
entirely in the browser, letting others experiment with parameters and
see results instantly.

**Creative coding projects** - Make generative art, music
visualisations, or interactive games using Python libraries you already
know.

**Rapid prototypes** - Test ideas quickly without setting up backend
infrastructure. Share prototypes with a simple URL.

**Browser-based tools** - Create utilities that process files, transform
data, or automate tasks - all running locally for privacy and speed.

The only limit is your imagination (and perhaps your users' patience
whilst the interpreter loads, but that's getting faster all the time).

## Next steps

Ready to start building with PyScript?

Explore [interacting with the web page](dom.md) to learn how a
PyScript application interacts with the browser, or jump to 
[Configuration](configuration.md) to understand how to set up your Python
environment.

Want to see PyScript in action first? Check out the
[example applications](../example-apps/overview.md) to see what's
possible and learn from working code.