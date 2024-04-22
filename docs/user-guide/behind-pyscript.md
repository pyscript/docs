# Behind PyScript

There are various projects that make PyScript possible and it's probably worth exploring each project responsibility to help both users and contributors to land both issues or feature requests in the right place.

## Polyscript

The [polyscript project](https://github.com/pyscript/polyscript#readme) purpose is to enable any runtime / programming language able to interface itself with *JS* through the *WASM* browsers native API.

The scope of this project can be summarized as such:

  * provide as little as possible abstraction to bootstrap different interpreters (Pyodide, MicroPython, R, Lua, Ruby, others ...)
  * simplify the bootstrap of any interpreter through DOM primitives (script, custom-elements, or both ...)
  * understand and parse any explicit configuration option (being this a file to parse or an already parsed object literal)
  * forward any defined **hook** to the interpreter so that code before, or right after, can be transparently executed
  * orchestrate a single bootstrap per each involved element, being this a script or a `<custom-script>` on the living page
  * ensure a *Worker*, optionally *Atomics* and *SharedArrayBuffer* based, stand-alone environment can be bootstrapped and available for at least not experimental runtime (Lua, Ruby, [others](https://pyscript.github.io/polyscript/#interpreter-features))

While this is a simplification of all the things polyscript does behind the scene, the rule of thumb to "*blame*" *polyscript* for anything affecting your project/idea is likely:

  * is my interpreter not loading?
  * where are errors around my interpreter not loading?
  * is my *HTML* event not triggering? (`py-*` or `mpy-*` or ...)
  * how come this feature handled explicitly by *polyscript* is not reflected in my *PyScript* project? (this is likely and advanced issue/use case, but it's always OK to ask *why* in polyscript, and answers will flow accordingly)

To summarize, as much as *PyScript* users should never encounter one of these issues, it is possible some specific feature request or issue might be enabled in polyscript first to land then in PyScript.

## Coincident

At the core of *polyscript* project there is one extra project enabling all the seamless worker to main, and vice-versa, features called [coincident](https://github.com/WebReflection/coincident#readme).

The purpose of this project is to enable, in a memory / garbage collector friendly way, a communication channel between one thread and another, handling the main thread dealing with workers references, or the other way around, as its best core feature.

Anything strictly related to *SharedArrayBuffer* issues is then an orchestration *coincident* is handling, and to some extend also anything memory leak related could as well fall down to this module purpose and scope.

In a nutshell, this project takes care of, and is responsible for, the following patterns:

  * invoking something from a worker that refers the main thread somehow fails
  * there is a reproducible and cross platform (browsers) memory leak to tackle
  * some function invoke with some specific argument from a worker doesn't produce the expected result

All these scenarios are unlikely to happen with *PyScript* project, as these are all battle tested and covered with such general purpose cross-env/realm oriented project way before landing in *PyScript*, but if you feel something is really off, leaking, or badly broken, please feel free to file an issue in this project and, once again, there is never a silly question about it so that, as long as you can provide any minimal reproducible issue, all questions and issues are more than welcome!

