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
import { hooks } from "<path_to_pyscript>/core.js";

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
behind Plugins.

### Concepts

**TODO: ADD LIST OF CONCEPTS**




Here's a list of the available hooks:
