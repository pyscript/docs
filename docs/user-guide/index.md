# The PyScript User Guide

!!! info

    This guide provides technical guidance and in-depth exploration of
    the PyScript platform.

    We assume you already have Python or web development experience. If
    you're new to PyScript, start with our
    [beginner's guide](../beginning-pyscript.md) to learn the
    fundamentals through a hands-on example.

    Once you're comfortable with the basics, return here to explore
    PyScript's full capabilities in detail.

## What you'll learn

This user guide will teach you how to:

**Build interactive web applications with Python** - Create rich user
interfaces, handle events, manipulate the DOM, and respond to user input
using idiomatic Python code.

**Leverage Python's ecosystem in the browser** - Use popular libraries
like NumPy, Pandas, Matplotlib, and thousands more from PyPI directly in
your web applications.

**Access browser capabilities from Python** - Capture photos and video,
record audio, read and write files, store data locally, and integrate
with web APIs.

**Create fast, responsive applications** - Use web workers to run Python
code in background threads, keeping your user interface smooth even
during heavy computation.

**Deploy Python applications anywhere** - Share your work with a simple
URL, no server-side Python required. Your applications run entirely in
the user's browser.

**Understand PyScript's architecture** - Learn how PyScript bridges
Python and JavaScript, when to use Pyodide vs. MicroPython, and how to
optimise your applications for performance.

## How to use this guide

This guide is organised into focused sections that build upon each other.
We recommend reading them in this order:

1. **[What is PyScript?](what.md)** - Understand the philosophy and
   capabilities of the platform.

2. **[First steps](first-steps.md)** - Learn the basic structure of a
   PyScript application.

3. **[Configuration](configuration.md)** - Discover how to configure
   your Python environment, specify packages, and customise PyScript's
   behaviour.

4. **[DOM interaction](dom.md)** - Master the core skill of working with
   web page elements using both the FFI and the `pyscript.web` module.

5. **[Events](events.md)** - Learn to respond to user actions and
   browser events with the `@when` decorator and other patterns.

6. **[Workers](workers.md)** - Understand how to use background threads
   for responsive applications.

7. **[Filesystem](filesystem.md)** and **[Media](media.md)** - Explore
   device capabilities like file access, camera, and audio.

8. **[Architecture](architecture.md)** - Dive deep into how PyScript
   works under the hood.

Of course, you can jump directly to any section that interests you. Each
page is written to be useful on its own, with cross-references to related
topics.

!!! tip

    New to web development? The [DOM interaction](dom.md) and
    [events](events.md) sections are essential reading. They explain
    core concepts that apply to all web applications, not just PyScript.

## Core concepts

PyScript brings together two powerful ecosystems: Python and the web.
Understanding a few key concepts will help you get the most from the
platform:

**The FFI (Foreign Function Interface)** - This is how Python and
JavaScript communicate. The FFI automatically translates between Python
and JavaScript objects, letting you use browser APIs directly from
Python code.

**Pyodide vs. MicroPython** - PyScript supports two Python interpreters.
Pyodide is full CPython compiled to WebAssembly, giving you access to
the entire Python ecosystem. MicroPython is smaller and faster to load,
making it ideal for mobile devices or when you don't need heavy
libraries.

**The `pyscript` namespace** - This is PyScript's Pythonic API for
working with the web. It includes modules like `pyscript.web` for DOM
manipulation, `pyscript.display` for showing output, and decorators like
`@when` for handling events.

**Web workers** - Background threads that let you run Python code
without blocking the user interface. Essential for data processing,
simulations, or any CPU-intensive work.

## Example applications

Throughout this guide, you'll find working examples that demonstrate
PyScript's features. All examples are complete, runnable applications
that you can explore, modify, and learn from.

You'll find the example applications in the
[`example-apps` directory in the source code for these docs](https://github.com/pyscript/docs/tree/main/docs/example-apps),
organised by app name. Each example includes all the files you need
(`index.html`, Python code, configuration) plus a README explaining what
it demonstrates and how it works.

## Get involved

PyScript is an open source project with a welcoming, vibrant community.

**Join the conversation** - Our [Discord server](https://discord.gg/HxvBtukrg2)
is the heart of the PyScript community. You'll find core developers,
experienced contributors, and fellow learners ready to help. It's the
best place to ask questions, share your projects, and discuss ideas.

**Contribute to PyScript** - Whether you're fixing documentation,
reporting bugs, or adding features, contributions are welcome. Visit
[PyScript's GitHub organisation](https://github.com/pyscript) to get
started.

**Share your work** - Built something interesting with PyScript? We love
to recognise and celebrate community projects. Share your work on
Discord or [get in touch](https://discord.gg/HxvBtukrg2) if you'd like
your project featured in our examples.

!!! note

    We [welcome constructive feedback](https://github.com/pyscript/docs/issues)
    on these docs. Found something unclear? Have a suggestion? Please let
    us know.

## Ready to dive in?

Start with [What is PyScript?](what.md) to understand the platform's
philosophy and capabilities, or jump straight to
[First steps](first-steps.md) if you're eager to start coding.

Welcome to PyScript!