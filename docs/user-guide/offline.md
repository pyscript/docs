# Running Offline

PyScript applications typically load from a Content Delivery Network
or webserver, fetching core files and Python interpreters over the internet.
This works well when you have reliable network access, but sometimes you need
applications to run offline ~ in air-gapped environments, on local
networks, or where internet connectivity isn't available or is patchy.

Running PyScript offline means bundling everything your application
needs locally. This guide explains how to package PyScript core and
Python interpreters so your applications work without network access.

## What you need

An offline PyScript application requires two components available
locally:

The first is PyScript core itself - the `core.js` file and associated
resources that provide the runtime. This is what loads interpreters,
manages execution, and bridges Python to the browser.

The second is the Python interpreter your application uses - either
Pyodide or MicroPython. These are substantial files containing the
entire Python runtime compiled to WebAssembly.

If your application imports Python packages, those need to be bundled
locally as well. For Pyodide applications using numpy, pandas, or other
libraries, the package files must also be available offline.

## Shortcut

Helpfully, since the end of 2025, all
[releases of PyScript](https://pyscript.net/releases/2025.11.2/)
have an associated `offline`
zip file containing everything you need. Just download it, unpack it and
start to modify the content of the `index.html` found therein to your needs.

Read on, if you want to modify or learn how such assets are created.

## Getting PyScript core

You have two ways to obtain PyScript core files.

### Using npm (recommended)

The simplest approach uses npm to download the distribution:

```sh
# Create your project directory.
mkdir pyscript-offline
cd pyscript-offline

# Create a package.json file.
echo '{}' > package.json

# Install PyScript core.
npm i @pyscript/core

# Copy distribution files to your public directory.
mkdir -p public
cp -R node_modules/@pyscript/core/dist public/pyscript
```

This gives you a `public/pyscript` directory containing everything
needed to run PyScript locally.

### Building from source

For development builds or customisation, clone and build the repository:

```sh
# Clone the repository.
git clone https://github.com/pyscript/pyscript.git
cd pyscript

# Follow build instructions from the developer guide.
# Once built, copy the dist folder.
cp -R dist ../pyscript-offline/public/pyscript
```

See the [developer guide](../developers.md) for detailed build
instructions.

## Setting up your application

Create an HTML file that loads PyScript from local paths rather than the
CDN:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyScript Offline</title>
  <script type="module" src="/pyscript/core.js"></script>
  <link rel="stylesheet" href="/pyscript/core.css">
</head>
<body>
  <script type="mpy">
    from pyscript import document
    
    document.body.append("Hello from PyScript")
  </script>
</body>
</html>
```

Save this as `public/index.html` and serve it locally:

```sh
python3 -m http.server -d public/
```

Open `http://localhost:8000` in your browser. PyScript loads from local
files with no network requests.

## Getting MicroPython

MicroPython is available through npm:

```sh
# Install the MicroPython package.
npm i @micropython/micropython-webassembly-pyscript

# Create target directory.
mkdir -p public/micropython

# Copy interpreter files.
cp node_modules/@micropython/micropython-webassembly-pyscript/micropython.* public/micropython/
```

This copies `micropython.mjs` and `micropython.wasm` to your public
directory. Configure your HTML to use these local files:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyScript Offline</title>
  <script type="module" src="/pyscript/core.js"></script>
  <link rel="stylesheet" href="/pyscript/core.css">
</head>
<body>
  <!-- This should be in a config file, using mpy-config for brevity. -->
  <mpy-config>
    interpreter = "/micropython/micropython.mjs"
  </mpy-config>
  <script type="mpy">
    from pyscript import document
    
    document.body.append("Hello from MicroPython offline")
  </script>
</body>
</html>
```

The `interpreter` configuration tells PyScript where to find the local
MicroPython files.

## Getting Pyodide

Pyodide is also available through npm:

```sh
# Install Pyodide.
npm i pyodide

# Create target directory.
mkdir -p public/pyodide

# Copy all necessary files.
cp node_modules/pyodide/pyodide* public/pyodide/
cp node_modules/pyodide/python_stdlib.zip public/pyodide/
```

!!! info

    Make sure to copy all files matching `pyodide*`, including
    `pyodide-lock.json`. This lock file is essential for Pyodide to
    function correctly.

Configure your HTML to use local Pyodide:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyScript Offline</title>
  <script type="module" src="/pyscript/core.js"></script>
  <link rel="stylesheet" href="/pyscript/core.css">
</head>
<body>
  <!-- This should be in a config file, using mpy-config for brevity. -->
  <py-config>
    interpreter = "/pyodide/pyodide.mjs"
  </py-config>
  <script type="py">
    from pyscript import document
    
    document.body.append("Hello from Pyodide offline")
  </script>
</body>
</html>
```

## Bundling Pyodide packages

If your application uses Python packages like numpy or pandas, you need
the Pyodide package bundle. Download it from the
[Pyodide releases page](https://github.com/pyodide/pyodide/releases).

!!! warning

    The complete package bundle exceeds 300MB. It contains all packages
    available in Pyodide. Pyodide loads packages on demand, so you only
    download what your code actually imports, but the entire bundle must
    be available locally.

Download and extract the bundle for your Pyodide version (e.g.,
`pyodide-0.29.1.tar.bz2`):

```sh
# Download the bundle.
wget https://github.com/pyodide/pyodide/releases/download/0.29.1/pyodide-0.29.1.tar.bz2

# Extract it.
tar -xjf pyodide-0.29.1.tar.bz2

# Copy package files to your public directory.
cp -R pyodide-0.29.1/pyodide/* public/pyodide/
```

Now use packages in your application:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyScript Offline</title>
  <script type="module" src="/pyscript/core.js"></script>
  <link rel="stylesheet" href="/pyscript/core.css">
</head>
<body>
  <py-config>
    interpreter = "/pyodide/pyodide.mjs"
    packages = ["pandas"]
  </py-config>
  <script type="py">
    import pandas as pd
    
    x = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = [i**2 for i in x]
    
    from pyscript import document
    document.body.append(str(result))
  </script>
</body>
</html>
```

The page will display `[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]` even with no
internet connection. Pyodide loads pandas and all dependencies from your
local package bundle.

## Testing offline operation

To verify everything works offline, disconnect from the internet and
reload your application. If it loads and runs correctly, you've
successfully configured offline operation.

You can also test using browser developer tools. Open the Network tab,
enable "Offline" mode, and reload. All resources should load from cache
or local files with no network errors.

## Serving with workers

If your application uses workers, you need a server that sets
Cross-Origin Isolation (COI) headers. These headers enable
`SharedArrayBuffer` and other features required for worker support.
[Use `mini-coi` instead](https://github.com/WebReflection/mini-coi)
of Python's simple server:

```sh
# Install mini-coi if needed.
npm i -g mini-coi

# Serve with COI headers enabled.
npx mini-coi public/
```

The `mini-coi` tool automatically sets the necessary headers to enable
worker functionality.

## What's next

Now that you understand offline deployment, explore these related
topics:

**[Architecture guide](architecture.md)** - provides technical details about
how PyScript implements workers using PolyScript and Coincident if you're
interested in the underlying mechanisms.

**[Workers](workers.md)** - Display content from background threads
(requires explicit `target` parameter).

**[Filesystem](filesystem.md)** - Learn more about the virtual
filesystem and how the `files` option works.

**[FFI](ffi.md)** - Understand how JavaScript modules integrate with
Python through the foreign function interface.

**[Media](media.md)** - Capture photos and video with the camera or 
record audio with your microphone.