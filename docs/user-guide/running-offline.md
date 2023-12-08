# Running PyScript offline

Althought users will want to create and share PyScript apps on the internet, there are cases when user want to run PyScript applications offline, in an airgapped fashion. This means that both PyScript core and the interpreter used to run code need to be served with the application itself. In short, the 2 main explicit tasks needed to create an offline PyScript application are:

* download and include PyScript core (`core.js`)
* download and include the [Python] interpreters you want to use in your Application

## Downloading and Including PyScript's `core.js`

There are at least 2 ways to use PyScript offline:

  * by **cloning the repository**, then building and installing dependencies and then run and then reach the `./dist/` folder
  * by **grabbing the npm package** which for simplicity sake will be the method used here at least until we find a better place to *pin* our *dist* folder via our CDN and make the procedure even easier than it is now

In the examples below, we'll assume we are creating a PyScript Application folder called `pyscript-offline` and we'll add all the necessary files to the folder. 

First of all, we are going to create a `pyscript-offline` folder as reference.

```sh
mkdir -p pyscript-offline
cd pyscript-offline
```

### Adding ore by Cloning the Repository

...

### Adding core by Installing `@pyscript/core` Locally

First of all, ensure you are in the folder you would like to test PyScirpt locally. In this case, the `pyscript-offline` folder we created earlier.

Once within the folder, be sure there is a `package.json` file. Even an empty one with just `{}` as content would work.
This is needed to be sure the folder will include locally the `npm_modules` folder instead of placing the package in the parent folder, if any.

```sh
# only if there is no package.json, create one
echo '{}' > ./package.json

# install @pyscript/core
npm i @pyscript/core
```

At this point the folder should contain a `node_module` in it and we can actually copy its `dist` folder wherever we like.

```sh
# create a public folder to serve locally
mkdir -p public

# move @pyscript/core dist into such folder
cp -R ./node_modules/@pyscript/core/dist ./public/pyscript
```

## Setting up your application

Once you've added PyScript code following one of the methods above, that's almost it! We are half way through our goal but we can already create a `./public/index.html` file that loads the project:

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

To run this project directly, after being sure that `index.html` file is saved into the `public` folder,  you can try:

```sh
python3 -m http.server -d ./public/
```

Alternatively, if you would like to test also `worker` features, you can try instead:

```sh
npx static-handler --coi ./public/
```

**Please note this page still needs the network to load** so that both *MicroPython* or *Pyodide* will be fetched from related CDN ... we are getting close though!

### Install MicroPython locally

Similarly to what we did for `@pyscript/core`, we can also install *MicroPython* from *npm*:

```sh
npm i @micropython/micropython-webassembly-pyscript
```

Our `node_modules` folder now should contain a `@micropython` one and from there we can move relevant files into our `public` folder, but let's be sure we have a target for that:

```sh
# create a folder in our public space
mkdir -p ./public/micropython

# copy related files into such folder
cp ./node_modules/@micropython/micropython-webassembly-pyscript/micropython.* ./public/micropython/
```

That folder should contain at least both `micropython.mjs` and `micropython.wasm` files and these are the files we are going to use locally via our dedicated config.

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

We are basically done: if we try to disconnect from the internet but we still run our local server, the page will still show that very same *Hello from PyScript* message :partying_face: 

### Install Pyodide locally

Currently there is a difference between MicroPython and Pyodide: the former does not have (*yet*) a package manager while the latest does, it's called *micropip*.

This is important to remember because while the procedure to have *pyodide* offline is very similar to the one we've just seen, if we want to use also 3rd party packages we also need to have these running locally ... but let's start simple:

```sh
# install locally the pyodide module
npm i pyodide

# create a folder in our public space
mkdir -p ./public/pyodide

# move all necessary files into that folder
cp ./node_modules/pyodide/pyodide* ./public/pyodide/
cp ./node_modules/pyodide/python_stdlib.zip ./public/pyodide/
```

Please **note** that also `pyodide-lock.json` file is needed so please don't change that `cp` operation as all `pyodide*` files need to be moved.

At this point, all we need to do is to change our *HTML* page to use *pyodide* instead:

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

We can now drop internet, still keeping the local server running, and everything should be fine :partying_face: 

### Local Pyodide Packages

In order to have also 3rd party packages available, we can use the bundle from [pyodide releases](https://github.com/pyodide/pyodide/releases/tag/0.24.1) that contains also packages.

Please note this bundle is more than 200MB: it not downloaded all at once, it contains each package that is required and it loads only related packages when needed.

Once downloaded and extracted, where in this case I am using `0.24.1` as reference bundle, we can literally copy and paste, or even move, all those files and folders inside the `pyodide-0.24.1/pyodide/*` directory into our `./public/pyodide/*` folder.

As the bundle contains files already present, feel free to either skip or replace the content, or even directly move that *pyodide* folder inside our `./public/` one.

Once it's done, we can now use any package we like that is available in *pyodide*. Let's see an example:

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

If everything went fine, we should now be able to read `[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]` on the page *even* if we disconnect from the Internet.

And **that's all folks** :wave: 