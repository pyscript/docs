# User Guide

!!! info

    This guide provides technical guidance and exploration of the PyScript
    platform.

    While we endeavour to write clearly, some of the content in this user guide
    will not be suitable for beginners. We assume readers already have Python
    or web development experience. If you're a beginner start with our
    [beginner's guide](beginning-pyscript.md).

    We [welcome constructive feedback](https://github.com/pyscript/docs/issues).

This guide has three aims:

1. A [clear overview](#what-is-pyscript) of all things PyScript.
2. [Exploration of PyScript](#architecture) in substantial technical detail.
3. Demonstration of the features of PyScript working together in
   [real-world example applications](#examples).

_Read this page in full_: it is a short but comprehensive overview of the
PyScript platform.

Get involved! Join in the PyScript conversation on our
[discord server](https://discord.gg/HxvBtukrg2). There you'll find core
developers, community contributors and a flourishing forum for those creating
projects with PyScript. Should you wish to engage with the development of
PyScript, you are welcome to contribute via 
[the project's GitHub organisation](https://github.com/pyscript).

Finally, the projects at the end of this page are all freely available
and copiously commented on [pyscript.com](https://pyscript.com).

!!! note

    Many of these examples come from contributors in our wonderful
    community. We love to recognise, amplify and celebrate the incredible work
    of folks in the PyScript community. If you believe you have a project that
    would make a good demonstration, please don't hesitate to
    [get in touch](https://discord.gg/HxvBtukrg2).

## What is PyScript?

[PyScript](https://pyscript.net) is a platform for [Python](https://python.org) in the
[browser](https://en.wikipedia.org/wiki/Web_browser).

PyScript brings together two of the most vibrant technical ecosystems on the
planet. If [the web](https://en.wikipedia.org/wiki/World_Wide_Web) and Python
had a baby, you'd get PyScript.

PyScript works because modern browsers support
[WebAssembly](https://webassembly.org/) (abbreviated to WASM) - an
[instruction set](https://en.wikipedia.org/wiki/Instruction_set_architecture)
for a [virtual machine](https://en.wikipedia.org/wiki/Virtual_machine) with
an open specification and near native performance. PyScript takes
versions of the Python interpreter compiled to WASM, and makes them easy to use
inside the browser.

At the core of PyScript is a _philosophy of digital empowerment_. The web is
the world's most ubiquitous computing platform, mature and familiar to billions
of people. Python is one of the
[world's most popular programming languages](https://spectrum.ieee.org/the-top-programming-languages-2023):
it is easy to teach and learn, used in a plethora of existing domains
(such as data science, games, embedded systems, artificial intelligence,
finance, physics  and film production - to name but a few), and the Python
ecosystem contains a huge number of popular and powerful libraries to address
its many uses.

PyScript brings together the ubiquity, familiarity and accessibility of the web
with the power, depth and expressiveness of Python. It means PyScript isn't
just for programming experts but, as we like to say, for the 99% of the rest of
the planet who use computers.

## Features

<dl>
    <dt><em>All the web</em></dt>
    <dd>
    <p>Pyscript gives you <a href="#the-dom">full access to the DOM</a> and all
    the <a href="https://developer.mozilla.org/en-US/docs/Web/API">web
    APIs implemented by your browser</a>.</p>

    <p>Thanks to the <a href="#ffi">foreign
    function interface</a> (FFI), Python just works with all the browser has to
    offer, including any third party JavaScript libraries that may be included
    in the page.</p>

    <p>The FFI is bi-directional ~ it also enables JavaScript to access the
    power of Python.</p></dd>

    <dt><em>All of Python</em></dt>
    <dd>
    <p>PyScript brings you two Python interpreters:</p>
    <ol>
        <li><a href="#pyodide">Pyodide</a> - the original standard
        CPython interpreter you know and love, but compiled to WebAssembly.
        </li>
        <li><a href="#micropython">MicroPython</a> - a lean and
        efficient reimplementation of Python3 that includes a comprehensive
        subset of the standard library, compiled to WebAssembly.</li>
    </ol>
    <p>Because it is just regular CPython, Pyodide puts Python's deep and
    <a href="https://pypi.org/">diverse ecosystem</a> of libraries, frameworks
    and modules at your disposal. No matter the area of computing endeavour,
    there's probably a Python library to help. Got a favourite library in
    Python? Now you can use it in the browser and share your work with just 
    a URL.</p>
    <p>MicroPython, because of its small size (170k) and speed, is especially
    suited to running on more constrained browsers, such as those on mobile
    or tablet devices. It includes a powerful sub-set of the Python standard
    library and efficiently exposes the expressiveness of Python to the
    browser.</p>
    <p>Both Python interpreters supported by PyScript implement the
    <a href="#ffi">same FFI</a> to bridge the gap between the worlds of Python
    and the browser.</p>
    </dd>

    <dt><em>AI and Data science built in</em></dt>
    <dd>Python is famous for its extraordinary usefulness in artificial
    intelligence and data science. The Pyodide interpreter comes with many of
    the libraries you need for this sort of work already baked in.</dd>

    <dt><em>Mobile friendly MicroPython</em></dt>
    <dd>
    <p>Thanks to MicroPython in PyScript, there is a compelling story for
    Python on mobile.</p>

    <p>MicroPython is small and fast enough that your app will start quickly
    on first load, and almost instantly (due to the cache) on subsequent
    runs.</p></dd>

    <dt><em>Parallel execution</em></dt>
    <dd>Thanks to a browser technology called
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API">web workers</a>
    expensive and blocking computation can run somewhere other than the main
    application thread controlling the user interface. When such work is done
    on the main thread, the browser appears frozen; web workers ensure
    expensive blocking computation <a href="#workers">happens elsewhere</a>.
    Think of workers as independent subprocesses in your web page.</dd>

    <dt><em>Rich and powerful plugins</em></dt>
    <dd>
    <p>PyScript has a small, efficient yet powerful core called
    <a href="https://github.com/pyscript/polyscript">PolyScript</a>. Most of
    the functionality of PyScript is actually implemented through PolyScript's
    <a href="#plugins_1">plugin system</a>.</p>

    <p>This approach ensures a clear separation of concerns: PolyScript
    can focus on being small, efficient and powerful, whereas the PyScript
    related plugins allow us to build upon the solid foundations of
    PolyScript.</p>

    <p>Because there is a plugin system, folks
    <em>independent of the PyScript core team</em> have a way to create and
    contribute to a rich ecosystem of plugins whose functionality reflects the
    unique and diverse needs of PyScript's users.</p>
    </dd>
</dl>

## First steps

It's simple:

* tell your browser to use PyScript, then,
* tell PyScript how to run your Python code.

For the browser to use PyScript, simply add a `<script>` tag, whose `src`
attribute references a CDN url for `pyscript.core`, to your HTML document's
`<head>`. We encourage you to add a reference to optional PyScript related
CSS:

```html title="Reference PyScript in your HTML"
<!doctype html>
<html>
    <head>
        <!-- Recommended meta tags -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <!-- PyScript CSS -->
        <link rel="stylesheet" href="https://pyscript.net/snapshots/2023.09.1.RC2/core.css">
        <!-- This script tag bootstraps PyScript -->
        <script type="module" src="https://pyscript.net/snapshots/2023.09.1.RC2/core.js"></script>
    </head>
    <body>
        <!-- your code goes here... -->
    </body>
</html>
```

There are two ways to tell PyScript how to find your code.

* With a standard HTML `<script>` tag whose `type` attribute is either `py`
  (for Pyodide) or `mpy` (for MicroPython). **This is the recommended way**.
* Via the bespoke `<py-script>` (Pyodide) and `<mpy-script>` (MicroPython)
  tags. Historically, `<py-script>` used to be the only way to reference your
  code.

These should be inserted into the `<body>` of your HTML document.

In both cases either use the `src` attribute to reference a Python
file containing your code, or inline your code between the opening and closing
tags. **We recommend you use the `src` attribute method**, but retain the
ability to include code between tags for convenience.

Here's a `<script>` tag with a `src` attribute containing a URL
pointing to a `main.py` Python file.

```html title="A &lt;script&gt; tag with a source file"
<script type="mpy" src="main.py"></script>
```

...and here's a `<py-script>` tag with inline Python code.

```html title="A &lt;py-script&gt; tag with inline code"
<py-script>
import sys
from pyscript import display


display(sys.version)
</py-script>
```

The `<script>` and `<py-script>` / `<mpy-script>` tags may have the following
attributes:

* `src` - the content of the tag is ignored and the Python code in the
  referenced file is evaluated instead. **This is the recommended way to
  reference your Python code.**
* `config` - your code will only be evaluated after the referenced
  [configuration](#configuration) has been parsed. Since configuration can be
  JSON or a TOML file,
  `config='{"packages":["numpy"]}'` and `config="./config.json"` or
  `config="./config.toml"` are all valid.
* `async` - your Python code can contain a
  [top level await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await#top_level_await).
* `worker` - a flag to indicate your Python code is to be run on a
  [web worker](#workers) instead of the "main thread" that looks after the user
  interface.
* `target` - The id or selector of the element where calls to
  [`display()`](#pyscriptdisplay) should write their values. 

!!! warning

    The `packages` setting used in the example configuration shown above is a
    **Pyodide-only feature** because MicroPython doesn't support code packaged
    on PyPI.

    For more information please refer to the [packages section](#packages) of
    this user guide.

!!! question

    Why do we recommend use of the `<script>` tag with a `src` attribute?

    Within the [HTML standard](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script),
    the `<script>` tag is used to embed executable code. Its use case
    completely aligns with our own, as does its default behaviour.

    By referencing a separate Python source file via the `src` attribute, your
    code is just a regular Python file your code editor will understand. Python
    code embedded within a `<script>` tag in an HTML file won't benefit from
    the advantages code editors bring: syntax highlighting, code analysis,
    language-based contextual awareness and perhaps even an AI co-pilot.

    Both the `<py-script>` and `<mpy-script>` tags with inline code are
    [web components](https://developer.mozilla.org/en-US/docs/Web/API/Web_Components)
    that are _not built into the browser_. While they are convenient, there is
    a performance cost to their use.

!!! info
    The browser's tab displaying the website running PyScript is an isolated
    computing sandbox. Define the Python environment in which your code will
    run with [configuration options](#configuration) (discussed later in this
    document).

!!! tip 

    If you want to run code on both the main thread and in a worker, be
    explicit and use separate tags.

    ```html
    <script type="mpy" src="main.py"></script>  <!-- on the main thread -->
    <script type="py" src="worker.py" worker config="pyconfig.toml"></script> <!-- on the worker -->
    ```

    Notice how different interpreters can be used with different
    configurations.

## Architecture

PyScript's architecture has two core concepts:

1. A small, efficient and powerful kernel called
   [PolyScript](https://github.com/pyscript/polyscript) is the foundation
   upon which PyScript and plugins are built.
2. The PyScript [stack](https://en.wikipedia.org/wiki/Solution_stack) inside
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

```html title="Bootstrapping with PolyScript"
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
* Handling of
  [browser events](https://pyscript.github.io/polyscript/#how-events-work)
  via code evaluated by an interpreter supported by PolyScript.
* A [clear way to use workers](https://pyscript.github.io/polyscript/#xworker)
  via the `XWorker` class and its related reference, `xworker`.
* [Custom scripts](https://pyscript.github.io/polyscript/#custom-scripts) to
  enrich PolyScript's capabilities.
* A [ready event](https://pyscript.github.io/polyscript/#ready-event)
  dispatched when an interpreter is ready and about to run code.
* [Multipe interpreters](https://pyscript.github.io/polyscript/#interpreter-features)
  (in addition to Pyodide and MicroPython, PolyScript works with Lua and Ruby -
  although these are beyond the scope of this project).

### The stack

The stack describes how the different building blocks _inside_ a PyScript
application relate to each other:

<img src="../assets/images/platform.png"/>

* Everything happens inside the context of the browser (represented by the
  black border). It means the browser tab for your PyScript app is your
  sandboxed computing environment.

!!! failure

    PyScript is simply Python running in the browser. It is an unfamiliar
    concept that some fail to remember.

    * PyScript isn't running on a server hosted in the cloud.
    * PyScript doesn't use the version of Python running natively on the user's
      operating system.
    * **PyScript only runs IN THE BROWSER (and nowhere else).**

* At the bottom of the stack are the Python interpreters compiled to WASM. They
  evaluate your code and interact with the browser via the [FFI](#ffi).
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
    2. Evaluate any [configuration](#configuration) on the page (either via
       single `<py-config>` or `<mpy-config>` tags **or** the `config`
       attribute of a `<script>`, `<py-script>` or `<mpy-script>` tag).
    3. Given the detected configuration, download the required interpreter.
    4. Setup the interpreter's environment. This includes any
       [plugins](#plugins), [packages](#packages) or [files](#files) that need
       to be loaded.
    5. Make available various
       [builtin helper objects and functions](#builtin-helpers) to the
       interpreter's environment (accessed via the `pyscript` module).
    6. Only then use the interpreter in the correctly configured environment to
       evaluate the detected Python code.
* When an interpreter is ready the `py:ready` or `mpy:ready` events are
  dispatched, depending which interpreter you've specified (Pyodide or
  MicroPython respectively).
* Finally, a `py:all-done` event is dispatched after every single script
  referenced from the page has finished.

In addition, various "hooks" are called at different moments in the lifecycle
of PyScript. These can be used by plugin authors to modify or enhance the
behaviour of PyScript. The hooks, and how to use them, are explored further in
[the section on plugins](#plugins_1).

!!! warning

    A web page's workers have completely separate environments to the main
    thread.

    It means configuration in the main thread can be different to that for
    an interpreter running on a worker. In fact, you can use different
    interpreters and configuration in each context (for instance, MicroPython
    on the main thread, and Pyodide on a worker).

## Interpreters

Python is an interpreted language, and thus needs an interpreter to work.

PyScript supports two versions of the Python interpreter that have
been compiled to WASM: Pyodide and MicroPython. You should select which one to
use depending on your use case and acceptable trade-offs.

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
[foreign function interface](#ffi) (FFI). This
bridges the gap between the browser and Python worlds.

### Pyodide

<a href="https://pyodide.org/"><img src="../assets/images/pyodide.png"/></a>

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
    find a "pure Python wheel" for a package. The Pyodide documentation
    [explains what to do in this situation](https://pyodide.org/en/stable/usage/faq.html#why-can-t-micropip-find-a-pure-python-wheel-for-a-package).

    Briefly, some packages with C extensions have versions compiled for WASM
    and these can be installed with `micropip`. Packages containing C
    extensions that _are not compiled for WASM_ cause the "pure Python wheel"
    error.

    There are plans afoot to make WASM a target in PyPI so packages with C
    extenions can be automatically compiled to WASM.

### MicroPython

<a href="https://micropython.org/"><img src="../assets/images/micropython.png"/></a>

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

Thanks to collaboration between the MicroPython and PyScript projects, there is
a foreign function interface for MicroPython. The MicroPython FFI deliberately
copies the API of the FFI originally written for Pyodide - meaning it is
relatively easy to migrate between the two supported interpreters.

## Configuration

The browser tab in which your PyScript based web page is displayed is a very
secure sandboxed computing environment for running your Python code.

This is also the case for web workers running Python. Despite being associated
with a single web page, workers are completely separate from each other
(except for some very limited and clearly defined means of interacting, which
PyScript looks after for you).

We need to tell PyScript how we want such Python environments to be configured.
This works in the same way for both the main thread and for web workers. Such
configuration ensures we get the expected resources ready before our Python
code is evaluated (resources such as arbitrary data files, third party Python
packages and PyScript plugins).

### TOML or JSON

Configuration can be expressed in two formats:

* [TOML](https://toml.io/en/) is the configuration file format preferred by
  folks in the Python community.
* [JSON](https://www.json.org/json-en.html) is a data format most often used
  by folks in the web community.

Since PyScript is the marriage of Python and the web, and we respect the
traditions of both technical cultures, we support both formats.

However, because JSON is built into all browsers by default and TOML requires
an additional download of a specialist parser before PyScript can work, **the
use of JSON is more efficient from a performance point of view**.

The following two configurations are equivalent, and simply tell PyScript to
ensure the packages [arrr](https://arrr.readthedocs.io/en/latest/) and
[numberwang](https://numberwang.readthedocs.io/en/latest/) are installed from
PyPI (the [Python Packaging Index](https://pypi.org/)):

```TOML title="Configuration via TOML"
packages = ["arrr", "numberwang" ]
```

```JSON title="Configuration via JSON"
{
    "packages": ["arrr", "numberwang"]
}
```

### File or inline

The recommended way to write configuration is via a separate file and then
reference it from the tag used to specify the Python code:

```HTML title="Reference a configuration file"
<script type="py" src="main.py" config="pyscript.toml"></script>
```

If you use JSON, you can make it the value of the `config` attribute:

```HTML title="JSON as the value of the config attribute"
<script type="mpy" src="main.py" config='{"packages":["arrr", "numberwang"]}'></script>
```

For historical and convenience reasons we still support the inline
specification of configuration information via a _single_ `<py-config>` or
`<mpy-config>` tag in your HTML document:

```HTML title="Inline configuration via the &lt;py-config&gt; tag"
<py-config>
{
    "packages": ["arrr", "numberwang" ]
}
</py-config>
```

!!! warning

    Should you use `<py-config>` or `<mpy-config>`, **there must be only one of
    these tags on the page per interpreter**.

### Options

There are four core options ([`interpreter`](#interpreter), [`files`](#files),
[`packages`](#packages) and [`plugins`](#plugins)). The user is free to define
arbitrary additional configuration options that plugins or an app may require
for their own reasons.

#### Interpreter

The `interpreter` option pins the Python interpreter to the version of the
specified value. This is useful for testing (does my code work on a specific
version of Pyodide?), or to ensure the precise combination of PyScript version
and interpreter version are pinned to known values.

The value of the `interpreter` option should be a valid version number
for the Python interpreter you are configuring, or a fully qualified URL to
a custom version of the interpreter.

The following two examples are equivalent:

```TOML title="Specify the interpreter version in TOML"
interpreter = "0.23.4"
```

```JSON title="Specify the interpreter version in JSON"
{
    "interpreter": "0.23.4"
}
```

The following JSON fragment uses a fully qualified URL to point to the same
version of Pyodide as specified in the previous examples:

```JSON title="Specify the interpreter via a fully qualified URL"
{
    "interpreter": "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.mjs"
}
```

#### Files

The `files` option fetches arbitrary content from URLs onto the filesystem
available to Python, and emulated by the browser. Just map a valid URL to a
destination filesystem path.

The following JSON and TOML are equivalent:

```json title="Fetch files onto the filesystem with JSON"
{
  "files": {
    "https://example.com/data.csv": "./data.csv",
    "/code.py": "./subdir/code.py"
  }
}
```

```toml title="Fetch files onto the filesystem with TOML"
[files]
"https://example.com/data.csv" = "./data.csv"
"/code.py" = "./subdir/code.py"
```

If you make the target an empty string, the final "filename" part of the source
URL becomes the destination filename, in the root of the filesystem, to which
the content is copied. As a result, the `data.csv` entry from the previous
examples could be equivalently re-written as:

```json title="JSON implied filename in the root directory"
{
  "files": {
    "https://example.com/data.csv": "",
    ... etc ...
  }
}
```

```toml title="TOML implied filename in the root directory"
[files]
"https://example.com/data.csv" = ""
... etc ...
```


!!! warning

    **PyScript expects all file destinations to be unique.**

    If there is a duplication PyScript will raise an exception to help you find
    the problem.

!!! tip

    **For most people, most of the time, the simple URL to filename mapping,
    described above, will be sufficient.**

    Yet certain situations may require more flexibility. In which case, read
    on.

Sometimes many resources are needed to be fetched from a single location and
copied into the same directory on the file system. To aid readability and
reduce repetition, the `files` option comes with a mini
[templating language](https://en.wikipedia.org/wiki/Template_processor)
that allows re-usable placeholders to be defined between curly brackets (`{`
and `}`). When these placeholders are encountered in the `files` configuration,
their name is replaced with their associated value.

!!! Attention

    Valid placeholder names are always enclosed between curly brackets
    (`{` and `}`), like this: `{FROM}`, `{TO}` and `{DATA SOURCE}`
    (capitalized names help identify placeholders
    when reading code ~ although this isn't strictly necessary).

    Any number of placeholders can be defined and used anywhere within URLs and
    paths that map source to destination.

The following JSON and TOML are equivalent:

```json title="Using the template language in JSON"
{
  "files": {
    "{DOMAIN}": "https://my-server.com",
    "{PATH}": "a/path",
    "{VERSION}": "1.2.3",
    "{FROM}": "{DOMAIN}/{PATH}/{VERSION}",
    "{TO}": "./my_module",
    "{FROM}/__init__.py": "{TO}/__init__.py",
    "{FROM}/foo.py": "{TO}/foo.py",
    "{FROM}/bar.py": "{TO}/bar.py",
    "{FROM}/baz.py": "{TO}/baz.py",
  }
}
```

```toml title="Using the template language in TOML"
[files]
"{DOMAIN}" = "https://my-server.com"
"{PATH}" = "a/path"
"{VERSION}" = "1.2.3"
"{FROM}" = "{DOMAIN}/{PATH}/{VERSION}"
"{TO}" = "./my_module"
"{FROM}/__init__.py" = "{TO}/__init__.py"
"{FROM}/foo.py" = "{TO}/foo.py"
"{FROM}/bar.py" = "{TO}/bar.py"
"{FROM}/baz.py" = "{TO}/baz.py"
```

The `{DOMAIN}`, `{PATH}`, and `{VERSION}` placeholders are
used to create a further `{FROM}` placeholder. The `{TO}` placeholder is also
defined to point to a common sub-directory on the file system. The final four
entries use `{FROM}` and `{TO}` to copy over four files (`__init__.py`,
`foo.py`, `bar.py` and `baz.py`) from the same source to a common destination
directory.

For convenience, if the destination is just a directory (it ends with `/`)
then PyScript automatically uses the filename part of the source URL as the
filename in the destination directory.

For example, the end of the previous config file could be:

```toml
"{TO}" = "./my_module/"
"{FROM}/__init__.py" = "{TO}"
"{FROM}/foo.py" = "{TO}"
"{FROM}/bar.py" = "{TO}"
"{FROM}/baz.py" = "{TO}"
```

#### Packages

The `packages` option defines a list of Python `packages` to be installed from
[PyPI](https://pypi.org/) onto the filesystem by Pyodide's 
[micropip](https://micropip.pyodide.org/en/stable/index.html) package
installer.

!!! warning

    Because `micropip` is a Pyodide-only feature, and MicroPython doesn't
    support code packaged on PyPI, **the `packages` option is only available
    for use with Pyodide**.

    If you need **Python modules for MicroPython** to use, you should use the
    [files](#files) option to manually copy the source code onto the
    file system.

The following two examples are equivalent:

```TOML title="A packages list in TOML"
packages = ["arrr", "numberwang", "snowballstemmer>=2.2.0" ]
```

```JSON title="A packages list in JSON"
{
    "packages": ["arrr", "numberwang", "snowballstemmer>=2.2.0" ]
}
```

The names in the list of `packages` can be any of the following valid forms:

* A name of a package on PyPI: `"snowballstemmer"`
* A name for a package on PyPI with additional constraints:
  `"snowballstemmer>=2.2.0"`
* An arbitrary URL to a Python package: `"https://.../package.whl"`
* A file copied onto the browser based file system: `"emfs://.../package.whl"`

#### Plugins

The `plugins` option lists plugins enabled by PyScript to add extra
functionality to the platform.

Each plugin should be included on the web page, as described in the
[plugins](#plugins_1) section below. Then the plugin's name should be listed.

```TOML title="A list of plugins in TOML"
plugins = ["custom_plugin", "!error"]
```

```JSON title="A list of plugins in JSON"
{
    "plugins": ["custom_plugin", "!error"]
}
```

!!! info

    The `"!error"` syntax is a way to turn off a plugin built into PyScript
    that is enabled by default.

    Currently, the only built-in plugin is the `error` plugin to display a
    stack trace and error messages in the DOM. More may be added at a later
    date.

#### Custom 

Sometimes plugins or apps need bespoke configuration options.

So long as you don't cause a name collision with the built-in option names then
you are free to use any valid data structure that works with both TOML and JSON
to express your configuration needs.

**TODO: explain how to programmatically get access to an object representing
the config.**

## The DOM

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

### FFI

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

The objects in your Python code look and behave like Python
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


### PyDom

The Standard Web APIs are massive and not always very user-friendly. `PyDom` is a
Python modue that exposes the power of the web with an easy and idiomatic Pythonic
interface on top.

While the[FFI](#ffi) interface described above focuses on giving full access to
the entire Standard Web APIs, `pydom` focuses on providing a small, intuitive and yet
powerful API that priotirizes common use cases fist. For this reason, it's first
layer is simple and intuitive (but limited to the most common use cases), but `pydom`
also provides a secondary layer that can be used to directly use full FFI interface
of a specific element.

It does not aim to replace the regular Web [Javascript] API nor to be as wide and offer
feature parity. On the contrary, it's intentionally small and focused on the most popular
use cases while still providing [a backdoor] access to the full JS API.


`Pydom` draws inspiration from popular Python APIs/Libraries known to be friendly and
easy to learn, and other successful projects related the web as well (for isntance,
`JQuery` was a good source of inspiration).

#### Core Concepts



The PyDom API is extensively described and demonstrated
[on this PyScript page](https://fpliger.pyscriptapps.com/pyweb/latest/pydom.html).

!!! warning

    PyDom is currently a work in progress.

    We welcome feedback and suggestions.


    
## Workers

Workers run code that won't block the "main thread" controlling the user
interface. If you block the main thread, your web page becomes annoyingly
unresponsive.** You should never block the main thread.**

Happily, PyScript makes it very easy to use workers.

To make this happen PyScript uses a feature recently added to web standards
called
[Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics).

### HTTP headers

For Atomics to work **you must ensure your web server enables the following
headers** (this is the default behaviour for
[pyscript.com](https://pyscript.com)):

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Resource-Policy: cross-origin
```

If you are not able to configure your server's headers, use the
[mini-coi](https://github.com/WebReflection/mini-coi#readme) project to
achieve the same end.

### Start working

To start your code in a worker, simply ensure the `<script>`, `<py-script>` or
`<mpy-script>` tag pointing to the code you want to run has a `worker`
attribute flag:

```HTML title="Evaluating code in a worker"
<script type="py" src="./my-worker-code.py" worker></script>
```

Code running in the worker needs to be able to access the web page running in
the main thread. This is achieved via builtin helper utilities described in the
next section.

!!! note

    For ease of use, the worker related functionality in PyScript is
    a simpler presentation of more sophisticated and powerful behaviour
    available via PolyScript.

    **If you are a confident advanced user**, please
    [consult the XWorker](https://pyscript.github.io/polyscript/#xworker)
    related documentation from the PolyScript project for how to make use of
    these features.

## Builtin helpers

PyScript makes available convenience objects and functions inside
Python. This is done via the `pyscript` module:

```python title="Accessing the document object via the pyscript module"
from pyscript import document
```

### Common features

These objects / functions are available in both the main thread and in code
running on a web worker:

#### `pyscript.window`

This object is a proxy for the web page's
[global window context](https://developer.mozilla.org/en-US/docs/Web/API/Window).

!!! warning

    Please note that in workers, this is still the main window, not the
    worker's own global context. A worker's global context is reachable instead
    via `import js` (the `js` object being a proxy for the worker's
    `globalThis`).

#### `pyscript.document`

This object is a proxy for the the web page's
[document object](https://developer.mozilla.org/en-US/docs/Web/API/Document).
The `document` is a representation of the
[DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Using_the_Document_Object_Model)
and can be used to manipulate the content of the web page.

#### `pyscript.display`

A function used to display content. The function is intelligent enough to
introspect the object[s] it is passed and work out how to correctly display the
object[s] in the web page.

The `display` function takes a list of `*values` as its first argument, and has
two optional named arguments:

* `target=None` - the DOM element into which the content should be placed.
* `append=True` - a flag to indicate if the output is going to be appended to
  the `target`.

There are some caveats:

* When used in the main thread, the `display` function automatically uses
  the current `<script>` tag as the `target` into which the content will
  be displayed.
* If the `<script>` tag has the `target` attribute, the element on the page
  with that ID (or which matches that selector) will be used to display
  the content instead.
* When used in a worker, the `display` function needs an explicit
  `target="dom-id"` argument to identify where the content will be
  displayed.
* In both the main thread a worker, `append=True` is the default
  behaviour.

#### `pyscript.when`

A Python decorator to indicate the decorated function should handle the
specified events for selected elements.

The decorator takes two parameters:

* The `event_type` should be the name of the
  [browser event to handle](https://developer.mozilla.org/en-US/docs/Web/Events)
  as a string (e.g. `"click"`).
* The `selector` should be a string containing a
  [valid selector](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model/Locating_DOM_elements_using_selectors)
  to indicate the target elements in the DOM whose events of `event_type` are
  of interest.

The following example has a button with an id of `my_button` and a decorated
function that handles `click` events dispatched by the button.

```html title="The HTML button"
<button id="my_button">Click me!</button>
```

```python title="The decorated Python function to handle click events"
from pyscript import when


@when("click", "#my_button")
def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    print("I've been clicked!")
```

### Main-thread only features

#### `pyscript.PyWorker`

A class used to instantiate a new worker from within Python.

!!! danger 

    Currently this only works with Pyodide.

The following fragment demonstrates who to start the Python code in the file
`worker.py` on a new worker from within Python.

```python title="Starting a new worker from Python"
from pyscript import PyWorker


a_worker = PyWorker("./worker.py")
```

### Worker only features

#### `pyscript.sync`

A function used to pass serializable data from workers to the main thread. 

Imagine you have this code on the main thread:

```python title="Python code on the main thread"
from pyscript import PyWorker

def hello(name="world"):
    display(f"Hello, {name}")

worker = PyWorker("./worker.py")
worker.sync.hello = hello
```

In the code on the worker, you can pass data back to handler functions like
this:

```python title="Pass data back to the main thread from a worker"
from pyscript import sync

sync.hello("PyScript")
```

## Plugins

**TODO: FINISH THIS**

# Examples
<!--

### Lots of DOM manipulation

### Data science-y

### Graphical

### Blocking with workers

### Calling an API -->
