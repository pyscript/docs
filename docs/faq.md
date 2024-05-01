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

When reading an error message, the easy way to find out what's going on is,
most of the time, to read the last line of the error.

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
because the object with the name `failure` did not exist.

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
  to instantiate a JavaScript class. While not idea it is clear and
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

#### Code archive (`zip` / `tgz`) 

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

The first thing to understand about *PyScript* File System operations is that each interpreter provides *its own* *Virtual File System* that works **only in memory**.

!!! Note

    We don't have yet a way to provide a shared, user's browser persistent, File System, so that any time we load or store and then read files we're doing that through the *RAM* and the current session: nothing is shared, nothing is stored, nothing persists!

#### Read/Write Content

The easiest way to add content to the virtual *FS* is by using native *Python* files operations:

```python title="Writing to a text file"
with open("./test.txt", "w") as dest:
    dest.write("hello vFS")
    dest.close()

# read the written content
source = open("./test.txt", "r")
print(source.read())
source.close()
```

Combined with our `pyscript.fetch` utility, it's also possible to store from the web more complex data.

```python title="Writing file as binary"
# assume an `async` attribute / execution
from pyscript import fetch, window

href = window.location.href

with open("./page.html", "wb") as dest:
    dest.write(await fetch(href).bytearray())
    dest.close()

# read the current HTML page
source = open("./page.html", "r")
print(source.read())
source.close()
```

#### Upload Content

Through the DOM API it's possible to also upload a file and store it into the virtual *FS*.

The following example is just one of the ways one can do that, but it's a pretty simple one and based on the very same code and logic already seen in the previous paragraph:

```html title="Upload file into vFS"
<input type="file">
<script type="mpy">
    from pyscript import document, fetch, window

    async def on_change(event):
        # per each file
        for file in input.files:
            # create a temporary URL
            tmp = window.URL.createObjectURL(file)
            # fetch and save its content somewhere
            with open(f"./{file.name}", "wb") as dest:
                dest.write(await fetch(tmp).bytearray())
                dest.close()
            # revoke the tmp URL
            window.URL.revokeObjectURL(tmp)

    input = document.querySelector("input[type=file]")
    input.onchange = on_change
</script>
```

#### Download Content

Once a file is present in the virtual File System, it's always possible to create a temporary link which goal is to download such file:

```python title="Download file from vFS"
def download_file(path, mime_type):
    from pyscript import document, ffi, window
    import os
    name = os.path.basename(path)
    with open(path, "rb") as source:
        data = source.read()

        # this is Pyodide specific
        buffer = window.Uint8Array.from_(data)
        details = ffi.to_js({"type": mime_type})

        # this is JS specific
        file = window.File.new([buffer], name, details)
        tmp = window.URL.createObjectURL(file)
        dest = document.createElement("a")
        dest.setAttribute("download", name)
        dest.setAttribute("href", tmp)
        dest.click()

        # here a timeout to window.URL.revokeObjectURL(tmp)
        # should keep the memory clear for the session
```

!!! warning

    The presented utility works only on *Pyodide* at the moment, as there is no `from_` or `assign` convention in *MicroPython*. Once this is fixed or a better example is discovered the example will be updated too so that all of them should work in both interpreters.

### create_proxy

Explained in details [in the ffi page](../ffi/), it's probably useful to cover the *when* `create_proxy` is needed at all.

To start with, there's a subtle difference between *Pyodide* and *MicroPython* around this topic, with or without using our `pyscript.ffi`, as it just forwards the utility behind scene.

##### Background

A *Python* function executed in the *JS* world inevitably needs to be wrapped in a way that, once executed, both its native (*Python*) function reference and any passed argument/parameter to such function can be normalized to *Python* references before such invocation happens.

The *JS* primitive to do so is the [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) one, which enables "*traps*" such as [apply](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy/apply) to do extra work before any result is actually returned from such invocation.

Once the `apply(target, self, args)` trap is invoked:

  * the interpreter must find which `target` in the current *WASM* running code that needs to be invoked
  * the `self` context for regular functions is likely ignored for common cases, but it's likely desired to eventually define `python.method()` invokes when these happen in the *JS* world
  * the `args` is a list of passed arguments where any proxy coming from *Python* must be resolved as reference, any primitive might be eventually converted into its *Python* primitive representation, if needed, and any *JS* reference must be translated into *Python* like objects / references

