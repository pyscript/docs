# Plugins


PyScript, like many other software plaforms, offers a Plugin API that can be used to extend its
own functionality without the need to modify its own core. By using this API, users can add new
features and distribute them as plugins.

At the moment, PyScript supports plugins written in Javascript. These plugins can use PyScript
Plugins API to define entry points and hooks so that the plugin can be collected and hook into
the PyScript lifecycle events, with the ablity to modify and integrate the features of PyScript
core itself.

Here's an example of how a PyScript plugin looks like:

```js
// import the hooks from PyScript first...
import { hooks } from "https://pyscript.net/releases/2023.12.1/core.js";

// Use the `main` attribute on hooks do define plugins that run on the main thread
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

// Use the `worker` attribute on hooks do define plugins that run on workers
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

That's it.


## Plugins API

As mentioned above, PyScript Plugins API exposes a set of hooks that can be used to intercept
specific events in the lifecycle of a PyScript application and add or modify specific features
of the platform itself. To better understand how it works it's important to understand the concepts
around a PyScript application and plugins.

### Code Execution Methods

There are 2 mains PyScript Applications can execute code: the browser main
[thread](https://developer.mozilla.org/en-US/docs/Glossary/Main_thread) and on
[web workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers).

We highly recommend users to independently search the difference between the 2 methods to fully understand
the difference and consequences but here's a short summary:

* main thread: executing code in the browser main thread means the code is being executed in the same
process where the browser processes user events and paints. By default, the browser uses this single thread
to run all the JavaScript code in your page, as well as to perform layout, reflows, and garbage collection.
This means that long-running code or blocking calls can or will block the thread, leading to an unresponsive
page and a bad user experience.
* web workers: code executed in workers actually run on "background" threads. This means the code can perform
tasks without interfering with the user interface or other operations being perfomed in the main thread. While
this adds great flexibility it's important to understand that workers actually have limited capabilities when
comparing to code executed on the main thread. For instace, while PyScript offers a DOM API that actually can
be used in web workers on the browser, by default, does not allow DOM operation in workers. So, in this case,
if you just use `window` and `document` directly mapping the Javascript FFI provided directly by the interpreters
we support (Pyodide and MicroPython). With that in mind, `from pyscript import window, document` will work and
allow you to interact with the DOM while the following will not:

```
from js import document, window
```

or

```
import js
js.document
```

or 

```
import js
js.window
```

will not.

In general, we recommend executing your code on workers unless there are explicit reasons preventing users from
doing that.

### Lifecycle Events

During the execution of a PyScript application there are specfic events that capture the beginning
or the end of specific stages. Here are the main lifecycle events of a PyScript Application:

Every script or tag running through PyScript inevitably passes through some main or worker thread related tasks.

In both worlds (wither executing code in the main thread or on a web worker), the exact sequence of steps around code execution is the following:

  * **ready** - the DOM recognized the special script or tag and the associated interpreter is ready to work. A *JS* callback might be useful to instrument the interpreter before anything else happens.
  * **before run** - there could be some *JS* code setup specific for the script on the main thread, or the worker. This is similar to a generic *setup* callback in tests.
  * **code before run** - there could be some *PL* code to prepend to the one being executed. In this case the code is a string because it will be part of the evaluation.
  * **actual code** - the code in the script or tag or the `src` file specified in the script. This is not a hook, just the exact time the code gets executed in general.
  * **code after run** - there could be some *PL* code to append to the one being executed. Same as *before*, the code is a string targeting the foreign *PL*.
  * **after run** - there could be some *JS* to execute right after the whole code has been evaluated. This is similar to a generic *teardown* callback in tests.

As most interpreters can run their code either *synchronously* or *asynchronously*, the very same sequence is guaranteed to run in order in both cases, and the difference is only around the naming convention [as we'll see below].

### Hooks

Hooks are a especial mechanism that can be used to tell PyScript that your code wants to subscribe to specific events, allowing your code to get called
by PyScript's event loop when a specific event happens.

#### Main Hooks

When it comes to *main* hooks all callbacks will receive a *wrapper* of the interpreter with its utilities, see the further section to know more, plus the element on the page that is going to execute its related code, being this a custom script/type or a custom tag.

This is the list of all possible, yet **optional** hooks, a custom type can define for **main**:

| name                      | example                                       | behavior  |
| :------------------------ | :-------------------------------------------- | :-------- |
| onReady                   | `onReady(wrap:Wrap, el:Element) {}`           | If defined, it is invoked before any other hook to signal that the element is going to execute the code. For custom scripts, this hook is in charge of eventually running the content of the script, anyway it prefers to do so. |
| onBeforeRun               | `onBeforeRun(wrap:Wrap, el:Element) {}`       | If defined, it is invoked before any other hook to signal that the element is going to execute the code. |
| onBeforeRunAsync          | `onBeforeRunAsync(wrap:Wrap, el:Element) {}`  | Same as `onBeforeRun` except it's the one used whenever the script is `async`. |
| codeBeforeRun             | `codeBeforeRun: () => 'print("before")'`      | If defined, prepend some code to evaluate right before the rest of the code gets executed. |
| codeBeforeRunAsync        | `codeBeforeRunAsync: () => 'print("before")'` | Same as `codeBeforeRun` except it's the one used whenever the script is `async`. |
| codeAfterRun              | `codeAfterRun: () => 'print("after")'`        | If defined, append some code to evaluate right after the rest of the code already executed. |
| codeAfterRunAsync         | `codeAfterRunAsync: () => 'print("after")'`   | Same as `codeAfterRun` except it's the one used whenever the script is `async`. |
| onAfterRun                | `onAfterRun(wrap:Wrap, el:Element) {}`        | If defined, it is invoked after the foreign code has been executed already. |
| onAfterRunAsync           | `onAfterRunAsync(wrap:Wrap, el:Element) {}`   | Same as `onAfterRun` except it's the one used whenever the script is `async`. |
| onWorker                  | `onWorker(wrap = null, xworker) {}`           | If defined, whenever a script or tag with a `worker` attribute is processed it gets triggered on the main thread, to allow to expose possible `xworker` features before the code gets executed within the worker thread. The `wrap` reference is most of the time `null` unless an explicit `XWorker` call has been initialized manually and/or there is an interpreter on the main thread (*very advanced use case*). Please **note** this is the only hook that doesn't exist in the *worker* counter list of hooks. |

#### Worker Hooks

When it comes to *worker* hooks, **all non code related callbacks must be serializable**, meaning that callbacks cannot use any outer scope reference, as these are forwarded as strings, hence evaluated after in the worker, to survive the main <-> worker `postMessage` dance.

Here an example of what works and what doesn't:

```js
// this works 👍
define('pl', {
  interpreter: 'programming-lang',
  hooks: {
    worker: {
      onReady() {
        // NOT suggested, just as example!
        if (!('i' in globalThis))
          globalThis.i = 0;
        console.log(++i);
      }
    }
  }
});

