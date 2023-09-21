# Beginning PyScript

PyScript is a platform for Python in browsers. All you and your users need is
a modern web browser.

To distribute a PyScript application, you simply host it like a static web page
and users click on the link to your application. PyScript and the browser do
the rest.

To start creating apps with PyScript you use a development environment
where you write your code, configure the project's assets, and distribute your
application.

This page covers these core aspects of PyScript in a beginner friendly manner.
We only assume you know how to use a browser and edit text.

!!! note

    The easiest way to get the a full PyScript development environment and
    hosting provider, is to use [pyscript.com](pyscript.com) in your browser.

    It is a free service that helps you create new projects from templates, and
    then edit, preview and deploy your apps with a unique link.

    While the core features of [pyscript.com](pyscript.com) will always be
    free, additional paid-for capabilities directly support and sustain the
    PyScript open source project. Commercial and educational support is also
    available.

## An application

All PyScript applications need three things:

1. A `pyscript.toml` file that configures your application.
2. An `index.html` file that is served to your browser.
3. Python code (usually in a file called something like `main.py`) that defines
   how your application works.

You could create these files with your favourite code editor on your local file
system. Alternatively, using [pyscript.com](pyscript.com) will take away all
the pain of organising, previewing and deploying your application.

If you decide to use [pyscript.com](pyscript.com) (recommended for first
steps), once signed in, create a new project by pressing the "+" button on the
left hand side below the site's logo. You'll be presented with a page
containing three columns (listing your files, showing your code and previewing
the app). The "save" and "run" buttons do exactly what you'd expect.

If you're using your local file system, you'll need a way to view how your
application looks in your browser. To make this work you'll need to serve these
files, and if you already have Python installed it can be accomplished with
the following command run from your terminal and in the same directory as your
files:

```sh
python3 -m http.server
```

Then point your browser at [http://localhost:8000](localhost:8000). Remember to
refresh the page (`CTRL-R`) to see any updates you may have made.

!!! note
    If you're using [VSCode](https://code.visualstudio.com/) as your editor,
    the
    [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
    can be used to reload the page as you edit your files.

Let's build a simple PyScript application that translates English 🇬🇧 into
Pirate 🏴‍☠️
speak. In order to do this we'll make use of the
[arrr](https://arrr.readthedocs.io/en/latest/) library.

You can see this application embedded into the page below:

<iframe src="https://ntoll.pyscriptapps.com/piratical/latest/" style="border: 1px solid black; width:100%;min-height: 400px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

Let's explore each of the three files that make this app work.

### pyscript.toml

This file tells PyScript and your browser about various configurable aspects of
your application. In this specific example, the only thing we need to configure
is that we're using the `arrr` module.

We do this by putting `arrr` as the single entry in a list of required
`packages`, so the content of `pyscript.toml` looks like this:

``` toml title="pyscript.toml"
packages = ["arrr" ]
```

### index.html

Next we come to the `index.html` file that is first served to your browser.

To start out, we need to tell the browser that this HTML document uses
PyScript, and so we create a `<script>` tag that references the PyScript
module in the document's `<head>` tag:

```html
<!DOCTYPE html>
<html>
  <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>Arrr - Piratical PyScript</title>
      <script type="module" src="https://pyscript.net/snapshots/2023.09.1.RC1/core.js"></script>
  </head>
  <body>

    <!-- TODO: Fill in our custom application code here... -->

  </body>
</html>
```

Notice that the `<body>` of the document is empty. It's in here that we put
standard HTML content to define our user interface, so the `<body>` now looks
like:

``` html
<body>
  <h1>Arrr</h1>
  <p>Translate English into Pirate speak...</p>
  <input type="text" name="english" id="english" placeholder="Type English here..." />
  <button py-click="translate_english">Translate</button>
  <div id="output"></div>
  <script type="py" src="./main.py" config="./pyscript.toml"></script>
</body>
```

This fragment of HTML contains the application's header (`<h1>`), some
instructions between the `<p>` tags, an `<input>` box for the English text, and
a `<button>` to click to generate the translation. Towards the end there's a
`<div id="output">` which will contain the resulting pirate speak as the
application's output.

There's something strange about the `<button>` tag: it has a `py-click`
attribute with the value `translate_english`. This is, in fact, the name of a
Python function we'll run whenever the button is clicked.

Notice how the body ends with a `<script>` tag that tells the browser we're
using Python (`type="py"`), where to find the source code (`src="./main.py"`,
whose content we'll get to in a moment) and the configuration to use
(`config="./pyscript.toml"`)

In the end, our HTML should look like this:

```html title="index.html"
<!DOCTYPE html>
<html>
  <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />

      <title>Arrr - Piratical PyScript</title>
      <script type="module" src="https://pyscript.net/snapshots/2023.09.1.RC1/core.js"></script>
  </head>
  <body>
    <h1>Arrr</h1>
    <p>Translate English into Pirate speak...</p>
    <input type="text" name="english" id="english" placeholder="Type English here..." />
    <button py-click="translate_english">Translate</button>
    <div id="output"></div>
    <script type="py" src="./main.py" config="./pyscript.toml"></script>
  </body>
</html>
```

But this only defines _how_ the user interface should look. To define its
behaviour we need to write some Python. Specifically, we need to define the
`translate_english` function, used when the button is clicked.

### main.py

The behaviour of the appication is defined in `main.py`. It looks like this:

``` python linenums="1" title="main.py"
import arrr
from js import document


def translate_english(event):
    input_text = document.querySelector("#english")
    english = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = arrr.translate(english)
```

It's not very complicated Python code.

On line 1 the `arrr` module is imported so we can do the actual English to
Pirate translation. Line 2 imports the `document` object from the browser's
global JavaScript context. Put simply, the `document` allows us to reach into
the things on the web page defined in `index.html`. Finally, on line 5 the
`translate_english` function is defined.

The `translate_english` function takes a single parameter called
`event` that represents the user's click of the button (but which we don't
actually use).

Inside the body of the function we first get a reference to the `input`
element with the `document.querySelector` function that takes `#english` as its
parameter (indicating we want the element with the id "english"). We assign the
result to `input_text`, then extract the user's `english` from the
`input_text`'s `value`. Next, we get a reference called `output_div` that
points to the `div` element with the id "output". Finally, we assign the
`innerText` of the `output_div` to the result of calling `arrr.translate`
(to actually translate the `english` to something piratical).

That's it!

## Sharing your app

### PyScript.com

If you're using [pyscript.com](pyscript.com), you should save all your files
and click the "run" button. Assuming you've copied the code properly, you
should have a fine old time translating English to Pirate-ish.

Alternatively, [click here to see a working example of this app](https://ntoll.pyscriptapps.com/piratical/latest/).
Notice that the bottom right hand corner contains a link to view the code on
[pyscript.com](pyscript.com).

### From a web server

Just host the three files (`pyscript.toml`, `index.html`
and `main.py`) in the same directory on a static web server somewhere.

Clearly, we recommend you use [pyscript.com](pyscript.com) for this, but any
static web host will do (for example,
[GitHub Pages](https://pages.github.com/),
[Amazon's S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html),
[Google Cloud](https://cloud.google.com/storage/docs/hosting-static-website) or
[Microsoft's Azure](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website)).

## Conclusion

Congratulations!

You have just created your first PyScript app, and understand
the core concepts needed to build yet more interesting things of your own.

PyScript is extremely powerful, and these beginner steps only just scratch the
surface. To learn about PyScript in more depth, check out
[our user guide](/user-guide).