This orchestration might feel convoluted for many or obvious for others, yet the detail behind the scene is that such `target` reference *needs to exist* on the *WASM* runtime in order to be executed when the *JS* world asks for it ... so here the caveat: globally available functions might outlive any *JS* runtime interoperability in the *WASM* world but locally scoped or runtime functions cannot be retained forever!

```python title="A basic Python to JS callback"
import js

js.addEventListener(
  "custom:event",
  lambda e: print(e.type)
)
```

In this scenario that `lambda` has no meaning or references in the running *Python* code, it's just delegated to the *JS* runtime / environment but it *must exist* whenever that `custom_event` is dispatched, hence triggered, or emitted, in the *JS* world.

From a pure architectural point of view there is literally nothing that defines in that user explicit intent how long that `lambda` should be kept alive in the current *Python* program while from the *JS* point of view that callback might never even be needed or invoked (i.e. the `custom:event` never happens ... which is a forever pending *lambda* use case).

Because all interpreters do care about memory consumption and have some *WASM* memory constrain to deal with, `create_proxy` (or any similar API) has been provided to delegate the responsibility to kill those references to the user, specially for unknown, in time, invocations scenarios like the one described in here.

**On the other hand**, when a *Python* callback is attached, as opposite of being just passed as argument, to a specific foreign instance, it is fairly easy for the *WASM* runtime to know when such `lambda` function, or any other non global function, could be freed from the memory.

```python title="A sticky lambda"
from pyscript import document

# logs "click" if nothing else stopped propagation
document.onclick = lambda e: print(e.type)
```

"*How is that easy?*" is a valid question and the answer is that if the runtime has *JS* bindings, hence it's capable of dealing with *JS* references, that `document` would be a well known *JSProxy* that points to some underlying *JS* reference.

In this case there's usually no need to use `create_proxy` because that reference is well understood and the interpreter can use the *FinalizationRegistry* to simply destroy that lambda, or decrease its reference counting, whenever the underlying *JS* reference is not needed anymore, hence finalized after its own release from *JS*.

Sure thing this example is fairly poor, because a `document` reference in the *JS* world would live "*forever*", but if instead of a `document` there was a live DOM element, as soon as that element gets replaced and it's both not live or referenced anymore, the *FinalizationRegistry* would inform the *WASM* based runtime that such reference is gone, and whatever was attached to it behind the scene can be gone too.

#### In Pyodide

