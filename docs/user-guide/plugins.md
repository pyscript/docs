# Plugins

PyScript offers a plugin API _so anyone can extend its functionality and
share their modifications_.

PyScript only supports plugins written in Javascript (although causing the
evaluation of bespoke Python code can be a part of such plugins). The plugin's
JavaScript code should be included on the web page via a
`<script type="module">` tag **before PyScript is included in the web page**.

The PyScript plugin API defines hooks that intercept named events in the
lifecycle of a PyScript application, so you can modify how the platform
behaves. The [example at the bottom of this page](#example-plugin) demonstrates
how this is done in code.

### Lifecycle Events

PyScript emits events that capture the beginning or the end of specific stages
in the application's life. No matter if code is running in the main thread or
on a web worker, the exact same sequence of steps takes place:

  * **ready** - the browser recognizes the PyScript `script` or tag, and the
    associated Python interpreter is ready to work. A JavaScript callback can
    be used to instrument the interpreter before anything else happens.
  * **before run** - some Python code is about to be evaluated. A JavaScript
    callback could setup a bespoke browser context, be that in the main thread
    or a web worker. This is similar to a generic *setup* callback found in
    test frameworks.
  * **code before run** - sometimes a plugin needs Python code to be evaluated
    before the code given to PyScript, in order to set up a Python context
    for the referenced code. Such code is simply a string of Python evaluated
    immediately before the code given to PyScript.
  * **At this point in the lifecycle the code referenced in the `script` or
    other PyScript related tags is evaluated.**
  * **code after run** - sometimes a plugin needs Python code to be evaluated
    after the code given to PyScript, in order to clean up or react to the
    final state created by the referenced code. Such code is simply a string of
    Python code evaluated immediately after the code given to PyScript.
  * **after run** - all the Python code has been evaluated. A JavaScript
    callback could clean up or react to the resulting browser context, be that
    on the main thread or a web worker. This is similar to a generic *teardown*
    callback found in test frameworks.

PyScript's interpreters can run their code either *synchronously* or
*asynchronously*. No matter, the very same sequence is guaranteed to run in
order in both cases, the only difference being the naming convention used to
reference synchronous or asynchronous lifecycle hooks.

### Hooks

Hooks are used to tell PyScript that your code wants to subscribe to specific
lifecycle events. When such events happen, your code will be called by
PyScript.

The available hooks depend upon where your code is running: on the browser's
(blocking) main thread or on a (non-blocking) web worker. These are defined via
the `hooks.main` and `hooks.worker` namespaces in JavaScript.


#### Main Hooks

Callbacks registered via hooks on the main thread will usually receive a
wrapper of the interpreter with its unique-to-that-interpreter utilities, along
with a reference to the element on the page from where the code was derived.

Please refer to the documentation for the interpreter you're using (Pyodide or
MicroPython) to learn about its implementation details and the potential
capabilities made available via the wrapper.

Callbacks whose purpose is simply to run raw contextual Python code, don't
receive interpreter or element arguments. 

This table lists all possible, **yet optional**, hooks a plugin can register on
the main thread:

