# PyScript FFI

The reason we decided to incrementally provide a unified *pyscript.ffi* utility is that [Pyodide](https://pyodide.org/en/stable/usage/api/python-api/ffi.html)'s *ffi* is only partially implemented in *MicroPython* but there are fundamental differences even with the few common utilities both projects provide, hence our intention to smooth out their usage with all the features or caveats one needs to be aware of.

Our `pyscript.ffi` offers the following utilities:

  * `ffi.to_js(reference)` to convert any Python reference to its *JS* counterpart
  * `ffi.create_proxy(def_or_lambda)` to proxy a generic Python's function into a *JS* one, without destroying its reference right away

## to_js

In the [Pyodide project](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#pyodide.ffi.to_js), this utility converts Python dictionaries into a *Map*. The *Map* object more accurately reflects the `obj.get(field)` native Python way to retrieve a value from a dictionary.

However, we have noticed that this default conversion plays very badly with pretty much any native or user made *JS* API, so that most of the code around `to_js` needs to explicitly define a `dict_converter=js.Object.fromEntries` instead of mapping Python's dictionaries directly as JS' objects literal.

On top of that, in *MicroPython* the default conversion already produces *object literals*, making the need to specify a different converter pretty pointless.

As we all known though, *explicit is better than implicit*, so whenever an object literal is expected and no reason to hold a Python reference in the JS world is needed, using `to_js(python_dictionary)` will guarantee the entity to be copied or passed as *object literal* to the consumer of that dictionary.

```html title="to_js: pyodide.ffi VS pyscript.ffi"
<!-- works on Pyodide (type py) only -->
<script type="py">
  from pyodide.ffi import to_js

  # default into JS new Map([["a", 1], ["b", 2]])
  to_js({"a": 1, "b": 2})
</script>

<!-- works on both Pyodide and MicroPython -->
<script type="py">
  from pyscript.ffi import to_js

  # always default into JS {"a": 1, "b": 2}
  to_js({"a": 1, "b": 2})
</script>
```

!!! Note

    It is still possible to specify a different `dict_converter` or use Pyodide
    specific features while converting Python references by simply overriding
    the explicit field for `dict_converter`. However, we cannot guarantee
    all fields and features provided by Pyodide will work the same on MicroPython.

## create_proxy

In the [Pyodide project](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#pyodide.ffi.create_proxy), this utility guarantees that a Python lambda or callback won't be garbage collected immediately after.

There are, still in *Pyodide*, dozens ad-hoc utilities that work around that implementation detail, such as `create_once_callable` or `pyodide.ffi.wrappers.add_event_listener` or `pyodide.ffi.wrappers.set_timeout` and others, all methods whose goal is to automatically handle the lifetime of the passed callback.

There are also implicit helpers like in `Promise` where `.then` or `.catch` callbacks are implicitly handled a part to guarantee no leaks once executed.

Because the amount of details could be easily overwhelming, we decided to provide an `experimental_create_proxy = "auto"` configuration option that should never require our users to care about all these details while all the generic APIs in the *JS* world should "*just work*".

This flag is strictly coupled with the *JS* garbage collector and it will eventually destroy all proxies that were previously created through the [FinalizationRegistry](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry) native utility.

This flag also won't affect *MicroPython* because it rarely needs a `create_proxy` at all, when Python functions are passed to JS, but there are still cases where that conversion might be needed or explicit.

For these reasons we expose also the `create_proxy` utility which does not change much in the *MicroPython* world or code, but it might be still needed in the *Pyodide* runtime.

The main difference with these two different runtime is that *MicroPython* doesn't provide (yet) a way to explicitly destroy the proxy reference, while in *Pyodide* it's still desirable to explicitly invoke that `proxy.destroy()` when the function is not needed/called anymore.

```html title="A classic Pyodide failure VS MicroPython"
<!-- Throws:
Uncaught Error: This borrowed proxy was automatically destroyed
at the end of a function call. Try using create_proxy or create_once_callable.
-->
<script type="py">
    import js
    js.setTimeout(lambda x: print(x), 1000, "fail");
</script>

<!-- logs "success" after a second -->
<script type="mpy">
    import js
    js.setTimeout(lambda x: print(x), 1000, "success");
</script>
```

To address the difference in Pyodide's behaviour, we can use the experimental flag:

```html title="experimental create_proxy"
<py-config>
    experimental_create_proxy = "auto"
</py-config>

<!-- logs "success" after a second -->
<script type="py">
    import js
    js.setTimeout(lambda x: print(x), 1000, "success");
</script>
```

Alternatively, it is possible to create a proxy via our *ffi* in both interpreters, but only in Pyodide can we then destroy such proxy:

```html title="pyscript.ffi.create_proxy"
<!-- success in both Pyodide and MicroPython -->
<script type="py">
    from pyscript.ffi import create_proxy
    import js

    def log(x):
        try:
            proxy.destroy()
        except:
            pass # MicroPython

        print(x)

    proxy = create_proxy(log)
    js.setTimeout(proxy, 1000, "success");
</script>
```

!!! warning

    In MicroPython proxies might leak due to the lack of a `destroy()` method.
    Usually proxies are better off created explicitly for event listeners
    or other utilities that won't need to be destroyed in the future.
    Until we have a `destroy()` in MicroPython, it's still suggested to try
    and test if the experimental flag is good enough for Pyodide and let
    both runtime handle possible leaks behind the scene automatically.