The `create_proxy` utility is exported [among others](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#module-pyodide.ffi.wrappers) to smooth out and circumvent memory leaks in the long run.

Using it separately from other utilities though requires some special care, most importantly, it requires that the user invokes that `destroy()` method when such callback is not needed anymore, hence it requires users to mentally track callbacks lifecycle, but that's not always possible for at least these reasons:

  * if the callback is passed to 3rd party libraries, the reference is kinda "*lost in a limbo*" where who knows when that reference could be actually freed
  * if the callback is passed to listeners or timers, or even promises based operations, it's pretty unpredictable and counter intuitive, also a bad *DX*, to try to track those cases

Luckily enough, the *Promise* use case is automatically handled by *Pyodide* runtime, but we're left with other cases:

```python title="Pyodide VS create_proxy"
from pyscript import ffi, window

# this is needed even if `print` won't ever need
# to be freed from the Python runtime
window.setTimeout(
  ffi.create_proxy(print),
  100,
  "print"
)

# this is needed not because `print` is used
# but because otherwise the lambda is gone
window.setTimeout(
  ffi.create_proxy(
    lambda x: print(x)
  ),
  100,
  "lambda"
)

def print_type(event):
    print(event.type)

# this is needed even if `print_type`
# is not a scoped / local function, rather
# a never freed global reference in this Python code
window.addEventListener(
  "some:event",
  ffi.create_proxy(print_type),
  # despite this intent, the proxy
  # will be trapped forever if not destroyed
  ffi.to_js({"once": True})
)

# this does NOT need create_function as it is
# attached to an object reference, hence observed to free
window.Object().no_create_function = lambda: print("ok")
```

To simplify some of this orchestration we landed the `experimental_create_proxy = "auto"` flag which goal is to intercept *JS* world callbacks invocation, and automatically proxy and destroy any proxy that is not needed or used anymore in the *JS* environment.

Please give it a try and actually try to *not* ever use, or need, `create_proxy` at all, and tell us when it's needed instead, than you!

!!! Note

    When it comes to *worker* based code, no *Proxy* can survive a roundtrip to the *main* thread and back.
    In this scenario we inevitably need to orchestrate the dance differently and reference instead *Python* callbacks, or een *JS* one, as these travel by their unique *id*, not their identity on the *worker*.
    We orchestrate the *free* dance automatically because nothing would work otherwise so that long story short, if your *pyodide* code runs from a *worker*, you likely never need to use `create_proxy` at all.

#### In MicroPython

Things are definitively easier to reason about in this environment, but mostly because it doesn't expose (yet?) a `destroy()` utility for created proxies.

Accordingly, using `create_proxy` in *micropython* might be needed only to have portable code, as proxies are created anyway when *Python* code refers to a callback and is passed to any *JS* utility, plus proxies won't be created multiple times if these were already proxy of some *Python* callback.

All the examples that require `create_proxy` in *Pyodide*, won't bother *MicroPython* but these would be also kinda not needed in general.

```python title="MicroPython VS create_proxy"
from pyscript import window

# this works
window.setTimeout(print, 100, "print")

# this also works
window.setTimeout(lambda x: print(x), 100, "lambda")

def print_type(event):
    print(event.type)

# this works too
window.addEventListener(
  "some:event",
  print_type,
  ffi.to_js({"once": True})
)

# and so does this
window.Object().no_create_function = lambda: print("ok")
```

!!! Note

    Currently *MicroPython* doesn't provide a `destroy()` method so it's actually preferred, in *MicroPython* projects, to not use or need the `create_proxy` because it lacks control over destroying it while it's up to the interpreter to decide when or how proxies can be destroyed.

### to_js

Also xplained in details [in the ffi page](../ffi/), it's probably useful to cover the *when* `to_js` is needed at all.

##### Background

Despite their similar look on the surface, *Python* dictionaries and *JS* object literals are very different primitives:

```python title="A Python dict"
ref = {"some": "thing"}
```

```js title="A JS literal"
const ref = {some: "thing"};
// equally valid as ...
const ref = {"some": "thing"};
```

In both worlds accessing `ref["some"]` would also produce the same result: pointing at `"value"` string as result. However, in *JS* `ref.some` would also return the very same `"value"` and while in *Python* `ref.get("some")` would do the same, some interpreter preferred to map dictionaries to *JS* [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) instead, probably because [Map.get](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/get) is really close to what *Python* dictionaries expect.

Long story short, *Pyodide* opted for that default conversion but unfortunately all *JS* APIs are usually expecting object literals, and *JS* maps don't really work seamlessly the same, so that it's possible to define a different `dict_converter` in *Pyodide*, but that definition is verbose and not too *DX* friendly:

```python title="A common Pyodide converter"
import js
from pyodide.ffi import to_js

js.callback(
    to_js(
        {"async": False},
        # transform a Map into an object literal
        dict_converter=js.Object.fromEntries
    )
)
```

Beside the fact that *MicroPython* `to_js` implementation already converts, by default, *Python* dictionaries to *JS* literal, after some experience with common use cases around *Python* and *JS* interoperability, we decided to automatically provide an `ffi` that always results into a *JS* object literal, so that no converter, unless explicitly defined, would be needed to have the desired result out of the box.

#### Caveats

One fundamental thing to consider when `to_js` is used, is that it detaches the created reference from its original "*source*", in this case the *Python* dictionary, so that any change applied elsewhere to such reference won't ever be reflected to its original counterpart.

This is probably one of the main reasons *Pyodide* sticked with the dictionary like proxy when it passes its reference to *JS* callbacks but at the same time no *JS* callback usually expect a foreign runtime reference to deal with, being this a *Python* one or any other programming language.

Accordingly, if your *JS* code is written to explicitly target *Pyodide* kind of proxies, you probably never need to use `to_js` as that won't reflect changes to the *Python* runtime, if changes ever happen within the callback receiving such reference, but if you are just passing *data* around, data that can be represented as *JSON*, as example, to configure or pass some option argument to *JS*, you can simply use our `pyscript.ffi.to_js` utility and forget about all these details around the conversion: dictionaries will be object literals and lists or tuples will be arrays, that's all you need to remember!
