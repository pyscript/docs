# Plugins

PyScript's plugin API lets you extend the platform and modify its
behaviour. Plugins intercept lifecycle events, inject code, and
customise how PyScript operates. Anyone can create plugins and share
them with the community.

This guide explains the plugin system, lifecycle hooks, and how to write
plugins that integrate with PyScript.

## Understanding plugins

Plugins are written in JavaScript and included on the page before
PyScript loads. They register hooks - callbacks that PyScript invokes at
specific points in the application lifecycle. These hooks let you
instrument interpreters, inject Python code, modify execution context,
and react to events.

Include plugin code via a `<script type="module">` tag before the
PyScript script tag. This ensures the plugin registers its hooks before
PyScript initialises.

## Application lifecycle

PyScript follows a predictable sequence of events, whether code runs on
the main thread or in workers. Understanding this lifecycle helps you
choose the right hooks for your plugin.

The sequence begins when the browser recognises a PyScript script tag.
The interpreter initialises and becomes ready. At this point, the
**ready** event fires. Plugins can instrument the interpreter before
anything else happens.

Before code evaluation, the **before run** event fires. Plugins can set
up browser context on either the main thread or workers. This is similar
to setup callbacks in test frameworks.

If plugins need Python code evaluated first, they provide **code before
run** - a string of Python that executes immediately before the main
code. This sets up Python context for the script.

Then the actual script code evaluates - the Python you wrote in your
script tags or source files.

After code finishes, **code after run** executes if plugins provided it.
This Python code cleans up or reacts to the final state.

Finally, the **after run** event fires. Plugins can clean up browser
context or react to results. This is similar to teardown callbacks in
test frameworks.

This sequence happens consistently for both synchronous and asynchronous
code execution. The naming conventions desscribed below distinguish sync
versus async hooks, but the sequence remains the same.

## Main thread hooks

Hooks on the main thread receive a wrapper around the interpreter and a
reference to the HTML element containing the script. The wrapper
provides interpreter-specific utilities and capabilities.

Refer to Pyodide or MicroPython documentation to understand what
capabilities the wrapper exposes for each interpreter.

Hooks that inject Python code don't receive these arguments - they
simply return Python code as strings.

### Available main hooks

**`onReady(wrap, element)`** - Called when the interpreter is ready but
before any code evaluates. Instrument the interpreter or prepare the
execution environment.

**`onBeforeRun(wrap, element)`** - Called just before code evaluation.
Set up browser context or prepare for execution.

**`onBeforeRunAsync(wrap, element)`** - Async version of `onBeforeRun`
for scripts requiring async behaviour.

**`codeBeforeRun()`** - Returns Python code as a string to evaluate
before the main script.

**`codeBeforeRunAsync()`** - Async version of `codeBeforeRun`.

**`codeAfterRun()`** - Returns Python code as a string to evaluate after
the main script.

**`codeAfterRunAsync()`** - Async version of `codeAfterRun`.

**`onAfterRun(wrap, element)`** - Called after code finishes executing.
Clean up or react to results.

**`onAfterRunAsync(wrap, element)`** - Async version of `onAfterRun`.

**`onWorker(wrap, xworker)`** - Called on the main thread when a script
with the `worker` attribute is processed. This is the only hook that
doesn't have a worker counterpart. It lets you expose features to the
worker before code evaluates there. The `wrap` is usually `null` unless
you've manually initialised an XWorker (advanced use case).

All hooks are optional. Register only the hooks your plugin needs.

## Worker hooks

Worker hooks follow the same lifecycle as main thread hooks but with
important constraints. Worker callbacks must be completely self-contained
and serialisable - they cannot reference anything in outer scope.

This is because callbacks are stringified and sent to the worker via
`postMessage`. Only the function body gets serialised, so outer scope
references fail.

This works because everything is self-contained:

```js
import { hooks } from "https://pyscript.net/releases/2025.11.2/core.js";

hooks.worker.onReady.add(() => {
    // Define global variable if it doesn't exist.
    if (!('i' in globalThis))
        globalThis.i = 0;
    console.log(++i);
});
```

This fails because of the outer scope reference:

```js
import { hooks } from "https://pyscript.net/releases/2025.11.2/core.js";

// This won't work in workers!
let i = 0;

hooks.worker.onReady.add(() => {
    // The outer 'i' doesn't exist in the worker.
    console.log(++i);
});
```

Worker hooks receive the same lifecycle events as main hooks, except
there's no `onWorker` hook.

The second argument to callback hooks is always an `xworker` object
instead of an element reference, since workers can be created
programmatically without corresponding HTML elements.

## Example plugin

Here's a complete plugin that logs lifecycle events to the console:

```js
// Import hooks from PyScript.
import { hooks } from "https://pyscript.net/releases/2025.11.2/core.js";

// Register main thread hooks.
hooks.main.onReady.add((wrap, element) => {
    console.log("main: interpreter ready");
    if (location.search === '?debug') {
        console.debug("wrap:", wrap);
        console.debug("element:", element);
    }
});

hooks.main.onBeforeRun.add(() => {
    console.log("main: about to run code");
});

hooks.main.codeBeforeRun.add('print("main: injected before")');
hooks.main.codeAfterRun.add('print("main: injected after")');

hooks.main.onAfterRun.add(() => {
    console.log("main: finished running code");
});

// Register worker hooks.
hooks.worker.onReady.add((wrap, xworker) => {
    console.log("worker: interpreter ready");
    if (location.search === '?debug') {
        console.debug("wrap:", wrap);
        console.debug("xworker:", xworker);
    }
});

hooks.worker.onBeforeRun.add(() => {
    console.log("worker: about to run code");
});

hooks.worker.codeBeforeRun.add('print("worker: injected before")');
hooks.worker.codeAfterRun.add('print("worker: injected after")');

hooks.worker.onAfterRun.add(() => {
    console.log("worker: finished running code");
});
```

Include this plugin before PyScript:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Plugin loads first. -->
    <script type="module" src="./log.js"></script>
    
    <!-- PyScript loads after. -->
    <link rel="stylesheet" 
      href="https://pyscript.net/releases/2025.11.2/core.css">
    <script type="module" 
      src="https://pyscript.net/releases/2025.11.2/core.js"></script>
</head>
<body>
    <script type="mpy">
        print("ACTUAL CODE")
    </script>
</body>
</html>
```

The output shows the lifecycle sequence: ready hooks fire first, then
before run hooks, then injected code before, then the actual script,
then injected code after, and finally after run hooks.

## Plugin use cases

Plugins enable many customisations. You might create plugins to log
execution for debugging, inject analytics or telemetry code, modify
interpreter behaviour, provide library bootstrapping, implement custom
security checks, or add domain-specific features.

The terminal and editor features in PyScript are themselves implemented
as plugins, demonstrating the power and flexibility of the plugin system.

## What's next

Now that you understand plugins, explore these related topics:

**[Terminal](terminal.md)** - Use the alternative REPL-style
interface for interactive Python sessions.

**[Editor](editor.md)** - Create interactive Python coding environments in
web pages with the built-in code editor.

**[PyGame](pygame-ce.md)** - Use PyGame-CE with PyScript, covering the
differences from traditional PyGame development and techniques for making
games work well in the browser.