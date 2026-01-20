# Architecture

Understanding how PyScript works helps you build better applications and
debug problems when they arise. This guide explains PyScript's
architecture, lifecycle, and the interpreters that power your Python
code in the browser.

You don't need to master these details to use PyScript effectively, but
knowing the fundamentals helps you understand what's happening behind
the scenes.

## The foundation: PolyScript

PyScript is built on [PolyScript](https://github.com/pyscript/polyscript),
a small kernel that bootstraps interpreters and provides core
capabilities. PolyScript handles script evaluation, event processing,
and worker management - the low-level machinery that makes everything
work.

Most PyScript users never interact with PolyScript directly. PyScript
wraps PolyScript with convenient features, helper functions, and
powerful capabilities that make Python in the browser accessible and
practical. PolyScript provides the foundation. PyScript provides the
usable platform.

You might encounter PolyScript if you debug interpreter loading issues,
investigate event handling problems, or explore advanced customisation.
But for typical application development, you can safely ignore
PolyScript's existence.

## Worker coordination: Coincident

PyScript uses [Coincident](https://github.com/WebReflection/coincident)
to coordinate interactions between the main thread and web workers. This
library handles the complexity of cross-thread communication,
SharedArrayBuffer management, and memory coordination.

Like PolyScript, Coincident operates behind the scenes. You use the
clean `pyscript.workers` API without worrying about the underlying
coordination mechanisms. Coincident makes worker communication feel
simple and natural, hiding the difficult parts.

If you encounter worker-related issues - functions not being callable
across threads, arguments not being passed correctly, or memory leaks -
these might originate in Coincident. Such problems are rare, but knowing
this layer exists helps when debugging unusual worker behaviour.

## The PyScript stack

Understanding how components layer together helps you think about where
your code fits:

<img src="../../assets/images/platform.png"/>

At the foundation are Python interpreters compiled to WebAssembly -
either Pyodide or MicroPython. These evaluate your code and interact
with the browser through the Foreign Function Interface.

The PyScript layer sits above the interpreters, consisting of two parts.
PolyScript provides the kernel that bootstraps everything and handles
core capabilities. PyScript and its plugins sit atop PolyScript,
providing the easy-to-use Python platform you actually interact with.

Your application code runs at the top of the stack, either directly or
through frameworks and libraries you've chosen. Everything happens
inside your browser tab - a sandboxed computing environment isolated
from both the server and the user's operating system.

!!! info

    PyScript runs entirely in the browser. It doesn't execute on a
    server in the cloud. It doesn't use Python installed on the user's
    operating system. Everything happens in the browser tab, and nowhere
    else.

## Application lifecycle

Understanding the lifecycle helps you think about timing and order of
operations in your applications. Here's how PyScript unfolds:

The browser loads your HTML page. When it encounters the PyScript
script tag, PyScript loads as a JavaScript module. Module loading is
non-blocking, so the page continues loading whilst PyScript
initialises.

Once loaded, PyScript discovers Python code on the page, evaluates any
configuration, downloads the required interpreter, and sets up the
interpreter's environment. This setup includes loading plugins,
packages, files, and JavaScript modules specified in your configuration.

PyScript then makes built-in helper objects and functions available
through the `pyscript` module. Only after this completes does the
interpreter evaluate your Python code.

When the interpreter is ready, PyScript dispatches a `py:ready` event
for Pyodide or `mpy:ready` for MicroPython. After all scripts finish
evaluating, a `py:done` event signals completion.

This lifecycle applies to both the main thread and workers. Workers have
completely separate environments - different configuration, different
interpreters, different package sets. Think of each worker as a
separate subprocess inside your browser tab.

## Choosing interpreters

PyScript supports two Python interpreters compiled to WebAssembly. Each
offers different trade-offs, and you should choose based on your
application's needs.

### Pyodide

[Pyodide](https://pyodide.org/) is CPython compiled to WebAssembly. It
provides full Python compatibility with access to the standard library
and many third-party packages.

<a href="https://pyodide.org/"><img src="../../assets/images/pyodide.png"/></a>

Pyodide's strengths include package installation from PyPI using
micropip, extensive documentation and community support, and pre-built
versions of popular data science packages like numpy, scipy, and pandas.
The active community produces excellent documentation and tutorials.

Use Pyodide when you need full Python compatibility, access to packages
from PyPI, or weighty computing libraries. The trade-off is larger
file size and slower initial load compared to MicroPython.

!!! warning

    Some packages with C extensions work in Pyodide, others don't.
    Pyodide can install packages with C extensions that have been
    compiled to WebAssembly. Packages not compiled for WebAssembly
    cause "pure Python wheel" errors. See
    [Pyodide's FAQ](https://pyodide.org/en/stable/usage/faq.html#why-can-t-micropip-find-a-pure-python-wheel-for-a-package)
    for details.

    If you want to check if a package works with PyScript, check
    out [this handy website](https://pyscript.github.io/pyscript-packages/)
    for more information.

### MicroPython

[MicroPython](https://micropython.org/) is a lean Python implementation
designed for constrained environments. It includes a subset of the
standard library and focuses on efficiency.

<a href="https://micropython.org/"><img src="../../assets/images/micropython.png"/></a>

MicroPython's key advantage is size. Compressed for delivery, it's only
about 170KB - smaller than many images on the web. This makes it ideal
for mobile devices with slower connections and less powerful hardware.

Use MicroPython when you need fast startup, small file size, or want to
minimise network transfer. It works especially well for user interface
code, simple scripting, or applications on mobile devices. The trade-off
is no package installation - you only get the standard library subset
MicroPython provides, or code you directly copy into the PyScript
environment via [`files` based configuration](./configuration.md#files).

### Cross-interpreter compatibility

Both interpreters implement almost the same Foreign Function Interface for
Python-JavaScript interaction. PyScript's unified [`pyscript.ffi`](../api/ffi.md)
namespace works consistently across both interpreters, making it
relatively straightforward to migrate between them.

However, code using packages from PyPI only works in Pyodide. Code
relying on full standard library features may behave differently or fail
in MicroPython. Test thoroughly if you switch interpreters.

## Understanding WebAssembly compilation

Both interpreters use [Emscripten](https://emscripten.org/), a compiler
toolchain built on [LLVM](https://llvm.org/), to compile C to WebAssembly. Emscripten
provides more than just compilation - it supplies APIs for operating
system-level features in the browser environment.

Through Emscripten, interpreters access a sandboxed filesystem (not the
user's actual filesystem), standard input/output streams, and network
capabilities. These features work within the browser's security sandbox,
providing familiar Python programming patterns whilst maintaining web
security.

This is why you can use `open()` to read files, `print()` to write
output, and `import` modules - Emscripten bridges the gap between Python's
expectations and the browser's capabilities.

## What's next

Now that you understand PyScript's architecture, these related topics
provide more context:

**[Workers](workers.md)** - Configure Python code to run in background
threads with the same configuration options.

**[Filesystem](filesystem.md)** - Learn more about the virtual
filesystem and how the `files` option works.

**[FFI](ffi.md)** - Understand how JavaScript modules integrate with
Python through the foreign function interface.

**[Media](media.md)** - Capture photos and video with the camera or 
record audio with your microphone.