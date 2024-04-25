# F.A.Q.

This page contains most common questions and "*gotchas*" asked in [our Discord channel](https://discord.com/channels/972017612454232116/972017612454232119) or within our community.

There are two major areas we'd like to help with, grouped here as [common errors](#common-errors) and as [common hints](#common-hints).

## Common Errors

This area contains most common issues our users might face due technical reasons or some misconception around the topic.

### SharedArrayBuffer

This is not by accident the very first, and most common, error our users might encounter while developing or deploying *PyScript* projects.

!!! failure

    Unable to use SharedArrayBuffer due insecure environment.
    Please read requirements in MDN: ...

The error contains [a link to MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer#security_requirements) but it's easy to get lost behind the amount of content provided by this topic.

**When**

This errors happens in one of these combined scenarios:

  * the server doesn't provide the correct headers to handle security concerns or there is no *Service Worker* able to override headers, as described [in the worker page](http://127.0.0.1:8000/user-guide/workers/) and ...
    * there is a `worker` attribute in the *py* or *mpy* script element and the [sync_main_only](https://pyscript.github.io/polyscript/#extra-config-features) flag is not present or not `True`
    * there is a `<script type="py-editor">` that uses a *worker* behind the scene
    * there is an explicit *PyWorker* or *MPWorker* bootstrap

The only exception is when the `sync_main_only = True` is part of the config with the following caveats:

  * it is not possible to manipulate the DOM or do anything meaningful on the main thread directly because *Atomics* cannot guarantee sync-like locks within *worker* ↔ *main* operations
  * the only desired use case is to expose, from the worker, `pyscript.sync` utilities that will need to be awaited from the *main* once invoked
  * the worker can only *await* main related references, one after the other, so that *DX* is really degraded in case one still needs to interact with main

If your project simply bootstraps on the *main* thread, none of this is relevant because no *worker* would need special features.

**Why**

The only way to make `document.getElementById('some-id').value` work out of a *worker* execution context is to use these two JS primitives:

  * **SharedArrayBuffer**, which allows multiple threads to read and / or write into a chunk of memory that is, like the name suggests, shared across threads
  * **Atomics**, which is needed to both `wait(sab, index)` and `notify(sab, index)` to unlock the awaiting thread

While a *worker* is waiting for some operation on main to happen, this is not using the CPU, it just idles until that index of the shared buffer gets notified, effectively never blocking the *main* thread, still pausing its own execution until such buffer is notified for changes.

As overwhelming or complicated as this might sounds, these two fundamental primitives make *main* ↔ *worker* interoperability an absolute wonder in term of *DX* so that we encourage to always prefer *workers* over *main* scripts, specially when it comes to *Pyodide* related projects with its heavier bootstrap or computation abilities, yet still delivering a *main-like* development experience.

Unfortunately, due past security concerns and attacks to shared buffers, each server or page needs to allow extra security to prevent malicious software to also read or write into these buffers but be assured that if you own your code, your project, and you trust the modules or 3rd party code you need and use, **there are no security concerns around this topic within this project**, it's simply an unfortunate "*one rule catch all*" standard any server can either enable or disable as it pleases.

### Borrowed Proxy

This is another classic error that might happen with listeners, timers or any other circumstance where a *Python* callback might be lazily invoked in the *JS* side of affair:

!!! failure

    Uncaught Error: This borrowed proxy was automatically destroyed at the end of a function call. Try using create_proxy or create_once_callable.
    For more information about the cause of this error, use `pyodide.setDebug(true)`

**When**

This error usually happens in *Pyodide* only related project, and only if a *Python* callback has been directly passed along as *JS* function parameter:

```python title="An expired borrowed proxy example"
import js
# will throw the error in case
js.setTimeout(lambda msg: print(msg), 1000, "FAIL")
```

Please note that this error *does not happen* if the code is executed in a worker and the *JS* reference comes from the *main* thread:

```python title="A worker has no borrowed issue"
from pyscript import window
window.setTimeout(lambda x: print(x), 1000, "OK")
```

In this case, because proxies cannot survive a *worker* ↔ *main* communication, the *Python* reference gets inevitably translated into a *JS* function and its unique *id* propagated and awaited to be released with a returning value, so that technically that lambda can be freed without causing any issue.

We provided an experimental way to always act in a similar way on both main and workers through the `experimental_create_proxy = "auto"` *config* flag.

This flag tries to intercept all *Python* proxies passed to a *JS* callback and it orchestrates an automatic memory free operation through the *JS* garbage collector.

!!! Note

    The [FinalizationRegistry](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry) is the primitive used to do so. It is not observable and nobody can predict when it will run to free, hence destroy, retained *Python* proxies. This means that *RAM* consumption might be slightly higher, but it's the *JS* engine responsibility to guarantee that when such *RAM* consumption is too high, that finalization registry would call and free all retained proxies, leaving room for more *RAM*.

**Why**

Most *WASM* based runtimes have their own garbage collector or memory management but when their references are passed along another programming language they cannot guarantee these references will ever be freed, or better, they lose control over that memory allocation because they cannot know when such allocation won't be needed anymore.

The theoretical solution to this is to allow users to explicitly create proxies of these references and then still explicitly invoke `proxy.destroy()` to communicate to the original *PL* that such reference and allocated can be freed, if not used internally for other reasons, effectively invalidating that *JS* reference, resulting into a "*dead reference*" that its garbage collector might get rid of when it's convenient.

At the practical level though, there are dozen use cases where users just don't, or can't, disambiguate the need for such proxy creation or easily forget to call `destroy()` at the right time.

To help most common use cases, *Pyodide* provide various [ffi.wrappers](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#module-pyodide.ffi.wrappers) but in theory none of these is strictly needed if we orchestrate a *FinalizationRegistry* to automatically `destroy` those proxies when not needed anymore, moving the responsibility from the user to the running *JS* engine, which is why we have provided the `experimental_create_proxy = "auto"` *config* flag.

### Python Modules

There is a huge difference in what can be imported in *pyodide* VS what can be imported in *micropython* and the reason is:

  * *pyodide* can import modules at runtime as long as these [have been ported](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) to it
  * *micropython* can only import at runtime *Python* only modules, or better, modules that use the same syntax and primitives allowed in *micropython* itself

Behind the scene *pyodide* uses [micropip](https://github.com/pyodide/micropip) while *micropython* uses [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip).

Due different architecture though, *micropython* cannot expose modules that require native compilation / translation for the resulting *WASM* artifact, but we're working on a "*super charged*" version of *micropython* that would bring at least the most common requested modules too (i.e. *numpy*).

!!! warning

    Accordingly to the current state, it could be hard to seamlessly port 1:1 a Pyodide project to MicroPython: expect possible issues while trying but please consider the mentioned caveats around or be sure the issue is something we could actually fix on our side or file an upstream issue otherwise, thank you!

### JS Modules

In more than one occasion, since we introduced the `pyscript.js_modules` feature, our users have encountered errors like:

!!! failure

    Uncaught SyntaxError: The requested module './library.js' does not provide an export named 'default'

!!! failure

    Uncaught SyntaxError: The requested module './library.js' does not provide an export named 'util'

**When**

99% of the time the issue with JS modules is that what we are importing are not, effectively, JS modules.

When the file uses `module.exports` or `globalThis.util` or anything that is not standard *ECMAScript* syntax for modules, such as `export default value` or `export const util = {}`, we cannot retrieve that file content in a standard way.

To **solve** this issue various *CDNs* provide a way to automatically deliver *ESM* (aka: *ECMAScript Modules*) out of the box and one of the most reliable and famous one is [esm.run](https://esm.run/).

```html title="An example of esm.run"
<mpy-config>
[js_modules.main]
"https://esm.run/d3" = "d3"
</mpy-config>
<script type="mpy">
  from pyscript.js_modules import d3
</script>
```

Alternatively, please be sure any `.js` file you are importing as module actually uses `export ...` within its content and, if that's not the case, ask for an `.mjs` counter-equivalent of that library or framework or trust `esm.run` produced artifacts.

**Why**

Even if standard *JS* modules have been around since 2015, a lot of old to even new libraries still produce files that are incompatible with modern *JS* expectations.

There is no logical or simple explanation to this situation for modules that target browsers, but there are various server side related projects that still rely on the legacy, *NodeJS* only, module system (aka: *CommonJS*).

Until that legacy module system exists, be aware some module might require special care.

### Reading Errors

Each interpreter might provide different error messages but the easy way to find what's going on is, most of the time, described in the last line with both *Pyodide* and *MicroPython*:

```text title="A Pyodide Error"
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

```text title="A MicroPython Error"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'failure' isn't defined
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The same applies when the error is shown in devtools/console where unfortunately the stack right after the error message might be a bit distracting but it's still well separated from the error message itself.

## Common Hints

This area contains most common questions, hacks, or hints we provide to the community.

!!! Note

    We have a lovely *PyScript* contributor, namely [Jeff Glass](https://github.com/jeffersglass), who is maintaining an awesome blog full of [PyScript Recipes](https://pyscript.recipes/) with even more use cases and solutions. If you cannot find what you are looking for in here, please do check over there as it's very likely there is something close to the answer you are looking for.

### PyScript latest

For various reasons previously discussed at length, we decided to remove our `latest` channel from our own CDN.

We were not super proud of users trusting that channel coming back with suddenly broken projects so we now [release only official versions](https://github.com/pyscript/pyscript/releases) everyone can pin-point in time.

We are also developing behind the scene through *npm* to be able to test in the wild breaking changes and whatnot and it's no secret that *CDNs* could also deliver our "*canary*" or "*development*" channel so that we're better off telling you exactly which links one should use to have the latest, whenever latest lands on the *CDN* which is usually within 24 hours from the last *npm* version change.

We still **do not guarantee any stability** around this channel so be aware this is never a good idea to use in production, documentation might lack behind landed changes, APIs might break or change too, and so on.

If you are still reading though, this is the template to have *latest*:

```html title="PyScript latest"
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@pyscript/core/dist/core.css">
<script type="module" src="https://cdn.jsdelivr.net/npm/@pyscript/core/dist/core.js"></script>
```

!!! warning

    Do not use shorter urls or other CDNs because the project needs both the correct headers to eventually run in *workers* and it needs to find its own assets at runtime so that other CDN links might result into a **broken experience** out of the box.

### Worker Bootstrap

In some occasion users asked to bootstrap a *pyodide* or *micropython* worker directly via *JS*.

```html title="PyScript Worker in JS"
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

sync.doStuff = do_stuff
```

### About Class.new

In more than one occasion users asked why there's the need to write `Class.new()`, when the class comes from the *JS* world, as opposite of just typing `Class()` like it is for *Python*.

The reason is very technical and related to *JS* history and poor introspection ability in this regard:

  * `typeof function () {}` and `typeof class {}` produce the same outcome: **function**, making it very hard to disambiguate the intention as both are valid and, strawberry on top, legacy *JS* used `function` to create instances, not `class`, so that legacy code might still use that good'ol convention
  * the *JS* proxy has `apply` and `construct` traps but because of the previous point, it's not possible to be sure that `apply` meant to `construct` the instance
  * diffrently from *Python*, just invoking `Class()` throws an error in *JS* if that is actually defined as `class {}` so that `new` is mandatory in the that case
  * the `new Class()` is invalid syntax in *Python*, there is a need to disambiguate the intent
  * the capitalized naming convention is lost once the code gets minified on the *JS* side, hence it's unreliable as convention
  * the `Class.new()` explicitly describe the intent ... it's true that it's ugly, when mixed up with *Python* classes too, but at least it clearly indicates that such `Class` is a *JS* one, not a *Python* thing

As summary, we all agree that in an ideal world just having `Class()` all over would be cool, but unless the *JS* code has been created via quite outdated artifacts we need to use the `.new()` convention which is adopted by both *pyodide* and *micropython*.

To close this paragraph, here an example of how it was possible before to avoid `new` *VS* now:

```js title="Legacy VS Modern JS"
// legacy pseudo pattern: it allows just Legacy()
// with or without `new Legacy` requirement
function Legacy(name) {
  if (!(this instanceof Legacy))
    return new Legacy(name);
  // bootstrap the instance
  this.name = name;
}

// legacy way to define classes
Legacy.prototype = {...};

// modern JS classes: private fields, own fields,
// super and other goodness available to devs
class Modern {}

// throws error: it requires `new Modern`
Modern()
```

### PyScript Events

Beside *hooks*' lifecycle, *PyScript* also dispatches specific events that might help users to work around its state:

#### m/py:ready

Both `mpy:ready` and `py:ready` events are dispatched per every *PyScript* related element found on the page, being this a `<script type="py">`, a `<py-script>` or any *mpy* counterpart.

Please **note** that these events are dispatched *right before* the code gets eventually executed, hence before the interpreter got a chance to run the code but always *after* the interpreter has already been bootstrapped.

```html title="A py:ready example"
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

As a matter of fact, if you are missing the previous *modal* showing a spinner while *pyodide* bootstrapped, it is fairly easy to provide a similar experience through this event: show a modal first, then close it once `py:ready` is triggered.

!!! warning

    On the *main* thread, *pyodide* blocks the *UI* until it's finished bootstrapping itself.
    This means that previous example without `worker` attribute will skip rendering `running` text because it happens at the same *UI* update that happens after the code has been executed.
    If needed, one can always `console.log` instead to be sure that event happened.

#### m/py:done

As the name might suggest, `mpy:done` and `py:done` events events are dispatched *after* the *sync* or *async* code has finished its execution.

```html title="A py:done example"
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

    If your async code never exits due some infinite loop or it uses some orchestration that keeps it running forever, such as `code` and `code.interact()` these events might never get triggered because the code actually is never really *done* so it cannot reach its own end of execution.

#### py:all-done

This event is special because it really groups all possible *mpy* or *py* scripts found on the page, no matter the interpreter.

In this example we'll see MicroPython waving before Pyodide and finally an *everything is done* message in *devtools*.

```html title="A py:all-done example"
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

### Python Modules

There are a few ways to host or include other modules in *PyScript*:

  * having the module already part of either *Pyodide* or *MicroPython* distribution
  * hosting on *GitHub* some file that need to be discovered and fetched at runtime as *package*
  * provide your own `module.py` as single file to include in the File System
  * create a folder with structured files and sub folders that can easily be *zipped* or *tar.gz* as unique entry, and let the File System do the rest

#### Hosting on GitHub

Beside modules already available behind the interpreter packages manager, it is possible to point directly at files in GitHub (or GitLab, or anywhere else the file can be downloaded without issues):

```python title="MicroPython mip example"
# Install default version from micropython-lib
mip.install("keyword")

# Install from raw URL
mip.install("https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/bisect/bisect.py")

# Install from GitHub shortcut
mip.install("github:jeffersglass/some-project/foo.py")
```

These URLs are recognized as *packages* entries in the *config* and as long as the URL allows *CORS* (fetching files from other domains) everything should be fine.

#### Provide your own file

Instead of using the *config* to define packages one can use the `files` field to bring modules in the runtime.

```html title="Module as File"
<mpy-config>
[files]
"./modules/bisect.py" = "./bisect.py"
</mpy-config>
<script type="mpy">
  import bisect
</script>
```

#### Zip or Tar Gz Modules

With this approach it's possible to archive in a compressed way the module content with a simple to complex structure:

```
my_module/__init__.py
my_module/util.py
my_module/sub/sub_util.py
```

Once archived as `.zip` or as `.tar.gz` in a way that contains the *my_module* folder and its content, it's possible to host this remotely or simply have it reachable locally:

```html title="Module as File"
<mpy-config>
[files]
"./my_module.zip" = "./*"
</mpy-config>
<script type="mpy">
  from my_module import util
  from my_module.sub import sub_util
</script>
```

Please **note** the `./*` convention, through a `.zip` or `.tar.gz` source, where the target folder with a star `*` will contain anything present in the source archive, in this example the whole *my_module* folder.

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
