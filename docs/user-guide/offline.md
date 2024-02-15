# Use PyScript Offline

Sometimes you want to run PyScript applications offline.

Both PyScript core and the interpreter used to run code need to be served with
the application itself. Two requirements are needed to create an
offline PyScript are:

* Download and include PyScript core.
* Download and include the Python interpreters used in your application.

## Get PyScript core

You have two choices:

  1. **Build from source**. Clone the repository, install dependencies, then
     build and use the content found in the `./dist/` folder.
  2. **Grab the npm package**. For simplicity this is the method we currently
     recommend as the easiest to get started.

In the following instructions, we assume the existence of a folder called
`pyscript-offline`. All the necessary files needed to use PyScript offline will
eventually find their way in there.

In your computer's command line shell, create the `pyscript-offline` folder
like this:

```sh
mkdir -p pyscript-offline
```

Now change into the newly created directory:

```sh
cd pyscript-offline
```

### PyScipt core from source

Build PyScript core by cloning the project repository and follow the
instructions in our [developer guide](/developers)

Once completed, copy the `build` folder, that was been created by the build
step, into your `pyscript-offline` folder.

### PyScript core from `npm`

Ensure you are in the `pyscript-offline` folder created earlier.

Create a `package.json` file. Even an empty one with just `{}` as content will
suffice. This is needed to make sure our folder will include the local
`npm_modules` folder instead of placing assets elsewhere. Our aim is to ensure
everything is in the same place locally.

```sh
# only if there is no package.json, create one
echo '{}' > ./package.json
```

Assuming you have
[npm installed on your computer](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm),
issue the following command in the `pyscript-offline` folder to install the
PyScript core package.

```
# install @pyscript/core
npm i @pyscript/core
```

Now the folder should contain a `node_module` folder in it, and we can copy the
`dist` folder found within the `@pyscript/core` package wherever we like.

```sh
# create a public folder to serve locally
mkdir -p public

# move @pyscript/core dist into such folder
cp -R ./node_modules/@pyscript/core/dist ./public/pyscript
```

That's almost it!

## Set up your application

Simply create a `./public/index.html` file that loads the local PyScript:

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

Run this project directly (after being sure that `index.html` file is saved
into the `public` folder):

```sh
python3 -m http.server -d ./public/
```

If you would like to test `worker` features, try instead:

```sh
npx static-handler --coi ./public/
```

## Download a local interpreter

PyScript officially supports *MicroPython* and *Pyodide* interpreters, so let's
see how to get a local copy for each one of them.

### Local MicroPython

Similar to `@pyscript/core`, we can also install *MicroPython* from *npm*:

```sh
npm i @micropython/micropython-webassembly-pyscript
```

Our `node_modules` folder should contain a `@micropython` one and from there we
can move relevant files into our `public` folder.

Let's be sure we have a target for that:

```sh
# create a folder in our public space
mkdir -p ./public/micropython

# copy related files into such folder
cp ./node_modules/@micropython/micropython-webassembly-pyscript/micropython.* ./public/micropython/
```

The folder should contain at least both `micropython.mjs` and
`micropython.wasm` files. These are the files to use locally via a dedicated
config.

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
  <mpy-config>
    interpreter = "/micropython/micropython.mjs"
  </mpy-config>
  <script type="mpy">
    from pyscript import document

    document.body.append("Hello from PyScript")
  </script>
</body>
</html>
``` 

### Local Pyodide

Remember, Pyodide uses `micropip` to install third party packages. While the
procedure for offline Pyodide is very similar to the one for MicroPython,
if we want to use 3rd party packages we also need to have these available
locally. We'll start simple and cover such packaging issues at the end.

```sh
# locally install the pyodide module
npm i pyodide

# create a folder in our public space
mkdir -p ./public/pyodide

# move all necessary files into that folder
cp ./node_modules/pyodide/pyodide* ./public/pyodide/
cp ./node_modules/pyodide/python_stdlib.zip ./public/pyodide/
```

Please **note** that the `pyodide-lock.json` file is needed, so please don't
change that `cp` operation as all `pyodide*` files need to be moved.

At this point, all we need to do is to change the configuration on our *HTML*
page to use *pyodide* instead:

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
  </py-config>
  <script type="py">
    from pyscript import document

    document.body.append("Hello from PyScript")
  </script>
</body>
</html>
```

## Wrap up

That's basically it!

Disconnect from the internet, run the local server, and the page will still
show that very same `Hello from PyScript` message.

## Local Pyodide packages

Finally, we need the ability to install Python packages from a local source
when using Pyodide.

Put simply, we use the packages bundle from
[pyodide releases](https://github.com/pyodide/pyodide/releases/tag/0.24.1).

!!! warning

    This bundle is more than 200MB!

    It contains each package that is required by Pyodide, and Pyodide will only
    load packages when needed.

Once downloaded and extracted (we're using version `0.24.1` in this example),
we can simply copy the files and folders inside the `pyodide-0.24.1/pyodide/*`
directory into our `./public/pyodide/*` folder.

Feel free to either skip or replace the content, or even directly move the
`pyodide` folder inside our `./public/` one.

Now use any package available in via the Pyodide bundle.

For example:

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
    x = pd.Series([1,2,3,4,5,6,7,8,9,10])

    from pyscript import document
    document.body.append(str([i**2 for i in x]))
  </script>
</body>
</html>
```

We should now be able to read `[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]` on the
page *even* if we disconnect from the Internet.

That's it!