// this DOES NOT WORK ⚠️
let i = 0;
define('pl', {
  interpreter: 'programming-lang',
  hooks: {
    worker: {
      onReady() {
        // that outer-scope `i` is nowhere understood
        // whenever this code executes in the worker
        // as this function gets stringified and re-evaluated
        console.log(++i);
      }
    }
  }
});
```

At the same time, as the worker doesn't have any `element` strictly related, as workers can be created also procedurally, the second argument won't be an element but the related *xworker* that is driving the logic.

As summary, this is the list of all possible, yet **optional** hooks, a custom type can define for **worker**:

| name                      | example                                       | behavior |
| :------------------------ | :-------------------------------------------- | :--------|
| onReady                   | `onReady(wrap:Wrap, xw:XWorker) {}`           | If defined, it is invoked before any other hook to signal that the xworker is going to execute the code. Differently from **main**, the code here is already known so all other operations will be performed automatically. |
| onBeforeRun               | `onBeforeRun(wrap:Wrap, xw:XWorker) {}`       | If defined, it is invoked before any other hook to signal that the xworker is going to execute the code. |
| onBeforeRunAsync          | `onBeforeRunAsync(wrap:Wrap, xw:XWorker) {}`  | Same as `onBeforeRun` except it's the one used whenever the worker script is `async`. |
| codeBeforeRun             | `codeBeforeRun: () => 'print("before")'`      | If defined, prepend some code to evaluate right before the rest of the code gets executed. |
| codeBeforeRunAsync        | `codeBeforeRunAsync: () => 'print("before")'` | Same as `codeBeforeRun` except it's the one used whenever the worker script is `async`. |
| codeAfterRun              | `codeAfterRun: () => 'print("after")'`        | If defined, append some code to evaluate right after the rest of the code already executed. |
| codeAfterRunAsync         | `codeAfterRunAsync: () => 'print("after")'`   | Same as `codeAfterRun` except it's the one used whenever the worker script is `async`. |
| onAfterRun                | `onAfterRun(wrap:Wrap, xw:XWorker) {}`        | If defined, it is invoked after the foreign code has been executed already. |
| onAfterRunAsync           | `onAfterRunAsync(wrap:Wrap, xw:XWorker) {}`   | Same as `onAfterRun` except it's the one used whenever the worker script is `async`. |
