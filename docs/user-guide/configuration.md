# Configuration

The browser tab in which your PyScript based web page is displayed is a very
secure sandboxed computing environment for running your Python code.

This is also the case for web workers running Python. Despite being associated
with a single web page, workers are completely separate from each other
(except for some very limited and clearly defined means of interacting, which
PyScript looks after for you).

We need to tell PyScript how we want such Python environments to be configured.
This works in the same way for both the main thread and for web workers. Such
configuration ensures we get the expected resources ready before our Python
code is evaluated (resources such as arbitrary data files and third party
Python packages).

## TOML or JSON

Configuration can be expressed in two formats:

* [TOML](https://toml.io/en/) is the configuration file format preferred by
  folks in the Python community.
* [JSON](https://www.json.org/json-en.html) is a data format most often used
  by folks in the web community.

Since PyScript is the marriage of Python and the web, and we respect the
traditions of both technical cultures, we support both formats.

However, because JSON is built into all browsers by default and TOML requires
an additional download of a specialist parser before PyScript can work, **the
use of JSON is more efficient from a performance point of view**.

The following two configurations are equivalent, and simply tell PyScript to
ensure the packages [arrr](https://arrr.readthedocs.io/en/latest/) and
[numberwang](https://numberwang.readthedocs.io/en/latest/) are installed from
PyPI (the [Python Packaging Index](https://pypi.org/)):

```TOML title="Configuration via TOML."
packages = ["arrr", "numberwang" ]
```

```JSON title="Configuration via JSON."
{
    "packages": ["arrr", "numberwang"]
}
```

## File or inline

The recommended way to write configuration is via a separate file and then
reference it from the tag used to specify the Python code:

```HTML title="Reference a configuration file"
<script type="py" src="main.py" config="pyscript.toml"></script>
```

If you use JSON, you can make it the value of the `config` attribute:

```HTML title="JSON as the value of the config attribute."
<script type="mpy" src="main.py" config='{"packages":["arrr", "numberwang"]}'></script>
```

For historical and convenience reasons we still support the inline
specification of configuration information via a _single_ `<py-config>` or
`<mpy-config>` tag in your HTML document:

```HTML title="Inline configuration via the &lt;py-config&gt; tag."
<py-config>
{
    "packages": ["arrr", "numberwang" ]
}
</py-config>
```

!!! warning

    Should you use `<py-config>` or `<mpy-config>`, **there must be only one of
    these tags on the page per interpreter**.

## Options

There are five core options ([`interpreter`](#interpreter), [`files`](#files),
[`packages`](#packages), [`js_modules`](#javascript-modules) and
[`sync_main_only`](#sync_main_only)) and an experimental flag
([`experimental_create_proxy`](#experimental_create_proxy)) that can be used in
the configuration of PyScript. The user is also free to define
arbitrary additional configuration options that plugins or an app may require
for their own reasons.

### Interpreter

The `interpreter` option pins the Python interpreter to the version of the
specified value. This is useful for testing (does my code work on a specific
version of Pyodide?), or to ensure the precise combination of PyScript version
and interpreter version are pinned to known values.

The value of the `interpreter` option should be a valid version number
for the Python interpreter you are configuring, or a fully qualified URL to
a custom version of the interpreter.

The following two examples are equivalent:

```TOML title="Specify the interpreter version in TOML."
interpreter = "0.23.4"
```

```JSON title="Specify the interpreter version in JSON."
{
    "interpreter": "0.23.4"
}
```

The following JSON fragment uses a fully qualified URL to point to the same
version of Pyodide as specified in the previous examples:

```JSON title="Specify the interpreter via a fully qualified URL."
{
    "interpreter": "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.mjs"
}
```

### Files

The `files` option fetches arbitrary content from URLs onto the virtual
filesystem available to Python, and emulated by the browser. Just map a valid
URL to a destination filesystem path on the in-browser virtual filesystem. You
can find out more in the section about
[PyScript and filesystems](../filesystem/).

The following JSON and TOML are equivalent:

```json title="Fetch files onto the filesystem with JSON."
{
  "files": {
    "https://example.com/data.csv": "./data.csv",
    "./code.py": "./subdir/code.py"
  }
}
```

```toml title="Fetch files onto the filesystem with TOML."
[files]
"https://example.com/data.csv" = "./data.csv"
"./code.py" = "./subdir/code.py"
```

If you make the target an empty string, the final "filename" part of the source
URL becomes the destination filename, in the root of the filesystem, to which
the content is copied. As a result, the `data.csv` entry from the previous
examples could be equivalently re-written as:

```json title="JSON implied filename in the root directory."
{
  "files": {
    "https://example.com/data.csv": "",
    "./code.py": ""
  }
}
```

```toml title="TOML implied filename in the root directory."
[files]
"https://example.com/data.csv" = ""
"./code.py" = ""
```

If the source part of the configuration is either a `.zip` or `.tar.gz` file
and its destination is a folder path followed by a star (e.g. `/*` or
`./dest/*`), then PyScript will extract the referenced archive automatically
into the target directory in the browser's built in file system.

!!! warning

    **PyScript expects all file destinations to be unique.**

    If there is a duplication PyScript will raise an exception to help you find
    the problem.

!!! warning
    **Use destination URLs instead of CORS / redirect URLs.**

    For example, `https://github.com/pyscript/ltk/raw/refs/heads/main/ltk/jquery.py`
    redirects to `https://raw.githubusercontent.com/pyscript/ltk/refs/heads/main/ltk/jquery.py`. Use the latter.

!!! tip

    **For most people, most of the time, the simple URL to filename mapping,
    described above, will be sufficient.**

    Yet certain situations may require more flexibility. In which case, read
    on.

Sometimes many resources are needed to be fetched from a single location and
copied into the same directory on the file system. To aid readability and
reduce repetition, the `files` option comes with a mini
[templating language](https://en.wikipedia.org/wiki/Template_processor)
that allows reusable placeholders to be defined between curly brackets (`{`
and `}`). When these placeholders are encountered in the `files` configuration,
their name is replaced with their associated value.

!!! Attention

    Valid placeholder names are always enclosed between curly brackets
    (`{` and `}`), like this: `{FROM}`, `{TO}` and `{DATA SOURCE}`
    (capitalized names help identify placeholders
    when reading code ~ although this isn't strictly necessary).

    Any number of placeholders can be defined and used anywhere within URLs and
    paths that map source to destination.

The following JSON and TOML are equivalent:

```json title="Using the template language in JSON."
{
  "files": {
    "{DOMAIN}": "https://my-server.com",
    "{PATH}": "a/path",
    "{VERSION}": "1.2.3",
    "{FROM}": "{DOMAIN}/{PATH}/{VERSION}",
    "{TO}": "./my_module",
    "{FROM}/__init__.py": "{TO}/__init__.py",
    "{FROM}/foo.py": "{TO}/foo.py",
    "{FROM}/bar.py": "{TO}/bar.py",
    "{FROM}/baz.py": "{TO}/baz.py",
  }
}
```

```toml title="Using the template language in TOML."
[files]
"{DOMAIN}" = "https://my-server.com"
"{PATH}" = "a/path"
"{VERSION}" = "1.2.3"
"{FROM}" = "{DOMAIN}/{PATH}/{VERSION}"
"{TO}" = "./my_module"
"{FROM}/__init__.py" = "{TO}/__init__.py"
"{FROM}/foo.py" = "{TO}/foo.py"
"{FROM}/bar.py" = "{TO}/bar.py"
"{FROM}/baz.py" = "{TO}/baz.py"
```

The `{DOMAIN}`, `{PATH}`, and `{VERSION}` placeholders are
used to create a further `{FROM}` placeholder. The `{TO}` placeholder is also
defined to point to a common sub-directory on the file system. The final four
entries use `{FROM}` and `{TO}` to copy over four files (`__init__.py`,
`foo.py`, `bar.py` and `baz.py`) from the same source to a common destination
directory.

For convenience, if the destination is just a directory (it ends with `/`)
then PyScript automatically uses the filename part of the source URL as the
filename in the destination directory.

For example, the end of the previous config file could be:

```toml
"{TO}" = "./my_module/"
"{FROM}/__init__.py" = "{TO}"
"{FROM}/foo.py" = "{TO}"
"{FROM}/bar.py" = "{TO}"
"{FROM}/baz.py" = "{TO}"
```

### Packages

The `packages` option lists
[Python packages](https://packaging.python.org/en/latest/)
to be installed onto the Python path.

!!! info 

    Pyodide uses a
    [utility called `micropip`](https://micropip.pyodide.org/en/stable/index.html)
    to install packages [from PyPI](https://pypi.org/).

    Because `micropip` is a Pyodide-only feature, and MicroPython doesn't
    support code packaged on PyPI, **the `packages` option only works with
    packages hosted on PyPI when using Pyodide**.

    MicroPython's equivalent utility,
    [`mip`](https://docs.micropython.org/en/latest/reference/packages.html),
    **uses a separate repository of available packages called
    [`micropython-lib`](https://github.com/micropython/micropython-lib)**.
    When you use the `packages` option with MicroPython, it is this repository
    (not PyPI) that is used to find available packages. Many of the packages
    in `micropython-lib` are for microcontroller based activities and
    **may not work with the web assembly port** of MicroPython.

    If you need **pure Python modules for MicroPython**, you have two further
    options:

    1. Use the [files](#files) option to manually copy the source code for a
       package onto the file system.
    2. Use a URL referencing a MicroPython friendly package instead of PyPI
       package name.

The following two examples are equivalent:

```TOML title="A packages list in TOML."
packages = ["arrr", "numberwang", "snowballstemmer>=2.2.0" ]
```

```JSON title="A packages list in JSON."
{
    "packages": ["arrr", "numberwang", "snowballstemmer>=2.2.0" ]
}
```

When using Pyodide, the names in the list of `packages` can be any of the
following valid forms:

* A name of a package on PyPI: `"snowballstemmer"`
* A name for a package on PyPI with additional constraints:
  `"snowballstemmer>=2.2.0"`
* An arbitrary URL to a Python package: `"https://.../package.whl"`
* A file copied onto the browser based file system: `"emfs://.../package.whl"`

### Plugins

The `plugins` option allows user to either augment, or exclude, the list of
plugins imported out of the box from *core* during bootstrap.

While augmenting requires some knowledge about *core* internals, excluding
some plugin might be desired to avoid such plugin behavior and, in edge cases,
reduce the amount of network requests to bootstrap *PyScript*.

It is possible to check the [list of plugins](https://github.com/pyscript/pyscript/blob/main/core/src/plugins.js)
we offer by default, where each *key* is used as plugin name and could be also
disabled using the `!pugin-name` convention, here an example:

```TOML title="Specify plugins in TOML"
plugins = ["custom_plugin", "!error"]
```

```JSON title="Specify plugins in JSON"
{
    "plugins": ["custom_plugin", "!error"]
}
```

!!! info

    The `"!error"` syntax is a way to turn off a plugin built into PyScript
    that is enabled by default.

    It is possible to turn off other plugins too using the very same
    convention.

!!! warning

    Please note `plugins` are currently a *core* only feature. If you need any
    extra functionality out of the box *files* or *js_modules* are the current
    way to provide more features without needing to file a *PR* in *core*.

    This means that the current `plugins` proposal is meant to disable our own
    plugins but it has no usage to add 3rd party plugins right now.

### JavaScript modules

It's easy to import and use JavaScript modules in your Python code. This
section of the docs examines the configuration needed to make this work. How
to make use of JavaScript is dealt with
[elsewhere](../dom/#working-with-javascript).

We need to tell PyScript about the JavaScript modules you want to
use. This is the purpose of the `js_modules` related configuration fields.

There are two fields:

* `js_modules.main` defines JavaScript modules loaded in the context of the
  main thread of the browser. Helpfully, it is also possible to interact with
  such modules **from the context of workers**. Sometimes such modules also
  need CSS files to work, and these can also be specified.
* `js_modules.worker` defines JavaScript modules loaded into the context of
  the web worker. Such modules **must not expect** `document` or `window`
  references (if this is the case, you must load them via `js_modules.main` and
  use them from the worker). However, if the JavaScript module could work
  without such references, then performance is better if defined on a worker.
  Because CSS is meaningless in the context of a worker, it is not possible to
  specify such files in a worker context.

Once specified, your JavaScript modules will be available under the
`pyscript.js_modules.*` namespace.

To specify such modules, simply provide a list of source/module name pairs.

For example, to use the excellent [Leaflet](https://leafletjs.com/) JavaScript
module for creating interactive maps you'd add the following lines:

```TOML title="JavaScript main thread modules defined in TOML."
[js_modules.main]
"https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet-src.esm.js" = "leaflet"
"https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css" = "leaflet" # CSS
```

```JSON title="JavaScript main thread modules defined in JSON."
{
    "js_modules": {
        "main": {
            "https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet-src.esm.js": "leaflet",
            "https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css": "leaflet"
        }
    }
}
```

!!! info
    
    Notice how the second line references the required CSS needed for the
    JavaScript module to work correctly.

    The CSS file **MUST** target the very same name as the JavaScript module to
    which it is related.

!!! warning

    Since the Leaflet module expects to manipulate the DOM and have access to
    `document` and `window` references, **it must only be added via the
    `js_modules.main` setting** (as shown) and cannot be added in a worker
    context.

At this point Python code running on either the main thread or in a
worker will have access to the JavaScript module like this:

```python title="Making use of a JavaScript module from within Python."
from pyscript.js_modules import leaflet as L

map = L.map("map")

# etc....
```

Some JavaScript modules (such as
[html-escaper](https://www.npmjs.com/package/html-escaper)) don't require
access to the DOM and, for efficiency reasons, can be included in the worker
context:

```TOML title="A JavaScript worker module defined in TOML."
[js_modules.worker]
"https://cdn.jsdelivr.net/npm/html-escaper" = "html_escaper"
```

```JSON title="A JavaScript worker module defined in JSON."
{
    "js_modules": {
        "worker": {
            "https://cdn.jsdelivr.net/npm/html-escaper": "html_escaper"
        }
    }
}
```

However, `from pyscript.js_modules import html_escaper` would then only work
within the context of Python code **running on a worker**.

### sync_main_only

Sometimes you just want to start an expensive computation on a web worker
without the need for the worker to interact with the main thread. You're simply
awaiting the result of a method exposed from a worker.

This has the advantage of not requiring the use of `SharedArrayBuffer` and
[associated CORS related header configuration](../workers/#http-headers).

If the `sync_main_only` flag is set, then **interactions between the main thread
and workers are limited to one way calls from the main thread to methods
exposed by the workers**.

```TOML title="Setting the sync_main_only flag in TOML."
sync_main_only = true
```

```JSON title="Setting the sync_main_only flag in JSON."
{
    "sync_main_only": true
}
```

If `sync_main_only` is set, the following caveats apply:

* It is not possible to manipulate the DOM or do anything meaningful on the
  main thread **from a worker**. This is because Atomics cannot guarantee
  sync-like locks between a worker and the main thread.
* Only a worker's `pyscript.sync` methods are exposed, and **they can only be
  awaited from the main thread**.
* The worker can only `await` main thread references one after the other, so
  developer experience is degraded when one needs to interact with the
  main thread.

### experimental_create_proxy

Knowing when to use the `pyscript.ffi.create_proxy` method when using Pyodide
can be confusing at the best of times and full of
[technical "magic"](../ffi#create_proxy).

This _experimental_ flag, when set to `"auto"` will cause PyScript to try to
automatically handle such situations, and should "just work".

```TOML title="Using the experimental_create_proxy flag in TOML."
experimental_create_proxy = "auto"
```

```JSON title="Using the experimental_create_proxy flag in JSON."
{
    "experimental_create_proxy": "auto"
}
```

!!! warning

    **This feature is _experimental_ and only needs to be used with Pyodide.**

    Should you encounter problems (such as problematic memory leaks) when using
    this flag with Pyodide, please don't hesitate to
    [raise an issue](https://github.com/pyscript/pyscript/issues) with a
    reproducable example, and we'll investigate.

### Custom 

Sometimes plugins or apps need bespoke configuration options.

So long as you don't cause a name collision with the built-in option names then
you are free to use any valid data structure that works with both TOML and JSON
to express your configuration needs.

Access the current configuration via `pyscript.config`, a Python `dict`
representing the configuration:

```python title="Reading the current configuration."
from pyscript import config


# It's just a dict.
print(config.get("files"))
```

!!! note

    Changing the `config` dictionary at runtime doesn't change the actual
    configuration.