| name                      | example                                       | behavior  |
| :------------------------ | :-------------------------------------------- | :-------- |
| onReady                   | `onReady(wrap:Wrap, el:Element) {}`           | If defined, this hook is invoked before any other to signal that the interpreter is ready and code is going to be evaluated. This hook is in charge of eventually running Pythonic content in any way it is defined to do so. |
| onBeforeRun               | `onBeforeRun(wrap:Wrap, el:Element) {}`       | If defined, it is invoked before to signal that an element's code is going to be evaluated. |
| onBeforeRunAsync          | `onBeforeRunAsync(wrap:Wrap, el:Element) {}`  | Same as `onBeforeRun`, except for scripts that require `async` behaviour. |
| codeBeforeRun             | `codeBeforeRun: () => 'print("before")'`      | If defined, evaluate some Python code immediately before the element's code is evaluated. |
| codeBeforeRunAsync        | `codeBeforeRunAsync: () => 'print("before")'` | Same as `codeBeforeRun,` except for scripts that require `async` behaviour. |
| codeAfterRun              | `codeAfterRun: () => 'print("after")'`        | If defined, evaluate come Python code immediately after the element's code has finished executing. |
| codeAfterRunAsync         | `codeAfterRunAsync: () => 'print("after")'`   | Same as `codeAfterRun`, except for scripts that require `async` behaviour. |
| onAfterRun                | `onAfterRun(wrap:Wrap, el:Element) {}`        | If defined, invoked immediately after the element's code has been executed. |
| onAfterRunAsync           | `onAfterRunAsync(wrap:Wrap, el:Element) {}`   | Same as `onAfterRun`, except for scripts that require `async` behaviour. |
| onWorker                  | `onWorker(wrap = null, xworker) {}`           | If defined, whenever a script or tag with a `worker` attribute is processed, **this hook is triggered on the main thread**.  This allows possible [`xworker` features](https://pyscript.github.io/polyscript/#xworker) to be exposed **before the code is evaluated on the web worker**. The `wrap` reference is usually `null` unless an explicit `XWorker` call has been initialized manually and there is an interpreter on the main thread (*very advanced use case*). **Please note**, this is the only hook that doesn't exist in the *worker* counter list of hooks. |

#### Worker Hooks

When it comes to hooks on a web worker, callbacks **cannot** use any JavaScript
outer scope references and must be completely self contained. This is because 
**callbacks must be serializable** in order to work on web workers since they
are actually communicated as strings
[via a postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Worker/postMessage)
to the worker's isolated environment.

For example, this will work because all references are contained within the
registered function:

```js
import { hooks } from "https://pyscript.net/releases/2024.6.2/core.js";

hooks.worker.onReady.add(() => {
    // NOT suggested, just an example!
    // This code simply defines a global `i` reference if it doesn't exist.
    if (!('i' in globalThis))
        globalThis.i = 0;
    console.log(++i);
});
```

However, due to the outer reference to the variable `i`, this will fail:

```js
import { hooks } from "https://pyscript.net/releases/2024.6.2/core.js";

// NO NO NO NO NO! ☠️
let i = 0;

hooks.worker.onReady.add(() => {
    // The `i` in the outer-scope will cause an error if
    // this code executes in the worker because only the
    // body of this function gets stringified and re-evaluated
    console.log(++i);
});
```

As the worker won't have an `element` related to it, since workers can be
created procedurally, the second argument won't be a reference to an `element`
but a reference to the
[related `xworker` object](https://pyscript.github.io/polyscript/#xworker)
that is driving and coordinating things.

The list of possible **yet optional** hooks a custom plugin can use with a
web worker is exactly
[the same as for the main thread](#main-hooks)
**except for the absence of `onWorker`** and the replacement of the second
`element` argument with that of an `xworker`.

### Example plugin

Here's a contrived example, written in JavaScript, that should be added to the
web page via a `<script type="module">` tag before PyScript is included in
the page.

```js title="log.js - a plugin that simply logs to the console."
// import the hooks from PyScript first...
import { hooks } from "https://pyscript.net/releases/2024.6.2/core.js";

// The `hooks.main` attribute defines plugins that run on the main thread.
hooks.main.onReady.add((wrap, element) => {
    console.log("main", "onReady");
    if (location.search === '?debug') {
        console.debug("main", "wrap", wrap);
        console.debug("main", "element", element);
    }
});

hooks.main.onBeforeRun.add(() => {
    console.log("main", "onBeforeRun");
});

hooks.main.codeBeforeRun.add('print("main", "codeBeforeRun")');
hooks.main.codeAfterRun.add('print("main", "codeAfterRun")');
hooks.main.onAfterRun.add(() => {
    console.log("main", "onAfterRun");
});

// The `hooks.worker` attribute defines plugins that run on workers.
hooks.worker.onReady.add((wrap, xworker) => {
    console.log("worker", "onReady");
    if (location.search === '?debug') {
        console.debug("worker", "wrap", wrap);
        console.debug("worker", "xworker", xworker);
    }
});

hooks.worker.onBeforeRun.add(() => {
    console.log("worker", "onBeforeRun");
});

hooks.worker.codeBeforeRun.add('print("worker", "codeBeforeRun")');
hooks.worker.codeAfterRun.add('print("worker", "codeAfterRun")');
hooks.worker.onAfterRun.add(() => {
    console.log("worker", "onAfterRun");
});
```

```html title="Include the plugin in the web page before including PyScript."
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- JS plugins should be available before PyScript bootstraps -->
        <script type="module" src="./log.js"></script>
        <!-- PyScript -->
        <link rel="stylesheet" href="https://pyscript.net/releases/2024.6.2/core.css">
        <script type="module" src="https://pyscript.net/releases/2024.6.2/core.js"></script>
    </head>
    <body>
        <script type="mpy">
            print("ACTUAL CODE")
        </script>
    </body>
</html>
```
