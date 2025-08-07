# PyScript FFI

The foreign function interface (FFI) gives Python access to JavaScript, and
JavaScript access to Python. As a result PyScript is able to access all the
standard APIs and capabilities provided by the browser.

We provide a unified `pyscript.ffi` because
[Pyodide's FFI](https://pyodide.org/en/stable/usage/api/python-api/ffi.html)
is only partially implemented in MicroPython and there are some fundamental
differences. The `pyscript.ffi` namespace smooths out such differences into
a uniform and consistent API.

Our `pyscript.ffi` offers the following utilities:

* `ffi.to_js(reference)` converts a Python object into its JavaScript
  counterpart.
* `ffi.create_proxy(def_or_lambda)` proxies a generic Python function into a
  JavaScript one, without destroying its reference right away.
* `ffi.is_none(reference)` to check if a specific value is either `None` or `JsNull`.

Should you require access to Pyodide or MicroPython's specific version of the
FFI you'll find them under the `pyodide.ffi` and `micropython.ffi` namespaces.
Please refer to the documentation for those projects for further information.

## to_js

In the
[Pyodide project](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#pyodide.ffi.to_js),
this utility converts Python dictionaries into
[JavaScript `Map` objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map).
Such `Map` objects reflect the `obj.get(field)` semantics native to Python's
way of retrieving a value from a dictionary.

Unfortunately, this default conversion breaks the vast majority of native and
third party JavaScript APIs. This is because the convention in idiomatic
JavaScript is to use an [object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects)
for such key/value data structures (not a `Map` instance).

A common complaint has been the repeated need to call `to_js` with the long
winded argument `dict_converter=js.Object.fromEntries`. It turns out, most
people most of the time simply want to map a Python `dict` to a JavaScript
`object` (not a `Map`).

Furthermore, in MicroPython the default Python `dict` conversion is to the
idiomatic and sensible JavaScript `object`, making the need to specify a
dictionary converter pointless.

Therefore, if there is no reason to hold a Python reference in a JavaScript
context (which is 99% of the time, for common usage of PyScript) then use the
`pyscript.ffi.to_js` function, on both Pyodide and MicroPython, to always
convert a Python `dict` to a JavaScript `object`.

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
    the explicit field for `dict_converter`.

    However, we cannot guarantee all fields and features provided by Pyodide
    will work in the same way on MicroPython.

## create_proxy

In the
[Pyodide project](https://pyodide.org/en/stable/usage/api/python-api/ffi.html#pyodide.ffi.create_proxy),
this function ensures that a Python callable associated with an event listener,
won't be garbage collected immediately after the function is assigned to the
event. Therefore, in Pyodide, if you do not wrap your Python function, it is
immediately garbage collected after being associated with an event listener.

This is so common a gotcha (see the FAQ for
[more on this](../../faq#borrowed-proxy)) that the Pyodide project have already
created many work-arounds to address this situation. For example, the
`create_once_callable`, `pyodide.ffi.wrappers.add_event_listener` and
`pyodide.ffi.set_timeout` are all methods whose goal is to automatically manage
the lifetime of the passed in Python callback.

Add to this situation methods connected to the JavaScript `Promise` object
(`.then` and `.catch` callbacks that are implicitly handled to guarantee no
leaks once executed) and things start to get confusing and overwhelming with
many ways to achieve a common end result.

Ultimately, user feedback suggests folks simply want to do something like this,
as they write their Python code:

```python title="Define a callback without create_proxy."
import js
from pyscript import window


def callback(msg):
    """
    A Python callable that logs a message.
    """
    window.console.log(msg)


# Use the callback without having to explicitly create_proxy.
js.setTimeout(callback, 1000, 'success')
```

Therefore, PyScript provides an experimental configuration flag called
`experimental_create_proxy = "auto"`. When set, you should never have to care
about these technical details nor use the `create_proxy` method and all the
JavaScript callback APIs should just work.

Under the hood, the flag is strictly coupled with the JavaScript garbage
collector that will eventually destroy all proxy objects created via the
[FinalizationRegistry](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry)
built into the browser.

This flag also won't affect MicroPython because it rarely needs a
`create_proxy` at all when Python functions are passed to JavaScript event
handlers. MicroPython automatically handles this situation. However,
there might still be rare and niche cases in MicroPython where such a
conversion might be needed.

Hence, PyScript retains the `create_proxy` method, even though it does not
change much in the MicroPython world, although it might be still needed with
the Pyodide runtime is you don't use the `experimental_create_proxy = "auto"`
flag.

At a more fundamental level, MicroPython doesn't provide (yet) a way to
explicitly destroy a proxy reference, whereas Pyodide still expects to
explicitly invoke `proxy.destroy()` when the function is not needed.

!!! warning

    In MicroPython proxies might leak due to the lack of a `destroy()` method.

    Happily, proxies are usually created explicitly for event listeners or
    other utilities that won't need to be destroyed in the future. So the lack
    of a `destroy()` method in MicroPython is not a problem in this specific,
    and most common, situation.

    Until we have a `destroy()` in MicroPython, we suggest testing the
    `experimental_create_proxy` flag with Pyodide so both runtimes handle
    possible leaks automatically.

For completeness, the following examples illustrate the differences in
behaviour between Pyodide and MicroPython:

```html title="A classic Pyodide gotcha VS MicroPython"
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

To address the difference in Pyodide's behaviour, we can use the experimental
flag:

```html title="experimental create_proxy"
<py-config>
    experimental_create_proxy = "auto"
</py-config>

<!-- logs "success" after a second in both Pyodide and MicroPython -->
<script type="py">
    import js
    js.setTimeout(lambda x: print(x), 1000, "success");
</script>
```

Alternatively, `create_proxy` via the `pyscript.ffi` in both interpreters, but
only in Pyodide can we then destroy such proxy:

```html title="pyscript.ffi.create_proxy"
<!-- success in both Pyodide and MicroPython -->
<script type="py">
    from pyscript.ffi import create_proxy
    import js

    def log(x):
        try:
            proxy.destroy()
        except:
            pass  # MicroPython
        print(x)

    proxy = create_proxy(log)
    js.setTimeout(proxy, 1000, "success");
</script>
```

## is_none

*Pyodide* version `0.28` onwards has introduced a new *nullish* value that
precisely represents JavaScript's `null` value.

Previously, both JavaScript `null` and `undefined` would have been converted
into Python's `None` but, alas, some APIs behave differently if a value is
`undefined` or explicitly `null`.

For example, in *JSON*, `null` would survive serialization while `undefined`
would vanish. To preserve that distinction in *Python*, the conversion
between *JS* and *Python* now has a new `pyodide.ffi.jsnull` as explained in
the
[pyodide documentation](https://pyodide.org/en/stable/usage/type-conversions.html#javascript-to-python).

In general, there should be no surprises. But, especially when dealing with the
*DOM* world, most utilities and methods return `null`.

To simplify and smooth-out this distinction, we decided to introduce `is_null`,
as [demoed here](https://pyscript.com/@agiammarchi/pyscript-ffi-is-none/latest?files=main.py):

```html title="pyscript.ffi.is_none"
<!-- success in both Pyodide and MicroPython -->
<script type="py">
    from pyscript.ffi import is_none
    import js

    js_undefined = js.undefined
    js_null = js.document.body.getAttribute("nope")

    print(js_undefined is None)     # True
    print(js_null)                  # jsnull
    print(js_null is None)          # False

    # JsNull is still a "falsy" value
    if (js_null):
        print("this will not be shown")

    # safely compared against both
    print(is_none(js_undefined))    # True
    print(is_none(js_none))         # True
</script>
```

Please note that in *MicroPython* the method works the same but, as we try to
reach feature-parity among runtimes, it is suggested to use `is_none(ref)`
even if, right now, there is no such distinction between `null` and
`undefined` in MicroPython.
