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

### PyScript latest

For various reasons previously discussed at length, we decided to remove our `latest` channel from our own CDN.

We were not super proud of users trusting that channel coming back with suddenly broken projects so we now [release only official versions](https://github.com/pyscript/pyscript/releases) everyone can pin-point in time.

We are also developing behind the scene through *npm* to be able to test in the wild breaking changes and what's not and it's no secret that *CDNs* could also deliver our "*canary*" or "*development*" channel so that we're better off telling you exactly which links one should use to have the latest, whenever latest lands on the *CDN* which is usually within 24 hours from the last *npm* version change.

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
