# Beginning PyScript

PyScript is an open source platform for
<a href="https://python.org/" target="_blank">Python</a>
in the browser.

<a href="https://pyscript.com/" target="_blank">Write code</a>, curate the
project's assets, and test your application just like you normally would.

However, to distribute a PyScript application, host it on the web, then click
on the link to your application. PyScript and the browser do the rest.

Simple!

Now read on for a beginner-friendly tour of the core aspects of PyScript.
We only assume you know how to use a browser and edit text.

## An application

Usually, PyScript applications need just three things:

1. An `index.html` file that is served to your browser.
2. A description of the Python environment in which your application will run.
   This is usually specified by a `settings.json` or `settings.toml`
   configuration file (the filename name doesn't matter, but you just need to
   know you can configure your Python environment).
3. Python code (usually in a file called something like `main.py`) that defines
   how your application works.

Create these files with your favourite code editor on your local file system.
Alternatively, services like [pyscript.com](https://pyscript.com) will take
away all the pain of organising, previewing and deploying your application.

If you're using your local file system, you'll need a way to view your
application in your browser. If you already have Python installed on
your local machine, serve your files with the following command run from your
terminal and in the same directory as your files:

```sh
python3 -m http.server
```

Point your browser at [http://localhost:8000](localhost:8000). Remember to
refresh the page (`CTRL-R`) to see any updates you may have made.

!!! note

    If you're using [VSCode](https://code.visualstudio.com/) as your editor,
    the
    [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
    can be used to reload the page as you edit your files.

    Alternatively, if you have an account on [GitHub](https://github.com) you
    could use VSCode in your browser as a
    [PyScript aware "CodeSpace"](https://github.com/ntoll/codespaces-project-template-pyscript/)
    (just follow the instructions in the README file).

If you decide to use [pyscript.com](https://pyscript.com), once signed in,
create a new project by pressing the "+" button on the left-hand side below
the site's logo. You'll be presented with a page containing three columns
(listing your files, showing your code and previewing the app). The "save"
and "run" buttons do exactly what you'd expect.

![PyScript.com](assets/images/pyscript.com.png)

Let's build a simple PyScript application that translates English 🇬🇧 into
Pirate 🏴‍☠️ speak. In order to do this we'll make use of the
[arrr](https://arrr.readthedocs.io/en/latest/) library. By building this app
you'll be introduced to all the core concepts of PyScript at an introductory
level.

You can see this application embedded into the page below (try it out!):

<iframe src="../example-apps/pirate-translator/" style="border: 1px solid black; width:100%;min-height: 400px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

Let's explore each of the three files that make this app work.

### `pyscript.json`

This file tells PyScript and your browser about various
[configurable aspects](user-guide/configuration.md)
of your application. Put simply, it tells PyScript what it needs in order to run
your application. The only thing we need to show is that we require the third
party `arrr` module to do the
[actual translation](https://arrr.readthedocs.io/en/latest/).

We do this by putting `arrr` as the single entry in a list of required
`packages`, so the content of `pyscript.json` looks like this:

```json title="pyscript.json"
{
    "packages": ["arrr"]
}
```

It doesn't need to be called `pyscript.json`, but it must be either a `json`
or `toml` file containing valid PyScript configuration.

!!! info

    Want to learn more about configuration options? The
    [configuration guide](user-guide/configuration.md) covers everything from
    specifying Python packages to customising how PyScript loads and runs.

### `index.html`

Next we come to the `index.html` file that is first served to your browser.

To start out, we need to tell the browser that this HTML document uses
PyScript, and so we create a `<script>` tag that references the PyScript
module, and a `<link>` to some PyScript specific CSS, in the document's
`<head>` tag:

```html title="The head of index.html"
<!DOCTYPE html>
<html>
  <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>🦜 Polyglot - Piratical PyScript</title>
      <link rel="stylesheet" href="https://pyscript.net/releases/2026.1.1/core.css">
      <script type="module" src="https://pyscript.net/releases/2026.1.1/core.js"></script>
  </head>
  <body>

    <!-- TODO: Fill in our custom application code here... -->

  </body>
</html>
```

Notice that the `<body>` of the document is empty except for the TODO comment.
It's in here that we put standard HTML content to define our user interface, so
the `<body>` now looks like:

```html title="The body of index.html"
<body>
  <h1>Polyglot 🦜 💬 🇬🇧 ➡️ 🏴‍☠️</h1>
  <p>Translate English into Pirate speak...</p>
  <input type="text" id="english" placeholder="Type English here..." />
  <button id="translate-button">Translate</button>
  <div id="output"></div>
  <script type="py" src="./main.py" config="./pyscript.json"></script>
</body>
```

This fragment of HTML contains the application's header (`<h1>`), some
instructions between the `<p>` tags, an `<input>` box for the English text, and
a `<button>` to click to generate the translation. Notice the button has an `id`
attribute (`id="translate-button"`) which we'll use to attach a Python function
to its `click` event. Towards the end there's a `<div id="output">` which will
contain the resulting pirate speak as the application's output.

We put all this together in the `script` tag at the end of the `<body>`. This
tells the browser the script is using PyScript (`type="py"`), and where PyScript
should find the Python source code (`src="./main.py"`). Finally, we indicate
where PyScript should find the configuration (`config="./pyscript.json"`).

In the end, our HTML should look like this:

```html title="The complete index.html"
<!DOCTYPE html>
<html>
  <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>🦜 Polyglot - Piratical PyScript</title>
      <link rel="stylesheet" href="https://pyscript.net/releases/2026.1.1/core.css">
      <script type="module" src="https://pyscript.net/releases/2026.1.1/core.js"></script>
  </head>
  <body>
    <h1>Polyglot 🦜 💬 🇬🇧 ➡️ 🏴‍☠️</h1>
    <p>Translate English into Pirate speak...</p>
    <input type="text" id="english" placeholder="Type English here..." />
    <button id="translate-button">Translate</button>
    <div id="output"></div>
    <script type="py" src="./main.py" config="./pyscript.json"></script>
  </body>
</html>
```

But this only defines _how_ the user interface should look. To define its
behaviour we need to write some Python. Specifically, we need to attach a
function to the button's click event.

### `main.py`

The behaviour of the application is defined in `main.py`. It looks like this:

```python linenums="1" title="main.py"
import arrr
from pyscript import web, when


@when("click", "#translate-button")
def translate_english(event):
    """
    Translate English text to Pirate speak.
    """
    input_text = web.page["english"]
    english = input_text.value
    output_div = web.page["output"]
    output_div.innerText = arrr.translate(english)
```

It's not very complicated Python code.

On line 1 the `arrr` module is imported so we can do the actual English to
Pirate translation. If we hadn't told PyScript to download the `arrr` module
in our `pyscript.json` configuration file, this line would cause an error.
PyScript has ensured our environment is set up with the expected `arrr` module
before our Python code is evaluated.

Line 2 imports the `web` module and the `when` decorator from `pyscript`. The
`web` module provides a Pythonic way to interact with the web page, while
`when` is used to easily attach Python functions to browser events.

On line 5 we use the `@when` decorator to attach our function to the button's
click event. The decorator takes two arguments: the event type (`"click"`) and
a CSS selector identifying the element (via the id `"#translate-button"`).
This is PyScript's idiomatic way to handle events - much more Pythonic than
HTML attributes.

The `translate_english` function is defined on line 6. It takes a single
parameter called `event`, which represents the browser event that triggered the
function (in this case, the user's click on the button).

Inside the body of the function we use `web.page["english"]` to get a reference
to the `<input>` element with the id "english". The `web.page` object
represents the current web page, and using the square bracket notation
(`web.page["element-id"]`) is PyScript's Pythonic way to find elements by their
unique id. We assign the result to `input_text`, then extract the user's
`english` text from the `input_text`'s `value` attribute.

Next, we get a reference called `output_div` that points to the `<div>` element
with the id "output" using the same `web.page["output"]` pattern. Finally, we
assign the `innerText` of the `output_div` to the result of calling
[`arrr.translate`](https://arrr.readthedocs.io/en/latest/#arrr.translate)
to actually translate the `english` to something piratical.

That's it!

!!! info "Alternative: JavaScript-style DOM access"

    PyScript also provides direct access to the browser's JavaScript APIs. If
    you're already familiar with JavaScript, you can use `document.querySelector`
    and other standard
    [DOM methods](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model).

## Editing your app

If you use an IDE (like VSCode or PyCharm) then you'll probably want it to
auto-suggest and introspect aspects of the Python code you're writing. The
problem is that the `pyscript` namespace *we provide* isn't installed anywhere
(because it's in your browser, not your IDE's context) so such information
isn't, by default, picked up.

Thankfully Python stubs come to the rescue.

Members of our community have
[created Python stub files for PyScript](https://github.com/pyscript/pyscript-stubs).
You should clone the linked-to repository and configure your IDE to consume the
stub files.

For example, let's say you
[cloned the repository](https://github.com/pyscript/pyscript-stubs) into
`~/src/stubs/pyscript-stubs`, then in VSCode, you'd create, in your PyScript
project, a file called `.vscode/settings.json` and add the following:

```js
{
    "python.analysis.stubPath": "~/src/stubs/pyscript-stubs/src/pyscript-stubs"
}
```

Then restart the Python language server in VSCode (press `Ctrl+Shift+P`, or
`Cmd+Shift+P` on Mac, to open the Command Palette and type
`Python: Restart Language Server`).

!!! note

    The stubs themselves are found within the `src/pyscript-stubs` directory
    in the git repository, hence the longer path in the configuration file.

## Sharing your app

### From a web server

To share your PyScript application, host the three files (`pyscript.json`, 
`index.html` and `main.py`) in the same directory on a static web server.

Any static web host will work (for example,
[GitHub Pages](https://pages.github.com/),
[Amazon's S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html),
[Google Cloud](https://cloud.google.com/storage/docs/hosting-static-website) or
[Microsoft's Azure](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website)).

### Using PyScript.com

If you're using [pyscript.com](https://pyscript.com) for development, you can also
deploy directly from there. Save all your files and click the "run" button to test
your application. The platform provides hosting and generates a shareable link for
your app.

## Run PyScript offline

To run PyScript offline, without the need of a CDN or internet connection, read
the [offline guide](user-guide/offline.md) section of the user guide.

We also provide an `offline.zip` file with
[each release](https://pyscript.net/releases/2026.1.1/). This file contains
everything you need for an offline version of PyScript: PyScript itself,
versions of Pyodide and MicroPython, and an index.html page from which you
could create your offline-first PyScript work.

## Conclusion

Congratulations!

You have just created your first PyScript app.

But PyScript can do so much more than update text on a page. Here are some of
the powerful and fun capabilities waiting for you:

**Rich output with `display()`**: Instead of manually finding elements and
setting their content, you can use PyScript's `display()` function to show
Python objects, images, and charts directly on your page. Imagine displaying a
matplotlib chart or a pandas DataFrame with a single function call. Learn more in
the [user guide](user-guide/display.md).

**Create dynamic interfaces**: The `pyscript.web` module lets you create entire
user interfaces from Python code - build forms, tables, and interactive
components without writing HTML. You can compose complex layouts using familiar
Python syntax. Explore the possibilities in the
[DOM interaction guide](user-guide/dom.md).

**Handle any browser event**: Beyond simple clicks, you can respond to
keyboard input, mouse movements, form submissions, and more. PyScript makes it
easy to create rich, interactive experiences. See the
[events guide](user-guide/events.md) for details.

**Access device capabilities**: Capture photos from the camera, record audio,
read files from the user's computer, store data locally - PyScript gives your
Python code access to modern web capabilities. Check out the
[media guide](user-guide/media.md) and [filesystem guide](user-guide/filesystem.md)
for more information.

**Build fast, responsive apps**: Use web workers to run Python code in the
background, keeping your interface smooth even during heavy computation. Perfect
for data processing, simulations, or any CPU-intensive task.
[Learn about workers here](user-guide/workers.md).

The [user guide](user-guide/index.md) explores all these topics and more. Keep
reading to discover what you can build with PyScript! And if you build something
wonderful, please
[share it via our community discord server](https://discord.gg/HxvBtukrg2) (we
love to learn about and celebrate what folks have been up to).