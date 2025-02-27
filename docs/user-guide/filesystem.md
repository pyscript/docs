# PyScript and Filesystems

As you know, the filesystem is where you store files. For Python to work there
needs to be a filesystem in which Python packages, modules and data for your
apps can be found. When you `import` a library, or when you `open` a file, it
is on the in-browser virtual filesystem that Python looks.

However, things are not as they may seem.

This section clarifies what PyScript means by a filesystem, and the way in
which PyScript interacts with such a concept.

## Two filesystems

PyScript interacts with two filesystems.

1. The browser, thanks to
   [Emscripten](https://emscripten.org/docs/api_reference/Filesystem-API.html),
   provides a virtual in-memory filesystem. **This has nothing to do with your
   device's local filesystem**, but is contained within the browser based
   sandbox used by PyScript. The [files](../configuration/#files)
   configuration API defines what is found on this filesystem.
2. PyScript provides an easy to use API for accessing your device's local
   filesystem. It requires permission from the user to mount a folder from the
   local filesystem onto a directory in the browser's virtual filesystem. Think
   of it as gate-keeping a bridge to the outside world of the device's local
   filesystem.

!!! danger 

    Access to the device's local filesystem **is only available in Chromium
    based browsers**. The maximum capacity for files shared in this way is
    4GB.

    Firefox and Safari do not support this capability (yet), and so it is not
    available to PyScript running in these browsers.

## The in-browser filesystem

The filesystem that both Pyodide and MicroPython use by default is the
[in-browser virtual filesystem](https://emscripten.org/docs/api_reference/Filesystem-API.html).
Opening files and importing modules takes place in relation to this sandboxed
environment, configured via the [files](../configuration/#files) entry in your
settings.

```toml title="Filesystem configuration via TOML."
[files]
"https://example.com/myfile.txt": ""
```

```python title="Just use the resulting file 'as usual'."
# Interacting with the virtual filesystem, "as usual".
with open("myfile.txt", "r") as myfile:
    print(myfile.read())
```

Currently, each time you re-load the page, the filesystem is recreated afresh,
so any data stored by PyScript to this filesystem will be lost.

!!! info

    In the future, we may make it possible to configure the in-browser virtual
    filesystem as persistent across re-loads.

[This article](https://emscripten.org/docs/porting/files/file_systems_overview.html)
gives an excellent overview of the browser based virtual filesystem's
implementation and architecture.

The most important key concepts to remember are:

* The PyScript filesystem is contained *within* the browser's sandbox.
* Each instance of a Python interpreter used by PyScript runs in a separate
  sandbox, and so does NOT share virtual filesystems.
* All Python related filesytem operations work as expected with this
  filesystem.
* The virtual filesystem is configured via the
  [files](../configuration/#files) entry in your settings.
* The virtual filesystem is (currently) NOT persistent between page re-loads. 
* Currently, the filesystem has a maximum capacity of 4GB of data (something
  over which we have no control).

## The device's local filesystem

**Access to the device's local filesystem currently only works on Chromium
based browsers**.

Your device (the laptop, mobile or tablet) that runs your browser has a
filesystem provided by a hard drive. Thanks to the
[`pyscript.fs` namespace in our API](../../api/#pyscriptfs), both MicroPython
and Pyodide (CPython) gain access to this filesystem should the user of
your code allow this to happen.

This is a [transient activation](https://developer.mozilla.org/en-US/docs/Glossary/Transient_activation)
for the purposes of
[user activation of gated features](https://developer.mozilla.org/en-US/docs/Web/Security/User_activation).
Put simply, before your code gains access to their local filesystem, an
explicit agreement needs to be gathered from the user. Part of this process
involves asking the user to select a target directory on their local
filesystem, to which PyScript will be given access.

The directory on their local filesystem, selected by the user, is then mounted
to a given directory inside the browser's virtual filesystem. In this way a
mapping is made between the sandboxed world of the browser, and the outside
world of the user's filesystem.

Your code will then be able to perform all the usual filesystem related
operations provided by Python, within the mounted directory. However, **such
changes will NOT take effect on the local filesystem UNTIL your code
explicitly calls the `sync` function**. At this point, the state of the
in-browser virtual filesystem and the user's local filesystem are synchronised.

The following code demonstrates the simplest use case:

```python title="The core operations of the pyscript.fs API"
from pyscript import fs

# Ask once for permission to mount any local folder
# into the virtual filesystem handled by Pyodide/MicroPython.
# The folder "/local" refers to the directory on the virtual
# filesystem to which the user-selected directory will be
# mounted.
await fs.mount("/local")

# ... DO FILE RELATED OPERATIONS HERE ...

# If changes were made, ensure these are persisted to the local filesystem's
# folder.
await fs.sync("/local")

# If needed to free RAM or that specific path, sync and unmount
await fs.unmount("/local")
```

It is possible to use multiple different local directories with the same mount
point. This is important if your application provides some generic
functionality on data that might be in different local directories because
while the nature of the data might be similar, the subject is not. For
instance, you may have different models for a PyScript based LLM in different
directories, and may wish to switch between them at runtime using different
handlers (requiring their own transient action). In which case use
the following technique:

```python title="Multiple local directories on the same mount point"
# Mount a local folder specifying a different handler.
# This requires a user explicit transient action (once).
await fs.mount("/local", id="v1")
# ... operate on that folder ...
await fs.unmount("/local")

# Mount a local folder specifying a different handler.
# This also requires a user explicit transient action (once).
await fs.mount("/local", id="v2")
# ... operate on that folder ...
await fs.unmount("/local")

# Go back to the original handler or a previous one.
# No transient action required now.
await fs.mount("/local", id="v1")
# ... operate again on that folder ...
```

In addition to the mount `path` and handler `id`, the `fs.mount` function can
take two further arguments:

* `mode` (by default `"readwrite"`) indicates the sort of activity available to
  the user. It can also be set to `read` for read-only access to the local
  filesystem. This is a part of the
  [web-standards](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker#mode)
  for directory selection.
* `root` - (by default, `""`) is a hint to the browser for where to start
  picking the path that should be mounted in Python. Valid values are:
  `desktop`, `documents`, `downloads`, `music`, `pictures` or `videos`
  [as per web standards](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker#startin).

The `sync` and `unmount` functions only accept the mount `path` used in the
browser's local filesystem.
