# FAQ

This page contains the most common questions and "*gotchas*" asked on
[our Discord server](https://discord.gg/HxvBtukrg2), in
[our community calls](https://www.youtube.com/@PyScriptTV), or
within our community.

There are two major areas we'd like to explore:
[common errors](#common-errors) and [helpful hints](#helpful-hints).

## Common errors

### Reading errors

If your application doesn't run, and you don't see any error messages on the
page, you should check
[your browser's console](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools).

When reading an error message, the easy way to find out what's going on,
most of the time, is to read the last line of the error.

```text title="A Pyodide error."
Traceback (most recent call last):
  File "/lib/python311.zip/_pyodide/_base.py", line 501, in eval_code
    .run(globals, locals)
     ^^^^^^^^^^^^^^^^^^^^
  File "/lib/python311.zip/_pyodide/_base.py", line 339, in run
    coroutine = eval(self.code, globals, locals)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 1, in <module>
NameError: name 'failure' is not defined
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```text title="A MicroPython error."
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'failure' isn't defined
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

In both examples, the code created a
[`NameError`](https://docs.python.org/3/library/exceptions.html#NameError)
because the object with the name `failure` did not exist. Everything above the
error message is potentially useful technical detail.

With this context in mind, these are the most common errors users of PyScript
encounter.

### SharedArrayBuffer

This is the first and most common error users may encounter with PyScript.

!!! failure

    Your application doesn't run and in
    [your browser's console](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools)
    you see this message:

    ```
    Unable to use SharedArrayBuffer due insecure environment.
    Please read requirements in MDN: ...
    ```

The error contains
[a link to MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer#security_requirements)
but it's the amount of content provided on this topic is overwhelming.

#### When

This error happens when **the server delivering your PyScript application is
incorrectly configured**. It fails to provide the correct headers to handle
security concerns for web workers, or you're not using
[mini-coi](https://github.com/WebReflection/mini-coi#readme) as an alternative
solution. (These requirements are explored
[in the worker page](../user-guide/workers#http-headers).)

**And** at least one of the following scenarios is true:

* There is a `worker` attribute in the *py* or *mpy* script element and the
  [sync_main_only](https://pyscript.github.io/polyscript/#extra-config-features)
  flag is not present or not `true`.
* There is a `<script type="py-editor">` that uses a *worker* behind the
  scenes.
* There is an explicit `PyWorker` or `MPWorker` bootstrapping somewhere in your
  code.

!!! info

    If `sync_main_only` is `true` then interactions between the main thread and
    workers are limited to one way calls from the main thread to methods
    exposed by workers.

If `sync_main_only = True`, the following caveats apply:

* It is not possible to manipulate the DOM or do anything meaningful on the
  main thread **from a worker**. This is because Atomics cannot guarantee
  sync-like locks between a worker and the main thread.
* Only a worker's `pyscript.sync` methods are exposed, and they can only be
  awaited from the main thread.
* The worker can only `await` main thread references one after the other, so
  developer experience is degraded when one needs to interact with the
  main thread.

If your project simply bootstraps on the main thread, none of this is relevant
because no worker requires such special features.

#### Why

The only way for `document.getElementById('some-id').value` to work in a
worker is to use these two JavaScript primitives:

  * **[SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)**,
    to allow multiple threads to read and / or write into a chunk of shared
    memory.
  * **[Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics)**,
    to both `wait(sab, index)` (`sab` is a `SharedArrayBuffer`) and
    `notify(sab, index)` to unlock the awaiting thread.

While a worker waits for an operation on main to happen, it is not using the
CPU. It idles until the referenced index of the shared buffer changes,
effectively never blocking the main thread while still pausing its own
execution until the buffer's index is changed.

As overwhelming or complicated as this might sounds, these two fundamental
primitives make main ↔ worker interoperability an absolute wonder in term of
developer experience. Therefore, we encourage folks to prefer using workers
over running Python in the main thread. This is especially so when using
Pyodide related projects, because of its heavier bootstrap or computation
requirements. Using workers ensures the main thread (and thus, the user
interface) remains unblocked.

Unfortunately, due to security concerns and potential attacks to shared
buffers, each server or page needs to allow extra security to prevent malicious
software to read or write into these buffers. But be assured that if you own
your code, your project, and you trust the modules or 3rd party code you need
and use, **there are less likely to be security concerns around this topic
within your project**. This situation is simply an unfortunate "*one rule catch
all*" standard any server can either enable or disable as it pleases.

### Borrowed proxy

This is another common error that happens with listeners, timers or in any
other situation where a Python callback is lazily invoked from JavaScript:

!!! failure

    Your application doesn't run and in
    [your browser's console](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools)
    you see this message:

    ```
    Uncaught Error: This borrowed proxy was automatically destroyed at the end of a function call.
    Try using create_proxy or create_once_callable.
    For more information about the cause of this error, use `pyodide.setDebug(true)`
    ```

#### When

This error happens when using Pyodide as the interpreter on the main thread,
and when a bare Python callable/function has been passed into JavaScript as a
callback handler:

```python title="An expired borrowed proxy example, with Pyodide on the main thread."
import js


# will throw the error
js.setTimeout(lambda msg: print(msg), 1000, "FAIL")
```

The garbage collector immediately cleans up the Python function once it is
passed into the JavaScript context. Clearly, for the Python function to work as
a callback at some time in the future, it should NOT be garbage collected and
hence the error message.

!!! info

    This error does not happen if the code is executed in a worker and the 
    JavaScript reference comes from the main thread:

    ```python title="Code running on Pyodide in a worker has no borrowed proxy issue."
    from pyscript import window


    window.setTimeout(lambda x: print(x), 1000, "OK")
    ```

    Proxy objects (i.e. how Python objects appear to JavaScript, and vice
    versa) cannot be communicated between a worker and the main thread.

    Behind the scenes, PyScript ensures references are maintained between
    workers and the main thread. It means Python functions in a worker are
    actually represented by JavaScript proxy objects in the main thread.

    As a result, such worker based Python functions are therefore **not** bare
    Python functions, but already wrapped in a managed JavaScript proxy, thus
    avoiding the borrowed proxy problem.

If you encounter this problem you have two possible solutions:

1. Manually wrap such functions with a call to
   [`pyscript.ffi.create_proxy`](../builtins/#pyscriptfficreate_proxy).
2. Set the
   [`experimental_create_proxy = "auto"`](../configuration/#experimental_create_proxy)
   flag in your application's settings. This flag intercepts Python objects
   passed into a JavaScript callback and ensures an automatic and sensible
   memory management operation via the JavaScript garbage collector.

!!! Note

    The
    [FinalizationRegistry](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry)
    is the browser feature used to make this so.

    By default, it is not observable and it is not possible to predict when it
    will free, and hence destroy, retained Python proxy objects. As a result,
    memory consumption might be slightly higher than when manually using
    `create_proxy`. However, the JavaScript engine is responsible for memory
    consumption, and will cause the finalization registry to free all retained
    proxies, should memory consumption become too high.

#### Why

PyScript's interpreters (Pyodide and MicroPython) both have their own garbage
collector for automatic memory management. When references to Python objects
are passed to JavaScript [via the FFI](../user-guide/ffi/), the Python
interpreters cannot guarantee such references will ever be freed by
JavaScript's own garbage collector. They may even lose control over the
reference since there's no infallible way to know when such objects won't be
needed by JavaScript.

One solution is to expect users to explicitly create and destroy such proxy
objects themselves. But this manual memory management makes automatic memory
management pointless while raising the possibility of dead references (where
the user explicitly destroys a Python object that's still alive in the
JavaScript context). Put simply, this is a difficult situation.

Pyodide provides
[ffi.wrappers](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#module-pyodide.ffi.wrappers)
to help with many of the common cases, and PyScript, through the
`experimental_create_proxy = "auto"` configuration option, automates memory
management via the `FinalizationRegistry` described above.

### Python packages

Sometimes Python packages, specified via the
[`packages` configuration setting](../user-guide/configuration/#packages)
don't work with PyScript's Python interpreter.

!!! failure

    **You are using Pyodide**.

    Your application doesn't run and in
    [your browser's console](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools)
    you see this message:

    ```
    ValueError: Can't find a pure Python 3 wheel for: 'package_name'
    ```

!!! failure

    **You are using MicroPython**.

    Your application doesn't run and in
    [your browser's console](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools)
    you see this message:

    ```
    Cross-Origin Request Blocked: The Same Origin Policy disallows reading the
    remote resource at https://micropython.org/pi/v2/package/py/package_name/latest.json.
    (Reason: CORS header ‘Access-Control-Allow-Origin’ missing).
    Status code: 404.
    ```

#### When

This is a complicated problem, but the summary is:

* **Check you have used the correct name for the package you want to use**.
  This is a remarkably common mistake to make: let's just check. :-)
* **In Pyodide**, the error indicates that the package you are trying to
  install has some part of it written in C, C++ or Rust. These languages are
  compiled, and the package has not yet been compiled for web assembly. Our
  friends in the Pyodide project and the
  [Python packaging authority](https://www.pypa.io/en/latest/) are working
  together to ensure web assembly is a default target for compilation. Until
  such time, we suggest you follow
  [Pyodide's own guidance](https://pyodide.org/en/stable/usage/faq.html#why-can-t-micropip-find-a-pure-python-wheel-for-a-package)
  to overcome this situation.
* **In MicroPython**, the package you want to use has not been ported into the
  [`micropython-lib` package repository](https://github.com/micropython/micropython-lib).
  If you want to use a pure Python package with MicroPython, use the
  [files configuration option](../user-guide/configuration/#files) to manually
  copy the package onto the file system, or use a URL to reference the package.

For hints and tips about packaging related aspects of PyScript read the
[packaging pointers](#packaging-pointers) section of this FAQ.

#### Why

Put simply, Pyodide and MicroPython are different Python interpreters, and both
are running in a web assembly environment. Packages built for Pyodide may not
work for MicroPython, and vice versa. Furthermore, if a package contains
compiled code, it may not yet have been natively compiled for web assembly.

If the package you want to use is written in a version of Python that both
Pyodide and MicroPython support (there are subtle differences between the
interpreters), then you should be able to use the package so long as you are
able to get it into the Python path via configuration (see above).

Currently, MicroPython cannot expose modules that require native compilation,
but PyScript is working with the MicroPython team to provide different builds
of MicroPython that include commonly requested packages (e.g. MicroPython's
version of `numpy` or `sqlite`).

!!! warning

    Depending on the complexity of the project, it may be hard to seamlessly
    make a 1:1 port from a Pyodide code base to MicroPython.

    MicroPython has [comprehensive documentation](https://docs.micropython.org/en/latest/genrst/index.html)
    to explain the differences between itself and "regular" CPython (i.e. the
    version of Python Pyodide provides).

### JavaScript modules

When [using JavaScript modules with PyScript](../user-guide/dom/#working-with-javascript)
you may encounter the following errors:

!!! failure

    Uncaught SyntaxError: The requested module './library.js' does not provide an export named 'default'

!!! failure

    Uncaught SyntaxError: The requested module './library.js' does not provide an export named 'util'

#### When

These errors happen because the JavaScript module you are trying to use is not
written as a standards-compliant JavaScript module.

Happily, to **solve** this issue various content delivery networks (CDNs)
provide a way to automatically deliver standard ESM (aka:
[ECMAScript](https://en.wikipedia.org/wiki/ECMAScript) Modules).
The one we recommend is [esm.run](https://esm.run/).

```html title="An example of esm.run"
<mpy-config>
[js_modules.main]
"https://esm.run/d3" = "d3"
</mpy-config>
<script type="mpy">
  from pyscript.js_modules import d3
</script>
```

Alternatively, ensure any JavaScript code you reference uses `export ...` or
ask for an `.mjs` version of the code. All the various options and technical
considerations surrounding the use of JavaScript modules in PyScript are
[covered in our user guide](../user-guide/dom/#working-with-javascript).

#### Why

Even though the standard for JavaScript modules has existed since 2015, many
old and new libraries still produce files that are incompatible with such
modern and idiomatic standards.

This isn't so much a technical problem, as a human problem as folks learn to
use the new standard and migrate old code away from previous and now
obsolete standards.

While such legacy code exists, be aware that JavaScript code may require
special care.

## Helpful hints

This section contains common hacks or hints to make using PyScript easier.

!!! Note

    We have an absolutely lovely PyScript contributor called
    [Jeff Glass](https://github.com/jeffersglass) who maintains an exceptional
    blog full of [PyScript recipes](https://pyscript.recipes/) with even more
    use cases, hints, tips and solutions. Jeff also has a
    [wonderful YouTube channel](https://www.youtube.com/@CodingGlass) full of
    very engaging PyScript related content.

    If you cannot find what you are looking for here, please check Jeff's blog
    as it's likely he's probably covered something close to the situation in
    which you find yourself.

    Of course, if ever you meet Jeff in person, please buy him a beer and
    remember to say a big "thank you". 🍻

### PyScript `latest`

PyScript follows the [CalVer](https://calver.org/) convention for version
numbering.

Put simply, it means each version is numbered according to when, in the
calendar, it was released. For instance, version `2024.4.2` was the _second_
release in the month of April in the year 2024 (**not** the release on the 2nd
of April but the second release **in** April).

It used to be possible to reference PyScript via a version called `latest`,
which would guarantee you always got the latest release.

However, at the end of 2023, we decided to **stop supporting `latest` as a
way to reference PyScript**. We did this for two broad reasons:

1. In the autumn of 2023, we release a completely updated version of PyScript
   with some breaking changes. Folks who wrote for the old version, yet still
   referenced `latest`, found their applications broke. We want to avoid this
   at all costs.
2. Our release cadence is more regular, with around two or three releases a
   month. Having transitioned to the new version of PyScript, we aim to avoid
   breaking changes. However, we are refining and adding features as we adapt
   to our users' invaluable feedback.

Therefore,
[pinning your app's version of PyScript to a specific release](https://github.com/pyscript/pyscript/releases)
(rather than `latest`) ensures you get exactly the version of PyScript you
used when writing your code.

However, as we continue to develop PyScript it _is_ possible to get our latest
development version of PyScript via `npm` and we could (should there be enough
interest) deliver our work-in-progress via a CDN's "canary" or "development"
channel. **We do not guarantee the stability of such versions of PyScript**,
so never use them in production, and our documentation may not reflect the
development version.

If you require the development version of PyScript, these are the URLs to use:

```html title="PyScript development. ⚠️⚠️⚠️ WARNING: HANDLE WITH CARE! ⚠️⚠️⚠️"
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@pyscript/core/dist/core.css">
<script type="module" src="https://cdn.jsdelivr.net/npm/@pyscript/core/dist/core.js"></script>
```

!!! warning

    ***Do not use shorter urls or other CDNs.***

    PyScript needs both the correct headers to use workers and to find its own
    assets at runtime. Other CDN links might result into a **broken
    experience**.

### Workers via JavaScript 

Sometimes you want to start a Pyodide or MicroPython web worker from
JavaScript.

Here's how:

```html title="Starting a PyScript worker from JavaScript."
<script type="module">
  // use sourceMap for @pyscript/core or change to a CDN
  import {
    PyWorker, // Pyodide Worker
    MPWorker  // MicroPython Worker
  } from '@pyscript/core';

  const worker = await MPWorker(
    // Python code to execute
    './micro.py',
    // optional details or config with flags
    { config: { sync_main_only: true } }
    //          ^ just as example ^
  );

  // "heavy computation"
  await worker.sync.doStuff();

  // kill the worker when/if needed
  worker.terminate();
</script>
```

```python title="micro.py"
from pyscript import sync

def do_stuff():
  print("heavy computation")

# Note: this reference is awaited in the JavaScript code.
sync.doStuff = do_stuff
```

### JavaScript `Class.new()`

When using Python to instantiate a class defined in JavaScript, one needs to
use the class's `new()` method, rather than just using `Class()` (as in
Python).

Why?

The reason is technical, related to JavaScript's history and its relatively
poor introspection capabilities:

* In JavaScript, `typeof function () {}` and `typeof class {}` produce the
  same outcome: `function`. This makes it **very hard to disambiguate the
  intent of the caller** as both are valid, JavaScript used to use
  `function` (rather than `class`) to instantiate objects, and the class you're
  using may not use the modern, `class` based, idiom.
* In the FFI, the JavaScript proxy has traps to intercept the use of the
  `apply` and `construct` methods used during instantiation. However, because
  of the previous point, it's not possible to be sure that `apply` is meant to
  `construct` an instance or call a function.
* Unlike Python, just invoking a `Class()` in JavaScript (without
  [the `new` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new))
  throws an error.
* Using `new Class()` is invalid syntax in Python. So there is still a need to
  somehow disambiguate the intent to call a function or instantiate a class.
* Making use of the capitalized-name-for-classes convention is brittle because
  when JavaScript code is minified the class name can sometimes change.
* This leaves our convention of `Class.new()` to explicitly signal the intent
  to instantiate a JavaScript class. While not ideal it is clear and
  unambiguous.

### PyScript events

PyScript uses hooks during the lifecycle of the application to facilitate the
[creation of plugins](../user-guide/plugins/).

Beside hooks, PyScript also dispatches events at specific moments in the
lifecycle of the app, so users can react to changes in state:

#### m/py:ready

Both the `mpy:ready` and `py:ready` events are dispatched for every PyScript
related element found on the page. This includes `<script type="py">`,
`<py-script>` or any MicroPython/`mpy` counterpart.

The `m/py:ready` events dispatch **immediately before** the code is executed,
but after the interpreter is bootstrapped.

```html title="A py:ready example."
<script>
    addEventListener("py:ready", () => {
        // show running for an instance
        const status = document.getElementById("status");
        status.textContent = 'running';
    });
</script>
<!-- show bootstrapping right away -->
<div id="status">bootstrapping</div>
<script type="py" worker>
    from pyscript import document

    # show done after running
    status = document.getElementById("status")
    status.textContent = "done"
</script>
```

A classic use case for this event is to recreate the "starting up"
spinner that used to be displayed when PyScript bootstrapped. Just show the
spinner first, then close it once `py:ready` is triggered!

!!! warning

    If using Pyodide on the main thread, the UI will block until Pyodide has
    finished bootstrapping. The "starting up" spinner won't work unless Pyodide
    is started on a worker instead.

#### m/py:done

The `mpy:done` and `py:done` events dispatch after the either the synchronous
or asynchronous code has finished execution.

```html title="A py:done example."
<script>
    addEventListener("py:ready", () => {
        // show running for an instance
        const status = document.getElementById("status");
        status.textContent = 'running';
    });
    addEventListener("py:done", () => {
        // show done after logging "Hello 👋"
        const status = document.getElementById("status");
        status.textContent = 'done';
    });
</script>

<!-- show bootstrapping right away -->
<div id="status">bootstrapping</div>
<script type="py" worker>
    print("Hello 👋")
</script>
```

!!! warning

    If `async` code contains an infinite loop or some orchestration that keeps
    it running forever, then these events may never trigger because the code
    never really finishes.

#### py:all-done

The `py:all-done` event dispatches when all code is finished executing.

This event is special because it depends upon all the MicroPython and Pyodide
scripts found on the page, no matter the interpreter.

In this example, MicroPython waves before Pyodide before the `"everything is
done"` message is written to the browser's console. 

```html title="A py:all-done example."
<script>
    addEventListener("py:all-done", () => {
        console.log("everything is done");
    });
</script>
<script type="mpy" worker>
    print("MicroPython 👋")
</script>
<script type="py" worker>
    print("Pyodide 👋")
</script>
```

### Packaging pointers

Applications need third party packages and [PyScript can be configured to
automatically install packages for you](user-guide/configuration/#packages).
Yet [packaging can be a complicated beast](#python-packages), so here are some
hints for a painless packaging experience with PyScript.

There are essentially four ways in which a third party package can become
available in PyScript.

1. The module is already part of either the Pyodide or MicroPython
   distribution. For instance, Pyodide includes numpy, pandas, scipy,
   matplotlib and scikit-learn as pre-built packages you need only activate
   via the [`packages` setting](../user-guide/configuration/#packages) in
   PyScript. There are plans for MicroPython to offer different builds for
   PyScript, some to include MicroPython's version of numpy or the API for
   sqlite.
2. Host a standard Python package somewhere (such as
   [PyScript.com](https://pyscript.com) or in a GitHub repository) so it can
   be fetched as a package via a URL at runtime.
3. Reference hosted Python source files, to be included on the file
   system, via the [`files` setting](../user-guide/configuration/#files).
4. Create a folder containing the package's files and sub folders, and create
   a hosted `.zip` or `.tgz`/`.tar.gz` archive to be decompressed into the file
   system (again, via the
   [`files` setting](../user-guide/configuration/#files)).

#### Host a package

Just put the package you need somewhere it can be served (like
[PyScript.com](https://pyscript.com/)) and reference the URL in the
[`packages` setting](../user-guide/configuration/#packages). So long as the
server at which you are hosting the package
[allows CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
(fetching files from other domains) everything should just work.

It is even possible to install such packages at runtime, as this example using
MicroPython's [`mip` tool](https://docs.micropython.org/en/latest/reference/packages.html)
demonstrates (the equivalent can be achieved with Pyodide
[via `micropip`](https://micropip.pyodide.org/en/stable/)).

```python title="MicroPython mip example."
# Install default version from micropython-lib
mip.install("keyword")

# Install from raw URL
mip.install("https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/bisect/bisect.py")

# Install from GitHub shortcut
mip.install("github:jeffersglass/some-project/foo.py")
```

#### Provide your own file

One can use the [`files` setting](../user-guide/configuration/#files) to copy
packages onto the Python path:

```html title="A file copied into the Python path."
<mpy-config>
[files]
"./modules/bisect.py" = "./bisect.py"
</mpy-config>
<script type="mpy">
  import bisect
</script>
```

#### Code archive (`zip`/`tgz`) 

Compress all the code you want into an archive (using either either `zip` or
`tgz`/`tar.gz`). Host the resulting archive and use the
[`files` setting](../user-guide/configuration/#files) to decompress it onto
the Python interpreter's file system.

Consider the following file structure:

```
my_module/__init__.py
my_module/util.py
my_module/sub/sub_util.py
```

Host it somewhere, and decompress it into the home directory of the Python
interpreter:

```html title="A code archive."
<mpy-config>
[files]
"./my_module.zip" = "./*"
</mpy-config>

<script type="mpy">
  from my_module import util
  from my_module.sub import sub_util
</script>
```

Please note, the target folder must end with a star (`*`), and will contain
everything in the archive. For example, `"./*"` refers to the home folder for
the interpreter.

### File System

Python expects a file system. In PyScript each interpreter provides its own
in-memory **virtual** file system. **This is not the same as the filesystem
on the user's device**, but is simply a block of memory in the browser.

!!! warning 

    **The file system is not persistent nor shareable** (yet).

    Every time a user loads or stores files, it is done in ephemeral memory
    associated with the current browser session. Beyond the life of the
    session, nothing is shared, nothing is stored, nothing persists!

#### Read/Write

The easiest way to add content to the virtual file system is by using native
Python file operations:

```python title="Writing to a text file."
with open("./test.txt", "w") as dest:
    dest.write("hello vFS")
    dest.close()

# Read and print the written content.
with open("./test.txt", "r") as f:
    content = f.read()
    print(content)
```

Combined with our `pyscript.fetch` utility, it's also possible to store more
complex data from the web.

```python title="Writing a binary file."
# Assume an `async` attribute / execution.
from pyscript import fetch, window

href = window.location.href

with open("./page.html", "wb") as dest:
    dest.write(await fetch(href).bytearray())

# Read and print the current HTML page.
with open("./page.html", "r") as source:
    print(source.read())
```

#### Upload

It's possible to upload a file onto the virtual file system from the browser
(`<input type="file">`), and using the DOM API.

The following fragment is just one way to achieve this. It's very simple and
builds on the file system examples already seen.

```html title="Upload files onto the virtual file system via the browser."
<!-- Creates a file upload element on the web page. -->
<input type="file">

<!-- Python code to handle file uploads via the HTML input element. -->
<script type="mpy">
    from pyscript import document, fetch, window

    async def on_change(event):
        # For each file the user has selected to upload...
        for file in input.files:
            # create a temporary URL,
            tmp = window.URL.createObjectURL(file)
            # fetch and save its content somewhere,
            with open(f"./{file.name}", "wb") as dest:
                dest.write(await fetch(tmp).bytearray())
            # then revoke the tmp URL.
            window.URL.revokeObjectURL(tmp)

    # Grab a reference to the file upload input element and add
    # the on_change handler (defined above) to process the files.
    input = document.querySelector("input[type=file]")
    input.onchange = on_change
</script>
```

#### Download

It is also possible to create a temporary link through which you can download
files present on the interpreter's virtual file system.


```python title="Download file from the virtual file system."
from pyscript import document, ffi, window
import os


def download_file(path, mime_type):
    name = os.path.basename(path)
    with open(path, "rb") as source:
        data = source.read()

        # Populate the buffer.
        buffer = window.Uint8Array.new(len(data))
        for pos, b in enumerate(data):
            buffer[pos] = b
        details = ffi.to_js({"type": mime_type})

        # This is JS specific
        file = window.File.new([buffer], name, details)
        tmp = window.URL.createObjectURL(file)
        dest = document.createElement("a")
        dest.setAttribute("download", name)
        dest.setAttribute("href", tmp)
        dest.click()

        # here a timeout to window.URL.revokeObjectURL(tmp)
        # should keep the memory clear for the session
```

### create_proxy

The `create_proxy` function is described in great detail
[on the FFI page](../ffi/), but it's also useful to explain _when_
`create_proxy` is needed and the subtle differences between Pyodide and
MicroPython.

#### Background

To call a Python function from JavaScript, the native Python function needs
to be wrapped in a JavaScript object that JavaScript can use. This JavaScript
object converts and normalises arguments passed into the function before
handing off to the native Python function. It also reverses this process with
any results from the Python function, and so converts and normalises values
before returning the result to JavaScript.

The JavaScript primitive used for this purpose is the
[Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy).
It enables "traps", such as
[apply](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy/apply),
so the extra work required to call the Python function can happen.

Once the `apply(target, self, args)` trap is invoked:

* JavaScript must find the correct Python interpreter to evaluate the code.
* In JavaScript, the `self` argument for `apply` is probably ignored for most
  common cases.
* All the `args` must be resolved and converted into their Python primitive
  representations or associated Python objects.

Ultimately, the targets referenced in the `apply` **must exist** in the Python
context so they are ready when the JavaScript `apply` method calls into the
Python context.

**Here's the important caveat**: locally scoped Python functions, or functions
created at run time cannot be retained forever.

```python title="A basic Python to JavaScript callback."
import js

js.addEventListener(
  "custom:event",
  lambda e: print(e.type)
)
```

In this example, the anonymous `lambda` function has no reference in the Python
context. It's just delegated to the JavaScript runtime via `addEventListener`,
and then Python immediately garbage collects it. However, as previously
mentioned, such a Python object must exist for when the `custom:event` is
dispatched.

Furthermore, there is no way to define how long the `lambda` should be kept
alive in the Python environment, nor any way to discover if the `custom:event`
callback will ever dispatch (so the `lambda` is forever pending). PyScript, the
browser and the Python interpreters can only work within a finite amount of
memory, so memory management and the "aliveness" of objects is important.

Therefore, `create_proxy` is provided to delegate responsibility for the
lifecycle of an object to the author of the code. In other words, wrapping the
`lambda` in a call to `create_proxy` would ensure the Python interpreter
retains a reference to the anonymous function for future use.

!!! info 

    This probably feels strange! An implementation detail of how the Python
    and JavaScript worlds interact with each other is bleeding into your code
    via `create_proxy`. Surely, if we always just need to create a proxy, a
    more elegant solution would be to do this automatically?

    As you'll see, this is a complicated situation with inevitable tradeoffs,
    but ultimately, through the
    [`experimental_create_proxy = "auto"` flag](../user-guide/configuration/#experimental_create_proxy),
    you probably never need to use `create_proxy`. This section of
    our docs gives you the context you need to make an informed decision.

**However**, this isn't the end of the story.

When a Python callback is attached to a specific JavaScript
instance (rather than passed as argument into an event listener), it is easy
for the Python interpreter to know when the function could be freed from the
memory.

```python title="A sticky lambda."
from pyscript import document

# logs "click" if nothing else stopped propagation
document.onclick = lambda e: print(e.type)
```

"**Wait, wat? This doesn't make sense at all!?!?**", is a valid
question/response to this situation.

In this case there's
no need to use `create_proxy` because the JavaScript reference to which the
function is attached isn't going away and the interpreter can use the
[`FinalizationRegistry`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry)
to destroy the `lambda` (or decrease its reference count) when the underlying
JavaScript reference to which it is attached is itself destroyed.

#### In Pyodide

The `create_proxy` utility was created
([among others](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#module-pyodide.ffi.wrappers))
to smooth out and circumvent the afore mentioned memory issues when using
Python callables with JavaScript event handlers.

Using it requires special care. The coder must invoke the `destroy()` method
when the Python callback is no longer needed. It means coders must track the
callback's lifecycle. But this is not always possible:

* If the callback is passed into opaque third party libraries, the reference is
  "lost in a limbo" where who-knows-when the reference should be freed.
* If the callback is passed to listeners, timers or promises it's hard to
  predict when the callback is no longer needed.

Luckily the `Promise` use case is automatically handled by Pyodide, but we're
still left with the other cases:

```python title="Different Pyodide create_proxy contexts."
from pyscript import ffi, window

# The create_proxy is needed when a Python
# function isn't attached to an object reference
# (but is, rather, an argument passed into
# the JavaScript context).

# This is needed so a proxy is created for
# future use, even if `print` won't ever need
# to be freed from the Python runtime.
window.setTimeout(
  ffi.create_proxy(print),
  100,
  "print"
)

# This is needed because the lambda is
# immediately garbage collected.
window.setTimeout(
  ffi.create_proxy(
    lambda x: print(x)
  ),
  100,
  "lambda"
)

def print_type(event):
    print(event.type)

# This is needed even if `print_type`
# is not a scoped / local function.
window.addEventListener(
  "some:event",
  ffi.create_proxy(print_type),
  # despite this intent, the proxy
  # will be trapped forever if not destroyed
  ffi.to_js({"once": True})
)

# This does NOT need create_function as it is
# attached to an object reference, hence observed to free.
window.Object().no_create_function = lambda: print("ok")
```

To simplify this complicated situation PyScript has an
`experimental_create_proxy = "auto"` flag. When set, **PyScript intercepts
JavaScript callback invocations, such as those in the example code above, and
automatically proxies and destroys any references that are garbage collected
in the JavaScript environment**.

**When this flag is set to `auto` in your configuration, you should never need
to use `create_proxy` with Pyodide**.

!!! Note

    When it comes code running on a web worker, due to the way browser work, no
    Proxy can survive a round trip to the main thread and back.

    In this scenario PyScript works differently and references callbacks
    via a unique id, rather than by their identity on the worker. When running
    on a web worker, PyScript automatically frees proxy object references, so
    you never need to use `create_proxy` when running code on a web worker.

#### In MicroPython

The proxy situation is definitely simpler in MicroPython. It just creates
proxies automatically (so there is no need for a manual `create_proxy` step).

This is because MicroPython doesn't (yet) have a `destroy()` method for
proxies, rendering the use case of `create_proxy` redundant.

Accordingly, **the use of `create_proxy` in MicroPython is only needed for
code portability purposes** between Pyodide and MicroPython. When using
`create_proxy` in MicroPython, it's just a pass-through function and doesn't
actually do anything.

All the examples that require `create_proxy` in Pyodide, don't need it in
MicroPython:

```python title="Different MicroPython create_proxy contexts."
from pyscript import window

# This just works.
window.setTimeout(print, 100, "print")

# This also just works.
window.setTimeout(lambda x: print(x), 100, "lambda")

def print_type(event):
    print(event.type)

# This just works too.
window.addEventListener(
  "some:event",
  print_type,
  ffi.to_js({"once": True})
)

# And so does this.
window.Object().no_create_function = lambda: print("ok")
```

### to_js

Use of the `pyodide.ffi.to_js` function is described
[in the ffi page](../user-guide/ffi/#to_js).
But it's also useful to cover the *when* and *why* `to_js` is needed, if at
all.

#### Background

Despite their apparent similarity,
[Python dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
and
[JavaScript object literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects)
are very different primitives:

```python title="A Python dictionary."
ref = {"some": "thing"}

# Keys don't need quoting, but only when initialising a dict...
ref = dict(some="thing")
```

```js title="A JavaScript object literal."
const ref = {"some": "thing"};

// Keys don't need quoting, so this is as equally valid...
const ref = {some: "thing"};
```

In both worlds, accessing `ref["some"]` would produce the same result: the
string `"thing"`.

However, in JavaScript `ref.some` (i.e. a dotted reference to the key) would
also work to return the string `"thing"` (this is not the case in Python),
while in Python `ref.get("some")` achieves the same result (and this is not the
case in JavaScript).

Perhaps because of this, Pyodide chose to convert Python dictionaries to
JavaScript
[Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
objects that share a
[`.get` method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/get)
with Python.

Unfortunately, in idiomatic JavaScript and for the vast majority of APIs, 
an object literal (rather than a `Map`) is used to represent key/value pairs.
Feedback from our users indicates the dissonance of using a `Map` rather than
the expected object literal to represent a Python `dict` is the source of a
huge amount of frustration. Sadly, the APIs for `Map` and object literals
are sufficiently different that one cannot be a drop in replacement for
another.

Pyodide have provided a way to override the default `Map` based behaviour, but
this results some rather esoteric code:

```python title="Convert a dict to an object literal in Pyodide."
import js
from pyodide.ffi import to_js

js.callback(
    to_js(
        {"async": False},
        # Transform the default Map into an object literal.
        dict_converter=js.Object.fromEntries
    )
)
```

In addition, MicroPython's version of `to_js` takes the opposite approach (for
many of the reasons stated above) and converts Python dictionaries to object
literals instead of `Map` objects.

As a result, **the PyScript `pyscript.ffi.to_js` ALWAYS returns a JavaScript
object literal by default when converting a Python dictionary** no matter if
you're using Pyodide or MicroPython as your interpreter.

#### Caveat

!!! warning

    **When using `pyscript.to_js`, the result is detached from the original
    Python dictionary.**

Any change to the JavaScript object **will not be reflected in the original
Python object**. For the vast majority of use cases, this is a desirable
trade-off. But it's important to note this detachment.

If you're simply passing data around, `pyscript.ffi.to_js` will fulfil your
requirements in a simple and idiomatic manner.
