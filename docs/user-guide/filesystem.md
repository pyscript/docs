# Filesystem

As you know, the filesystem is where you store files. For Python to work, there
needs to be a filesystem in which Python packages, modules, and data for your
applications can be found. When you `import` a library or `open()` a file,
Python looks in the filesystem.

However, things are not as they may seem in the browser environment.

This guide clarifies what PyScript means by a filesystem, and the ways in which
PyScript interacts with such concepts.

## Two filesystems

PyScript interacts with two distinct filesystems.

The first is provided by the browser, thanks to
[Emscripten](https://emscripten.org/docs/api_reference/Filesystem-API.html).
This is a virtual in-memory filesystem that has nothing to do with your
device's local filesystem. It exists entirely within the browser based sandbox
used by PyScript. The [`files` configuration option](configuration.md#files)
defines what is found on this filesystem.

The second filesystem is your device's actual local filesystem - the hard drive
on your laptop, mobile, or tablet. PyScript provides an API for accessing it,
but this requires explicit permission from the user. Think of it as
gate-keeping a bridge between the sandboxed world of the browser and the
outside world of your device's filesystem. Once mounted, *a folder from your
local filesystem appears at a directory in the browser's virtual filesystem*.

!!! danger 

    **Access to the device's local filesystem is only available in recent Chromium
    based browsers**. The maximum capacity for files shared in this way is 4GB.

    Firefox and Safari do not support this capability yet, so it is not
    available to PyScript running in these browsers.

## The in-browser virtual filesystem

The filesystem that both Pyodide and MicroPython use by default is the
[in-browser virtual filesystem](https://emscripten.org/docs/api_reference/Filesystem-API.html).
Opening files and importing modules takes place in relation to this sandboxed
environment. You configure it via the [`files` entry in your
settings](configuration.md#files).

Here's a simple example. First, configure a file to be fetched:

```json
{
  "files": {
    "https://example.com/myfile.txt": "./myfile.txt"
  }
}
```

Then use the resulting file as usual from Python:

```python
with open("myfile.txt", "r") as myfile:
    print(myfile.read())
```

Currently, each time you reload the page, the filesystem is recreated afresh.
Any data stored by PyScript to this filesystem will be lost when you reload. In
the future, we may make it possible to configure the in-browser virtual
filesystem as persistent across reloads.

!!! info

    The [Emscripten filesystem article](https://emscripten.org/docs/porting/files/file_systems_overview.html)
    provides an excellent technical overview of the browser based virtual
    filesystem's implementation and architecture.

In summary, the PyScript filesystem is
contained within the browser's sandbox, and each instance of a Python
interpreter used by PyScript runs in a separate sandbox. They do not share
virtual filesystems. All Python related filesystem operations work as expected
with each isolated filesystem. The virtual filesystem is configured via the `files`
entry in your settings. Currently, the filesystem is not persistent between
page reloads, and has a maximum capacity of 4GB of data (a limitation we cannot
control).

## The device's local filesystem

!!! warning

    Access to the device's local filesystem currently only works on recent
    Chromium based browsers.

Your device that runs your browser has a filesystem provided by a hard drive.
Thanks to the [`pyscript.fs` namespace](../api/fs.md), both MicroPython and Pyodide can gain
access to this filesystem, should the user of your code allow this to happen.

This requires what's called a
[transient activation](https://developer.mozilla.org/en-US/docs/Glossary/Transient_activation)
for the purposes of
[user activation of gated features](https://developer.mozilla.org/en-US/docs/Web/Security/User_activation).
Put simply, before your code gains access to their local filesystem, an
explicit agreement needs to be gathered from the user. Part of this process
involves asking the user to select a target directory on their local filesystem
to which PyScript will be given access.

The directory on their local filesystem, selected by the user, is then mounted
to a given directory inside the browser's virtual filesystem. In this way, a
mapping is made between the sandboxed world of the browser and the outside
world of the user's filesystem.

Your code will then be able to perform all the usual filesystem related
operations provided by Python within the mounted directory. However, such
changes will not take effect on the local filesystem until your code explicitly
calls the `sync()` function. At this point, the state of the in-browser virtual
filesystem and the user's local filesystem are synchronised.

!!! warning

    Changes you make to mounted files are not automatically saved to the local
    filesystem. You must call `fs.sync()` to persist them.

The following code demonstrates the simplest use case:

```python
# Chromium only browsers!
from pyscript import fs


# Ask for permission to mount any local folder into the virtual
# filesystem. The folder "/local" refers to the directory on the
# virtual filesystem to which the user-selected directory will be
# mounted.
await fs.mount("/local")

# Do file related operations here.
with open("/local/data.txt", "w") as f:
    f.write("Hello from PyScript!")

# Ensure changes are persisted to the local filesystem's folder.
await fs.sync("/local")

# If needed, sync and unmount to free RAM.
await fs.unmount("/local")
```

It is possible to use multiple different local directories with the same mount
point. This is important if your application provides some generic
functionality on data that might be in different local directories. For
instance, you may have different versions of data for a PyScript based application in
different directories, and may wish to switch between them at runtime. In this
case, use the following technique:

```python
# Mount a local folder specifying a different handler. This requires a
# user explicit transient action (once).
await fs.mount("/local", id="v1")

# Operate on that folder.
with open("/local/model.dat", "r") as f:
    data = f.read()
await fs.unmount("/local")

# Mount a different local folder specifying a different handler. This
# also requires a user explicit transient action (once).
await fs.mount("/local", id="v2")

# Operate on that folder.
with open("/local/model.dat", "r") as f:
    data = f.read()
await fs.unmount("/local")

# Go back to the original handler. No transient action required now.
await fs.mount("/local", id="v1")

# Operate again on that folder.
```

In addition to the mount `path` and handler `id`, the `fs.mount()` function
accepts two further arguments. The `mode` parameter (by default `"readwrite"`)
indicates the sort of activity available to the user. It can also be set to
`"read"` for read-only access to the local filesystem. This is part of the
[web standards](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker#mode)
for directory selection. The `root` parameter (by default `""`) is a hint
to the browser for where to start picking the path that should be mounted
in Python. Valid values are `"desktop"`, `"documents"`, `"downloads"`,
`"music"`, `"pictures"`, or `"videos"`
[as per web standards](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker#startin).

The `sync()` and `unmount()` functions only accept the mount `path` used in the
browser's local filesystem.

!!! info

    Mounting requires user activation. It must happen during or shortly after a
    user interaction like a button click. This security requirement prevents sites
    from accessing your filesystem without your knowledge. **Always attach your
    `fs.mount()` call to a button click or similar user action**.

## Example: Note-taking application

Here's a simple note-taking application demonstrating local filesystem access:

!!! warning

    If the "Select Folder" button appears unresponsive, it's because your
    browser does not support local filesystem access.

    Remember, **this is a Chromium only feature** at this moment in time.

<iframe src="../../example-apps/note-taker/" style="border: 1px solid black; width:100%; min-height: 500px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/note-taker).

This application lets you select a folder on your computer and save notes into
it. The notes persist between page reloads because they're saved to your actual
filesystem, not the browser's temporary virtual filesystem.

Click "Select Folder" and the browser will prompt you to choose a directory.
Once mounted, you can type your note and click "Save Note". The file will be
written to your chosen folder and will still be there after you close the
browser.

## What's next

Now that you understand PyScript's filesystems, explore these related topics
to deepen your knowledge.

**[Workers](workers.md)** - Display content from background threads
(requires explicit `target` parameter).

**[FFI](ffi.md)** - Understand how JavaScript modules integrate with
Python through the foreign function interface.

**[Media](media.md)** - Capture photos and video with the camera or 
record audio with your microphone.

**[Offline](offline.md)** - Use PyScript while not connected to the internet.